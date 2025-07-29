from enum import Enum
import json
import os
import requests
import time
import logging
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from pydantic import BaseModel
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - wavespeed-server - %(levelname)s - %(message)s'
)
logger = logging.getLogger("wavespeed-server")


class WaveSpeedTools(str, Enum):
    GENERATE_IMAGE = "generate_image"
    GENERATE_VIDEO = "generate_video"


class WaveSpeedResult(BaseModel):
    request_id: str
    status: str
    outputs: Optional[List[str]] = None
    error: Optional[str] = None
    processing_time: float


class LoraModel(BaseModel):
    path: str
    scale: float


class WaveSpeedServer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.wavespeed.ai/api/v3"
        
    def generate_image(self, 
                      prompt: str,
                      image: str = "",
                      mask_image: str = "",
                      loras: List[Dict[str, Union[str, float]]] = None,
                      strength: float = 0.8,
                      size: str = "1024*1024",
                      num_inference_steps: int = 28,
                      guidance_scale: float = 3.5,
                      num_images: int = 1,
                      seed: int = -1,
                      enable_base64_output: bool = False,
                      enable_safety_checker: bool = True,
                      ) -> WaveSpeedResult:
        """使用 WaveSpeed AI 生成图像"""
        
        url = f"{self.base_url}/wavespeed-ai/flux-dev-lora"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # 如果未提供 loras，使用默认值
        if not loras:
            loras = [{"path": "linoyts/yarn_art_Flux_LoRA", "scale": 1.0}]
        
        payload = {
            "prompt": prompt,
            "image": image,
            "mask_image": mask_image,
            "strength": strength,
            "loras": loras,
            "size": size,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "seed": seed,
            "enable_base64_output": enable_base64_output,
            "enable_safety_checker": enable_safety_checker
        }
        
        return self._make_api_request(url, headers, payload)
    
    def generate_video(self,
                      image_url: str,
                      prompt: str,
                      negative_prompt: str = "",
                      loras: List[Dict[str, Union[str, float]]] = None,
                      size: str = "832*480",
                      num_inference_steps: int = 30,
                      duration: int = 5,
                      guidance_scale: float = 5,
                      flow_shift: int = 3,
                      seed: int = -1,
                      enable_safety_checker: bool = True) -> WaveSpeedResult:
        """使用 WaveSpeed AI WAN-2.1 I2V 生成视频"""
        
        url = f"{self.base_url}/wavespeed-ai/wan-2.1/i2v-480p-lora"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # 如果未提供 loras，使用默认值
        if not loras:
            loras = [{"path": "Remade-AI/Deflate", "scale": 1.0}]
        
        payload = {
            "image": image_url,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "loras": loras,
            "size": size,
            "num_inference_steps": num_inference_steps,
            "duration": duration,
            "guidance_scale": guidance_scale,
            "flow_shift": flow_shift,
            "seed": seed,
            "enable_safety_checker": enable_safety_checker
        }
        
        return self._make_api_request(url, headers, payload)
    
    def _make_api_request(self, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> WaveSpeedResult:
        """发送 API 请求并处理结果"""
        begin = time.time()
        logger.info(f"正在发送请求到 WaveSpeed API: {url}")
        
        logger.info(f"请求头: {headers}")
        logger.info(f"请求体: {payload}")
        try:
            logger.info("发送 POST 请求...")
            # Comment out this code block for test
            # start
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            logger.info(f"收到响应，状态码: {response.status_code}")
            response.raise_for_status()
        
            if response.status_code != 200:
                logger.error(f"API 请求失败，状态码: {response.status_code}")
                raise McpError(f"API request failed with status code {response.status_code}")
        
            result = response.json()["data"]
            request_id = result["id"]
            logger.info(f"请求 ID: {request_id}，开始轮询结果")
            # end
            
            # for test
            #request_id = "b1d650c19c534993bb69f33fd3b2c806"
            #image: ccfd3252053d456aada155351e9847a0
            #video:9d81894b7e6f4a1ab17aea7fe78eda3c

            # 轮询结果
            result_url = f"{self.base_url}/predictions/{request_id}/result"
            result_headers = {"Authorization": f"Bearer {self.api_key}"}
            
            poll_count = 0
            while True:
                poll_count += 1
                logger.info(f"轮询结果 #{poll_count}...")
                response = requests.get(result_url, headers=result_headers)
                logger.info(f"轮询响应，状态码: {response.status_code}")
                response.raise_for_status()
                
                if response.status_code != 200:
                    logger.error(f"轮询请求失败，状态码: {response.status_code}")
                    raise McpError(f"API request failed with status code {response.status_code}")
        
                result = response.json()["data"]
                status = result["status"]
                logger.info(f"当前状态: {status}")
            
                if status == "completed":
                    end = time.time()
                    outputs = result.get("outputs", [])
                    logger.info(f"请求完成，处理时间: {end - begin:.2f} 秒")
                    return WaveSpeedResult(
                        request_id=request_id,
                        status=status,
                        outputs=outputs,
                        processing_time=end - begin
                    )
                elif status == "failed":
                    end = time.time()
                    error = result.get("error", "unknown error")
                    logger.error(f"请求失败: {error}")
                    return WaveSpeedResult(
                        request_id=request_id,
                        status=status,
                        error=error,
                        processing_time=end - begin
                    )
            
                time.sleep(0.5)
            
        except Exception as e:
            end = time.time()
            logger.exception(f"API 请求异常: {str(e)}")
            return WaveSpeedResult(
                request_id="",
                status="failed",
                error=str(e),
                processing_time=end - begin
            )


async def serve(api_key: str) -> None:
    logger.info("正在启动 WaveSpeed 服务器...")
    server = Server("mcp-wavespeed")
    wavespeed_server = WaveSpeedServer(api_key)
    logger.info("WaveSpeed 服务器已初始化")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """列出可用的 WaveSpeed 工具"""
        logger.info("客户端请求工具列表")
        return [
            Tool(
                name=WaveSpeedTools.GENERATE_IMAGE.value,
                description="Image generated using WaveSpeed ​​AI Flux Dev Lora",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Input prompt for image generation",
                        },
                        "image": {
                            "type": "string",
                            "description": "image url(used for image to image)",
                        },
                        "mask_image": {
                            "type": "string",
                            "description": "The mask image tells the model where to generate new pixels (white) and where to preserve the original image (black). It acts as a stencil or guide for targeted image editing.",
                        },
                        "loras": {
                            "type": "array",
                            "description": "List of LoRAs to apply (max 5)",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "path": {
                                        "type": "string",
                                        "description": "Path to the LoRA model，E.g.: 'linoyts/yarn_art_Flux_LoRA'"
                                    },
                                    "scale": {
                                        "type": "number",
                                        "description": "Scale of the LoRA model,"
                                    }
                                }
                            }
                        },
                        "strength": {
                            "type": "number",
                            "description": "Strength indicates extent to transform the reference image",
                        },
                        "size": {
                            "type": "string",
                            "description": "Output image size. E.g.: '1024*1024'",
                        },
                        "num_inference_steps": {
                            "type": "integer",
                            "description": "Number of inference steps",
                        },
                        "guidance_scale": {
                            "type": "number",
                            "description": "Guidance scale for generation",
                        },
                        "num_images": {
                            "type": "integer",
                            "description": "Number of images to generate",
                        },
                        "seed": {
                            "type": "integer",
                            "description": "Random seed (-1 for random)",
                        },
                        "enable_base64_output": {
                            "type": "boolean",
                            "description": "If enabled, the output will be encoded into a BASE64 string instead of a URL.",
                        },
                        "enable_safety_checker": {
                            "type": "boolean",
                            "description": "Enable safety checker",
                        },
                    },
                    "required": ["prompt", "image", "loras"],
                },
            ),
            Tool(
                name=WaveSpeedTools.GENERATE_VIDEO.value,
                description="Convert images to videos with WaveSpeed ​​AI WAN-2.1 I2V",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "image_url": {
                            "type": "string",
                            "description": "The image for generating the output.",
                        },
                        "prompt": {
                            "type": "string",
                            "description": "The prompt for generating the output.",
                        },
                        "negative_prompt": {
                            "type": "string",
                            "description": "The negative prompt for generating the output.",
                        },
                        "loras": {
                            "type": "array",
                            "description": "The LoRA weights for generating the output.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "path": {
                                        "type": "string",
                                        "description": "Path to the LoRA model，E.g.: 'Remade-AI/Deflate'"
                                    },
                                    "scale": {
                                        "type": "number",
                                        "description": "Scale of the LoRA model"
                                    }
                                }
                            }
                        },
                        "size": {
                            "type": "string",
                            "description": "The size of the output.，E.g.: '832*480'",
                        },
                        "num_inference_steps": {
                            "type": "integer",
                            "description": "The number of inference steps.",
                        },
                        "duration": {
                            "type": "integer",
                            "description": "Generate video duration length seconds.",
                        },
                        "guidance_scale": {
                            "type": "number",
                            "description": "The guidance scale for generation.",
                        },
                        "flow_shift": {
                            "type": "integer",
                            "description": "The shift value for the timestep schedule for flow matching.",
                        },
                        "seed": {
                            "type": "integer",
                            "description": "The seed for random number generation.",
                        },
                        "enable_safety_checker": {
                            "type": "boolean",
                            "description": "Whether to enable the safety checker.",
                        },
                    },
                    "required": ["image_url", "prompt", "loras"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """处理 WaveSpeed 工具调用"""
        logger.info(f"收到工具调用请求: {name}")
        logger.info(f"调用参数: {arguments}")
        try:
            if name == WaveSpeedTools.GENERATE_IMAGE.value:
                # 提取必需参数
                prompt = arguments.get("prompt")
                if not prompt:
                    raise ValueError("Required parameter is missing：prompt")
                
                # 提取可选参数
                image = arguments.get("image")
                if not image:
                    raise ValueError("Required parameter is missing：image")
                
                # 处理 loras 参数
                loras = arguments.get("loras")
                if loras is None:
                    raise ValueError("Required parameter is missing：loras")
                
                mask_image = arguments.get("mask_image", "")
                strength = float(arguments.get("strength", 0.8))
                size = arguments.get("size", "1024*1024")
                num_inference_steps = int(arguments.get("num_inference_steps", 28))
                guidance_scale = float(arguments.get("guidance_scale", 3.5))
                num_images = int(arguments.get("num_images", 1))
                seed = int(arguments.get("seed", -1))
                enable_base64_output = bool(arguments.get("enable_base64_output", False))
                enable_safety_checker = bool(arguments.get("enable_safety_checker", True))
                
                # 调用 WaveSpeed API
                logger.info("正在调用 WaveSpeed 图像生成 API...")
                result = wavespeed_server.generate_image(
                    prompt=prompt,
                    image=image,
                    mask_image=mask_image,
                    loras=loras,
                    strength=strength,
                    size=size,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    num_images=num_images,
                    seed=seed,
                    enable_base64_output=enable_base64_output,
                    enable_safety_checker=enable_safety_checker,
                )
                
                # 处理结果
                if result.status == "completed" and result.outputs:
                    # 返回图像内容
                    responses = []
                    for i, image_url in enumerate(result.outputs):
                        # 在日志中打印图像 URL
                        logger.info(f"生成的图像 URL #{i+1}: {image_url}")
                        # 只返回文本内容，包含图像 URL
                        responses.append(TextContent(
                            type="text", 
                            text=f"生成的图像 URL #{i+1}: {image_url}"
                        ))
                    
                    responses.append(TextContent(
                        type="text", 
                        text=f"图像生成成功！处理时间: {result.processing_time:.2f} 秒"
                    ))
                    return responses
                else:
                    # 返回错误信息
                    return [
                        TextContent(
                            type="text", 
                            text=f"Image generation failed: {result.error or 'unknown error'}. Processing time: {result.processing_time:.2f} seconds"
                        )
                    ]
            
            elif name == WaveSpeedTools.GENERATE_VIDEO.value:
                # 提取必需参数
                image_url = arguments.get("image_url")
                prompt = arguments.get("prompt")
                
                if not image_url:
                    raise ValueError("Required parameter is missing：image_url")
                if not prompt:
                    raise ValueError("Required parameter is missing：prompt")
                
                # 提取可选参数
                negative_prompt = arguments.get("negative_prompt", "")
                
                # 处理 loras 参数
                loras = arguments.get("loras")
                if loras is None:
                    raise ValueError("Required parameter is missing：loras")
                
                size = arguments.get("size", "832*480")
                num_inference_steps = int(arguments.get("num_inference_steps", 30))
                duration = int(arguments.get("duration", 5))
                guidance_scale = float(arguments.get("guidance_scale", 5))
                flow_shift = int(arguments.get("flow_shift", 3))
                seed = int(arguments.get("seed", -1))
                enable_safety_checker = bool(arguments.get("enable_safety_checker", True))
                
                # 调用 WaveSpeed API
                logger.info("正在调用 WaveSpeed 视频生成 API...")
                result = wavespeed_server.generate_video(
                    image_url=image_url,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    loras=loras,
                    size=size,
                    num_inference_steps=num_inference_steps,
                    duration=duration,
                    guidance_scale=guidance_scale,
                    flow_shift=flow_shift,
                    seed=seed,
                    enable_safety_checker=enable_safety_checker
                )
                
                # 处理结果
                if result.status == "completed" and result.outputs:
                    # 返回视频内容
                    video_url = result.outputs[0]
                    # 在日志中打印视频 URL
                    logger.info(f"生成的视频 URL: {video_url}")
                    return [
                        TextContent(type="text", text=f"视频生成成功！处理时间：{result.processing_time:.2f} 秒"),
                        TextContent(type="text", text=f"生成的视频 URL: {video_url}")
                    ]
                else:
                    # 返回错误信息
                    return [
                        TextContent(
                            type="text", 
                            text=f"视频生成失败：{result.error or '未知错误'}。处理时间：{result.processing_time:.2f} 秒"
                        )
                    ]
            else:
                logger.error(f"未知工具: {name}")
                raise ValueError(f"未知工具：{name}")

        except Exception as e:
            logger.exception(f"处理 WaveSpeed 请求时出错: {str(e)}")
            return [TextContent(type="text", text=f"处理 WaveSpeed 请求时出错：{str(e)}")]

    @server.list_prompts()
    async def handle_list_prompts() -> list[Tool]:
        """列出可用的提示模板"""
        return [
            Tool(
                name="wavespeed-image-prompt",
                description="使用 WaveSpeed AI 生成图像的提示模板",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "style": {
                            "type": "string",
                            "description": "图像风格，例如 'yarn_art', 'realistic', 'anime' 等",
                        },
                    },
                    "required": ["style"],
                },
            ),
            Tool(
                name="wavespeed-video-prompt",
                description="使用 WaveSpeed AI 将图像转换为视频的提示模板",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "effect": {
                            "type": "string",
                            "description": "视频效果，例如 'deflate', 'zoom', 'pan' 等",
                        },
                    },
                    "required": ["effect"],
                },
            ),
        ]

    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: Dict[str, str] | None) -> Any:
        """获取提示模板"""
        from mcp.types import GetPromptResult, PromptMessage
        
        if name == "wavespeed-image-prompt":
            if not arguments or "style" not in arguments:
                raise ValueError("缺少必需参数：style")

            style = arguments["style"]
            
            prompt_template = f"""
            我想使用 WaveSpeed AI 生成一张 {style} 风格的图像。

            请帮我使用 generate_image 工具，生成一张符合以下描述的图像：
            
            [在这里输入您的图像描述]
            
            您可以调整以下参数：
            - loras：选择合适的 LoRA 模型列表，每个包含 path 和 scale
            - strength：调整提示词强度（0-1）
            - size：设置图像尺寸
            - guidance_scale：调整创意自由度
            - seed：设置随机种子（-1 表示随机）
            - model：选择模型类型（flux-dev-lora, flux-dev, flux-dev-ultra-fast, flux-dev-lora-ultra-fast）
            
            请根据我的描述生成图像，并解释您选择的参数。
            """
            
            return GetPromptResult(
                description=f"{style} 风格的图像生成提示",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=prompt_template.strip()),
                    )
                ],
            )
        
        elif name == "wavespeed-video-prompt":
            if not arguments or "effect" not in arguments:
                raise ValueError("缺少必需参数：effect")

            effect = arguments["effect"]
            
            prompt_template = f"""
            我想使用 WaveSpeed AI 的 WAN-2.1 I2V 功能将图像转换为具有 {effect} 效果的视频。

            请帮我使用 generate_video 工具，生成一个符合以下描述的视频：
            
            [在这里输入您的视频描述]
            
            您需要提供：
            - image_url：输入图像的 URL
            - prompt：描述视频内容和效果的提示词
            
            您还可以调整以下参数：
            - loras：选择合适的 LoRA 模型列表，每个包含 path 和 scale
            - duration：设置视频时长（秒）
            - guidance_scale：调整创意自由度
            - flow_shift：调整流动效果强度
            - seed：设置随机种子（-1 表示随机）
            
            请根据我的描述生成视频，并解释您选择的参数。
            """
            
            return GetPromptResult(
                description=f"{effect} 效果的视频生成提示",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=prompt_template.strip()),
                    )
                ],
            )
        
        else:
            raise ValueError(f"未知提示模板：{name}")

    # 确保创建初始化选项并运行服务器
    logger.info("正在创建初始化选项...")
    options = server.create_initialization_options()
    logger.info("正在启动服务器...")
    async with stdio_server() as (read_stream, write_stream):
        logger.info("服务器连接已建立，准备运行...")
        await server.run(read_stream, write_stream, options)