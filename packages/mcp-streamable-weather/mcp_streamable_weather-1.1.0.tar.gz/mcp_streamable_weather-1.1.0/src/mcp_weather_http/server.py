import requests
import logging
import json
import click
import contextlib
import uvicorn
import mcp.types as types
from collections.abc import AsyncIterator
from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount

# 编写请求天气函数
async def fetch_weather(city: str, api_key):
    try:
        url="https://api.seniverse.com/v3/weather/now.json"
        params={
            "key": api_key,
            "location": city,
            "language": "zh-Hans",
            "unit": "c"
        }
        response = requests.get(url, params=params)
        temperature = response.json()['results'][0]['now']
    except Exception:
        return "error"
    return json.dumps(temperature)

# 通过clik设置命令行启动参数
@click.command()
@click.option("--port", default=3000, help="Port to listen on for HTTP")
@click.option(
    "--api-key",
    required=True,
    help="心知天气API key",
)
@click.option(
    "--log-level",
    default="INFO",
    help="日志级别(DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
@click.option(
    "--json-response",
    is_flag=True,
    default=False,
    help="使用JSON响应代替SSE 流式输出",
)
def main(port, api_key, log_level, json_response):
    # ---------------------- 设置日志 ----------------------
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger("weather-server")

    # 创建MCP服务端
    app = Server("Weather-Streamable-HTTP-MCP-Server")

    # 工具调用
    @app.call_tool()
    async def call_tool(name, arguments):
        """
        Handle the 'get-weather' tool call.
        """
        ctx = app.request_context
        city = arguments.get("city")
        if not city:
            raise ValueError("'city' is required in arguments")

        # 准备发起天气请求发送日志
        await ctx.session.send_log_message(
            level="info",
            data=f"Fetching weather for {city}…",
            logger="weather",
            related_request_id=ctx.request_id,
        )

        try:
            weather = await fetch_weather(city, api_key)
        except Exception as err:
            #天气请求失败发送日志
            await ctx.session.send_log_message(
                level="error",
                data=str(err),
                logger="weather",
                related_request_id=ctx.request_id,
            )
            raise
        
        # 天气请求成功发送日志
        await ctx.session.send_log_message(
            level="info",
            data="Weather data fetched successfully!",
            logger="weather",
            related_request_id=ctx.request_id,
        )

        return [
            types.TextContent(type="text", text=weather)
        ]

    # 工具列表
    @app.list_tools()
    async def list_tools():
        """
        Expose available tools to the LLM.
        """
        return [
            types.Tool(
                name="get-weather",
                description="查询指定城市的实时天气（心知天气数据）",
                inputSchema={
                    "type": "object",
                    "required": ["city"],
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，如 '北京'",
                        }
                    },
                },
            )
        ]
        
    #----------管理请求会话--------------
    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=None, #无状态，不保存历史事件
        json_response=json_response,
        stateless=True
    )
    async def handle_streamable_http(scope, receive, send):
        await session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(app):
        async with session_manager.run():
            logger.info("Weather MCP server started! 🚀")
            try:
                yield
            finally:
                logger.info("Weather MCP server shutting down…")
    
    # 将MCP服务挂载到/mcp路径上，用户访问整个路径时，就会进入刚才创建的MCP HTTP会话管理器
    starlette_app = Starlette(
        debug=False,
        routes=[Mount("/mcp", app=handle_streamable_http)],
        lifespan=lifespan,
    )

    # 利用uvicorn启动ASGI服务器并监听指定端口
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)

    return 0

if __name__ == "__main__":
    main()