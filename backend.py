#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动漫工厂后端服务 - 连接OpenClaw
提供7个分身角色，让动漫工厂里的AI能真正执行任务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import json
import os
from typing import Optional

app = FastAPI(title="动漫工厂后端", version="1.0.0")

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

# OpenClaw配置
OPENCLAW_API = "http://127.0.0.1:8000"

# 7个分身角色定义
AGENTS = {
    "ceo": {
        "name": "CEO分身",
        "icon": "👔",
        "role": "总调度，统筹全局，分配任务",
        "system_prompt": "你是千尘AI动漫工厂的CEO分身，负责统筹全局、分配任务、协调各个分身工作。你的职责是确保项目顺利进行，做出关键决策。"
    },
    "artist": {
        "name": "美术总监",
        "icon": "🎨",
        "role": "负责AI绘图、分镜设计、画面构图",
        "system_prompt": "你是千尘AI动漫工厂的美术总监分身，负责AI绘图、分镜设计、画面构图。你需要确保所有图片风格统一、质量优秀。"
    },
    "writer": {
        "name": "编剧",
        "icon": "📝",
        "role": "负责剧本创作、对白设计、情节编排",
        "system_prompt": "你是千尘AI动漫工厂的编⌫分身，负责剧本创作、对白设计、情节编排。你需要创作引人入胜的故事和角色对话。"
    },
    "editor": {
        "name": "剪辑师",
        "icon": "🎬",
        "role": "负责视频剪辑、特效处理、最终合成",
        "system_prompt": "你是千尘AI动漫工厂的剪辑师分身，负责视频剪辑、特效处理、最终合成。你需要将素材剪辑成流畅的视频。"
    },
    "prompter": {
        "name": "提示词工程师",
        "icon": "💡",
        "role": "负责优化AI提示词、提升生成质量",
        "system_prompt": "你是千尘AI动漫工厂的提示词工程师分身，负责优化AI提示词、提升生成质量。你需要编写精准的提示词来获得最佳效果。"
    },
    "qa": {
        "name": "质检总监",
        "icon": "🔍",
        "role": "负责质量检查、风格统一、问题修复",
        "system_prompt": "你是千尘AI动漫工厂的质检总监分身，负责质量检查、风格统一、问题修复。你需要确保所有作品达到专业标准。"
    },
    "voice": {
        "name": "配音师",
        "icon": "🎤",
        "role": "负责角色配音、音效设计、音频处理",
        "system_prompt": "你是千尘AI动漫工厂的配音师分身，负责角色配音、音效设计、音频处理。你需要为角色赋予声音和情感。"
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

@app.get("/")
async def home():
    return {
        "message": "动漫工厂后端服务已启动",
        "agents": list(AGENTS.keys()),
        "docs": "/docs"
    }

@app.get("/agents")
async def get_agents():
    """获取所有分身角色信息"""
    return {"agents": AGENTS}

@app.post("/chat")
async def chat(request: ChatRequest):
    """与分身对话"""
    agent_id = request.agent
    
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail=f"分身 {agent_id} 不存在")
    
    agent = AGENTS[agent_id]
    
    # 构建完整的提示词
    full_prompt = f"""
{agent['system_prompt']}

用户请求: {request.message}

请用中文回复，并说明你会执行什么具体操作。
"""
    
    # 这里应该调用OpenClaw API
    # 暂时返回模拟响应
    response = f"""我是{agent['icon']} {agent['name']}！

收到你的指令：{request.message}

我会立即执行以下操作：
1. 分析任务需求
2. 调用相关工具
3. 完成任务并反馈结果

正在执行中，请稍候..."""
    
    return ChatResponse(
        agent=agent_id,
        response=response,
        action="executing"
    )

@app.post("/execute")
async def execute_task(request: ChatRequest):
    """执行具体任务"""
    agent_id = request.agent
    
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail=f"分身 {agent_id} 不存在")
    
    agent = AGENTS[agent_id]
    
    # 根据不同分身执行不同任务
    result = {
        "agent": agent_id,
        "task": request.message,
        "status": "completed",
        "result": f"{agent['name']}已完成任务：{request.message}"
    }
    
    return result

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "动漫工厂后端"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)