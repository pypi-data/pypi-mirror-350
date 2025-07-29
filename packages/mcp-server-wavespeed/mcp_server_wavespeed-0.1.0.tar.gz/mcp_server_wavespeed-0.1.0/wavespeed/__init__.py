import os
import asyncio
from dotenv import load_dotenv

from .server import serve

load_dotenv()

def main():
    """MCP WaveSpeed Server - 提供 WaveSpeed AI 图像和视频生成功能"""
    import argparse

    parser = argparse.ArgumentParser(
        description="为模型提供 WaveSpeed AI 图像和视频生成能力"
    )
    parser.add_argument("--api-key", type=str, help="WaveSpeed API 密钥")

    args = parser.parse_args()
    api_key = args.api_key or os.getenv("WAVESPEED_API_KEY")
    
    if not api_key:
        raise ValueError("缺少 WaveSpeed API 密钥。请通过 --api-key 参数或 WAVESPEED_API_KEY 环境变量提供。")
    
    asyncio.run(serve(api_key))