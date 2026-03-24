#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动漫工厂后端服务 - 真正调用AI API
支持小米MiMo、火山引擎等，让7个分身真正工作
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import json
import os
import base64
from typing import Optional

app = FastAPI(title="动漫工厂后端", version="2.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="."), name="static")

# 小米MiMo API配置
MIMO_API_KEY = "sk-c3j4vatk8bf3izceepuhz5dst8bmr8t6c7b4mb7wa0ju2kze"
MIMO_BASE_URL = "https://api.xiaomimimo.com/v1"

# 火山引擎API配置（用于画图）
VOLCANO_API_KEY = "f47d6f15-832c-4b4a-8434-cb882dbe0ea2"
VOLCANO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

# 7个分身角色定义
AGENTS = {
    "ceo": {
        "name": "CEO分身",
        "icon": "👔",
        "role": "总调度，统筹全局，分配任务",
        "system_prompt": "你是一个动漫制作团队的CEO分身。你必须用中文回复，语言简洁专业。你的职责是统筹全局、分配任务、协调各个分身工作。"
    },
    "artist": {
        "name": "美术总监",
        "icon": "🎨",
        "role": "负责AI绘图、分镜设计、画面构图",
        "system_prompt": "你是一个动漫制作团队的美术总监分身。你必须用中文回复，语言专业。你的职责是负责AI绘图、分镜设计、画面构图。"
    },
    "writer": {
        "name": "编剧",
        "icon": "📝",
        "role": "负责剧本创作、对白设计、情节编排",
        "system_prompt": "你是一个动漫制作团队的编⌫分身。你必须用中文回复，语言富有创意。你的职责是负责剧本创作、对白设计、情节编排。"
    },
    "editor": {
        "name": "剪辑师",
        "icon": "🎬",
        "role": "负责视频剪辑、特效处理、最终合成",
        "system_prompt": "你是一个动漫制作团队的剪辑师分身。你必须用中文回复，语言专业。你的职责是负责视频剪辑、特效处理、最终合成。"
    },
    "prompter": {
        "name": "提示词工程师",
        "icon": "💡",
        "role": "负责优化AI提示词、提升生成质量",
        "system_prompt": "你是一个动漫制作团队的提示词工程师分身。你必须用中文回复，语言专业。你的职责是负责优化AI提示词、提升生成质量。"
    },
    "qa": {
        "name": "质检总监",
        "icon": "🔍",
        "role": "负责质量检查、风格统一、问题修复",
        "system_prompt": "你是一个动漫制作团队的质检总监分身。你必须用中文回复，语言严谨。你的职责是负责质量检查、风格统一、问题修复。"
    },
    "voice": {
        "name": "配音师",
        "icon": "🎤",
        "role": "负责角色配音、音效设计、音频处理",
        "system_prompt": "你是一个动漫制作团队的配音师分身。你必须用中文回复，语言富有表现力。你的职责是负责角色配音、音效设计、音频处理。"
    }
}

class ChatRequest(BaseModel):
    agent: str
    message: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    agent: str
    response: str
    action: Optional[str] = None
    image_url: Optional[str] = None

def call_mimo_api(system_prompt: str, user_message: str) -> str:
    """调用小米MiMo API生成回复"""
    headers = {
        "Authorization": f"Bearer {MIMO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mimo-v2-pro",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    try:
        # 调试信息
        print(f"Calling MiMo API with payload: {payload}")
        
        response = requests.post(
            f"{MIMO_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        # 调试信息
        print(f"API Response Status: {response.status_code}")
        print(f"API Response: {response.text[:500]}")
        
        if response.status_code == 200:
            result = response.json()
            # 调试信息
            print(f"Parsed JSON: {result}")
            
            # 从API响应中提取内容
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0].get("message", {})
                content = message.get("content", "")
                # 调试信息
                print(f"Extracted content: {content}")
                
                # 确保返回有效内容
                if content:
                    return content
            return "API返回格式异常"
        else:
            return f"API调用失败: {response.status_code}"
    except Exception as e:
        print(f"Exception: {str(e)}")
        return f"调用出错: {str(e)}"

def generate_image(prompt: str) -> str:
    """调用火山引擎生成图片"""
    headers = {
        "Authorization": f"Bearer {VOLCANO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "doubao-seedream-4-5-251128",
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1
    }
    
    try:
        response = requests.post(
            f"{VOLCANO_BASE_URL}/images/generations",
            headers=headers,
            json=payload,
            timeout=180
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result.get("data", [])
            if data:
                return data[0].get("url", "")
        return ""
    except Exception as e:
        return ""

@app.get("/")
async def home():
    return {
        "message": "动漫工厂后端服务已启动",
        "version": "2.0.0",
        "agents": list(AGENTS.keys()),
        "features": ["AI对话", "图片生成"],
        "docs": "/docs"
    }

@app.get("/agents")
async def get_agents():
    """获取所有分身角色信息"""
    return {"agents": AGENTS}

@app.post("/chat")
async def chat(request: ChatRequest):
    """与分身对话 - 真正调用AI"""
    agent_id = request.agent
    
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail=f"分身 {agent_id} 不存在")
    
    agent = AGENTS[agent_id]
    
    # 调用小米MiMo API
    mimo_response = call_mimo_api(agent["system_prompt"], request.message)
    
    # 调试信息
    print(f"Agent: {agent_id}")
    print(f"Message: {request.message}")
    print(f"MiMo Response: {mimo_response}")
    
    # 确保返回有效的中文内容
    if not mimo_response or len(mimo_response.strip()) == 0:
        mimo_response = f"我是{agent['icon']} {agent['name']}，已收到您的指令：{request.message}，正在处理中..."
    
    return ChatResponse(
        agent=agent_id,
        response=mimo_response,
        action="completed"
    )

@app.post("/generate-image")
async def generate_image_endpoint(request: ChatRequest):
    """生成图片"""
    agent_id = request.agent
    
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail=f"分身 {agent_id} 不存在")
    
    agent = AGENTS[agent_id]
    
    # 首先用AI优化提示词
    optimized_prompt = call_mimo_api(
        f"你是{agent['name']}，{agent['system_prompt']}。请根据用户的描述，生成一个详细的英文AI绘图提示词，用于生成动漫风格的图片。只返回提示词，不要其他内容。",
        request.message
    )
    
    # 生成图片
    image_url = generate_image(optimized_prompt)
    
    return ChatResponse(
        agent=agent_id,
        response=f"已生成图片！优化后的提示词：\n{optimized_prompt}",
        action="image_generated",
        image_url=image_url
    )

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "动漫工厂后端",
        "mimo_api": "configured",
        "volcano_api": "configured"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)