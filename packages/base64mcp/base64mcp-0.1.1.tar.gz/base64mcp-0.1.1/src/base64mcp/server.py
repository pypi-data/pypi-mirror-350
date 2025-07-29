import base64
from asyncio import Server
from contextlib import asynccontextmanager
from typing import AsyncIterator

from mcp.server import FastMCP


class Env:
    def __init__(self, to_low, to_upper):
        self.to_lower = to_low
        self.to_upper = to_upper


class Client:
    def __init__(self, env: Env):
        self.env = env


def serve(env: Env):

    # 定义投传参数
    @asynccontextmanager
    async def server_lifespan(server: Server) -> AsyncIterator[dict]:
        """Manage server startup and shutdown lifecycle."""
        yield {"client": Client(env)}


    mcp = FastMCP(name="base64-mcp", lifespan=server_lifespan)

    @mcp.tool("encode")
    def encode(data: str):
        """encode str to base64"""
        # 1. 将输入字符串编码为字节串 (例如 UTF-8)
        data_bytes = data.encode('utf-8')
        # 2. 使用 b64encode 进行 Base64 编码
        encoded_bytes = base64.b64encode(data_bytes)
        # 3. 将编码后的字节串解码回字符串 (通常是 UTF-8 或 ASCII)
        encoded_str = encoded_bytes.decode('utf-8')

        client = mcp.get_context().request_context.lifespan_context['client']
        # 根据 env 的设置转换大小写
        # env.to_lower 应该是一个布尔值，这里假设它是
        is_to_lower = str(client.env.to_lower).lower() == 'true' # 确保正确解析布尔环境变量

        if is_to_lower:
            final_result = encoded_str.lower()
        elif str(client.env.to_upper).lower() == 'true': # 假设也有 to_upper 的判断逻辑
            final_result = encoded_str.upper()
        else:
            final_result = encoded_str # 默认情况，或 env.to_upper 为 False

        return final_result



    @mcp.tool("decode")
    def decode(data: str):
        """decode base64 to str"""
        # 1. 将输入的 Base64 字符串编码为字节串 (通常是 ASCII 或 UTF-8)
        base64_bytes = data.encode('ascii')
        try:
            # 2. 使用 b64decode 进行 Base64 解码
            decoded_bytes = base64.b64decode(base64_bytes)
            # 3. 将解码后的字节串解码回原始字符串 (例如 UTF-8)
            decoded_str = decoded_bytes.decode('utf-8')
        except base64.binascii.Error as e:
            # 处理可能的解码错误，例如无效的 Base64 字符串
            return f"Error decoding Base64: {e}"

        client = mcp.get_context().request_context.lifespan_context['client']
        # 根据 env 的设置转换大小写
        # env.to_lower 应该是一个布尔值，这里假设它是
        is_to_lower = str(client.env.to_lower).lower() == 'true'

        if is_to_lower:
            final_result = decoded_str.lower()
        elif str(client.env.to_upper).lower() == 'true': # 假设也有 to_upper 的判断逻辑
             final_result = decoded_str.upper()
        else:
            final_result = decoded_str # 默认情况

        return final_result


    mcp.run("stdio")