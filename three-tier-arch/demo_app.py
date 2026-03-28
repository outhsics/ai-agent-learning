#!/usr/bin/env python3
"""
三层架构演示应用
展示 MinIO + PostgreSQL + Milvus 的完整使用
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
from minio import Minio
from minio.error import S3Error
import io
import os
import uuid
from datetime import datetime
from sentence_transformers import SentenceTransformer
import numpy as np

# ==================== FastAPI 应用 ====================
app = FastAPI(title="三层架构演示", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 配置 ====================
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "chat-files")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_USER = os.getenv("POSTGRES_USER", "demo_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "demo_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "chat_db")

MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", "19530"))

# ==================== 初始化连接 ====================
# MinIO
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
    print(f"❌ MinIO 错误: {e}")

# PostgreSQL
def get_pg_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB
    )

# Milvus
connections.connect(
    alias="default",
    host=MILVUS_HOST,
    port=MILVUS_PORT
)

# 创建 Milvus collection
def create_milvus_collection():
    try:
        # 定义字段
        fields = [
            FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=100, is_primary=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=384),
            FieldSchema(name="modality", dtype=DataType.VARCHAR, max_length=50),
        ]

        # 创建 schema
        schema = CollectionSchema(fields, description="聊天消息向量")
        collection = Collection("chat_vectors", schema)

        # 创建索引
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "COSINE",
            "params": {"nlist": 128}
        }
        collection.create_index("vector", index_params)

        print(f"✅ Milvus collection 'chat_vectors' 创建成功")
        return collection
    except Exception as e:
        print(f"ℹ️  Milvus collection 可能已存在: {e}")
        return Collection("chat_vectors")

milvus_collection = create_milvus_collection()
milvus_collection.load()

# 嵌入模型
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# ==================== Pydantic 模型 ====================
class MessageRequest(BaseModel):
    conversation_id: str = None
    content: str

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

# ==================== API 路由 ====================

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "三层架构演示应用",
        "architecture": {
            "layer1": "MinIO (对象存储)",
            "layer2": "PostgreSQL (关系数据库)",
            "layer3": "Milvus (向量数据库)"
        },
        "endpoints": {
            "POST /upload": "上传文件到 MinIO",
            "POST /messages": "保存消息（三层存储）",
            "POST /search": "语义搜索消息",
            "GET /messages/{conversation_id}": "获取对话历史",
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
        "milvus": "unknown"
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

    # 检查 Milvus
    try:
        connections.get_connection_addr("default")
        status["milvus"] = "healthy"
    except:
        status["milvus"] = "unhealthy"

    return status

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    第一层：上传文件到 MinIO
    """
    try:
        # 生成唯一文件名
        file_ext = file.filename.split(".")[-1]
        unique_name = f"{uuid.uuid4()}.{file_ext}"

        # 上传到 MinIO
        data = await file.read()
        minio_client.put_object(
            MINIO_BUCKET,
            unique_name,
            io.BytesIO(data),
            length=len(data),
            content_type=file.content_type
        )

        # 生成文件 URL
        file_url = f"http://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{unique_name}"

        return {
            "success": True,
            "file_url": file_url,
            "file_name": unique_name,
            "file_size": len(data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")

@app.post("/messages")
async def save_message(request: MessageRequest):
    """
    完整三层存储演示
    1. 保存文件到 MinIO（如果有）
    2. 保存元数据到 PostgreSQL
    3. 保存向量到 Milvus
    """
    try:
        # 生成消息 ID
        message_id = str(uuid.uuid4())

        # 如果没有 conversation_id，创建新的
        if not request.conversation_id:
            conn = get_pg_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO conversations (user_id, title) VALUES (%s, %s) RETURNING id",
                ("demo_user", f"对话 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            )
            conversation_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
        else:
            conversation_id = request.conversation_id

        # ========== 第二层：PostgreSQL 保存元数据 ==========
        conn = get_pg_connection()
        cur = conn.cursor()
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

        # ========== 第三层：Milvus 保存向量 ==========
        # 生成文本向量
        vector = embedder.encode([request.content])[0].tolist()

        # 插入到 Milvus
        entities = [{
            "id": message_id,
            "vector": vector,
            "modality": "text"
        }]
        milvus_collection.insert(entities)

        return {
            "success": True,
            "message_id": message_id,
            "conversation_id": conversation_id,
            "content": request.content,
            "created_at": result[1],
            "storage": {
                "minio": "无文件上传",
                "postgres": f"消息元数据已保存 (ID: {message_id})",
                "milvus": f"向量已保存 (维度: 384)"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")

@app.post("/search")
async def search_messages(request: SearchRequest):
    """
    语义搜索演示
    """
    try:
        # 生成查询向量
        query_vector = embedder.encode([request.query])[0].tolist()

        # 在 Milvus 中搜索
        results = milvus_collection.search(
            data=[query_vector],
            anns_field="vector",
            param={"metric_type": "COSINE", "params": {"nprobe": 10}},
            limit=request.limit,
            output_fields=["modality"]
        )

        # 获取详细消息
        messages = []
        conn = get_pg_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        for hit in results[0]:
            message_id = hit.id
            similarity = hit.score

            # 从 PostgreSQL 获取完整消息
            cur.execute("SELECT * FROM messages WHERE id = %s", (message_id,))
            message = cur.fetchone()

            if message:
                messages.append({
                    "message_id": message_id,
                    "content": message["content"],
                    "similarity": f"{similarity:.2%}",
                    "created_at": message["created_at"].isoformat()
                })

        cur.close()
        conn.close()

        return {
            "query": request.query,
            "results": messages,
            "count": len(messages)
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
    print("  🚀 三层架构演示应用")
    print("="*60)
    print("\n📋 架构说明:")
    print("  第一层: MinIO (对象存储) - localhost:9000")
    print("  第二层: PostgreSQL (关系数据库) - localhost:5432")
    print("  第三层: Milvus (向量数据库) - localhost:19530")
    print("\n🌐 API 服务: http://localhost:8000")
    print("📚 API 文档: http://localhost:8000/docs")
    print("\n" + "="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
