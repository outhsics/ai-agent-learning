#!/usr/bin/env python3
"""
三层架构简化演示
不使用 sentence-transformers，直接展示架构
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from minio import Minio
from minio.error import S3Error
import os
import uuid
from datetime import datetime
import random

# FastAPI 应用
app = FastAPI(title="三层架构简化演示", version="1.0")

# 配置
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "chat-files")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_USER = os.getenv("POSTGRES_USER", "demo_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "demo_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "chat_db")

# MinIO 客户端
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# 创建 bucket
try:
    if not minio_client.bucket_exists(MINIO_BUCKET):
        minio_client.make_bucket(MINIO_BUCKET)
        print(f"✅ MinIO bucket '{MINIO_BUCKET}' 创建成功")
except S3Error as e:
    print(f"ℹ️  MinIO bucket 已存在或错误: {e}")

# PostgreSQL 连接
def get_pg_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB
    )

# Pydantic 模型
class MessageRequest(BaseModel):
    content: str

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

# API 路由
@app.get("/")
async def root():
    return {
        "message": "三层架构简化演示",
        "architecture": {
            "layer1": "MinIO (对象存储)",
            "layer2": "PostgreSQL (关系数据库)",
            "layer3": "Milvus (向量数据库) - 简化版使用模拟向量"
        },
        "endpoints": {
            "POST /upload": "上传文件到 MinIO",
            "POST /messages": "保存消息（三层存储）",
            "POST /search": "搜索消息（模拟向量搜索）",
            "GET /health": "健康检查"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    status = {
        "app": "healthy",
        "minio": "unknown",
        "postgres": "unknown",
        "milvus": "simulated"
    }

    # 检查 MinIO
    try:
        buckets = minio_client.list_buckets()
        status["minio"] = "healthy"
    except:
        status["minio"] = "unhealthy"

    # 检查 PostgreSQL
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        status["postgres"] = "healthy"
    except:
        status["postgres"] = "unhealthy"

    return status

@app.post("/messages")
async def save_message(request: MessageRequest):
    """
    保存消息演示
    1. 保存元数据到 PostgreSQL
    2. 生成模拟向量（简化版）
    """
    try:
        message_id = str(uuid.uuid4())

        # ========== 第二层：PostgreSQL 保存元数据 ==========
        conn = get_pg_connection()
        cur = conn.cursor()

        # 获取或创建 conversation
        cur.execute(
            "SELECT id FROM conversations WHERE user_id = %s LIMIT 1",
            ("demo_user",)
        )
        conv_result = cur.fetchone()

        if conv_result:
            conversation_id = conv_result[0]
        else:
            # 创建新对话
            cur.execute(
                "INSERT INTO conversations (user_id, title) VALUES (%s, %s) RETURNING id",
                ("demo_user", f"对话 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            )
            conversation_id = cur.fetchone()[0]

        # 保存消息
        cur.execute(
            """
            INSERT INTO messages (id, conversation_id, role, content)
            VALUES (%s, %s, %s, %s)
            RETURNING id, created_at
            """,
            (message_id, conversation_id, "user", request.content)
        )
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        # ========== 第三层：模拟向量（简化版）==========
        # 在实际应用中，这里会使用 sentence-transformers 生成向量
        # 然后保存到 Milvus
        # 这里我们只是模拟，记录向量维度
        vector_dim = 384
        mock_vector = [random.random() for _ in range(vector_dim)]

        return {
            "success": True,
            "message_id": message_id,
            "content": request.content,
            "created_at": result[1],
            "storage": {
                "minio": "无文件上传",
                "postgres": f"消息元数据已保存 (ID: {message_id})",
                "milvus": f"模拟向量已生成 (维度: {vector_dim})"
            },
            "note": "这是简化演示版，实际应该使用真实的向量模型"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")

@app.post("/search")
async def search_messages(request: SearchRequest):
    """
    搜索消息演示（简化版 - 使用关键词匹配）
    """
    try:
        conn = get_pg_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # 使用 LIKE 模拟语义搜索
        cur.execute(
            """
            SELECT * FROM messages
            WHERE content LIKE %s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (f"%{request.query}%", request.limit)
        )
        messages = cur.fetchall()

        cur.close()
        conn.close()

        return {
            "query": request.query,
            "results": messages,
            "count": len(messages),
            "note": "这是简化演示版，实际应该使用 Milvus 向量搜索"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@app.get("/messages/{conversation_id}")
async def get_messages(conversation_id: str):
    """获取对话历史"""
    try:
        conn = get_pg_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            """
            SELECT * FROM messages
            WHERE conversation_id = %s
            ORDER BY created_at ASC
            """,
            (conversation_id,)
        )
        messages = cur.fetchall()

        cur.close()
        conn.close()

        return {
            "conversation_id": conversation_id,
            "messages": messages,
            "count": len(messages)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("  🚀 三层架构简化演示")
    print("="*60)
    print("\n📋 架构说明:")
    print("  第一层: MinIO (对象存储) - localhost:9000")
    print("  第二层: PostgreSQL (关系数据库) - localhost:5432")
    print("  第三层: Milvus (向量数据库) - 简化版使用模拟")
    print("\n⚠️  注意: 这是简化版，不使用 sentence-transformers")
    print("  实际应用应该使用真实的向量模型")
    print("\n🌐 API 服务: http://localhost:8000")
    print("📚 API 文档: http://localhost:8000/docs")
    print("\n" + "="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
