# 🏗️ 三层架构完整文档

## 架构概述

AI 聊天应用的三层数据存储架构：

```
┌─────────────────────────────────────────────────────────────┐
│                      用户聊天界面                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   应用服务器 (FastAPI)                      │
└──────────┬──────────────────────┬───────────────────────────┘
           │                      │
           ▼                      ▼
    ┌──────────┐          ┌──────────┐
    │ 文本处理  │          │ 文件处理  │
    └────┬─────┘          └────┬─────┘
         │                     │
         └──────────┬──────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│ MinIO   │   │PostgreSQL│  │ Milvus  │
│原始文件 │   │ 元数据   │   │ 向量   │
└─────────┘   └─────────┘   └─────────┘
```

---

## 第一层：MinIO（对象存储）

### 用途
存储原始非结构化数据：
- 图片（PNG, JPG, WebP）
- 视频（MP4, WebM）
- 音频（MP3, WAV）
- 文档（PDF, DOCX）

### API 示例

```python
from minio import Minio

# 初始化客户端
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin123",
    secure=False
)

# 上传文件
client.fput_object(
    "chat-files",
    "photo.jpg",
    "/path/to/photo.jpg"
)

# 获取文件 URL
file_url = "http://localhost:9000/chat-files/photo.jpg"
```

---

## 第二层：PostgreSQL（关系数据库）

### 用途
存储结构化元数据：

```sql
-- 对话表
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 消息表
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(20) NOT NULL,
    content TEXT,
    file_url VARCHAR(1000),
    file_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### API 示例

```python
import psycopg2

# 连接数据库
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="demo_user",
    password="demo_password",
    dbname="chat_db"
)

# 插入消息
cur = conn.cursor()
cur.execute(
    "INSERT INTO messages (content, role) VALUES (%s, %s)",
    ("你好", "user")
)
conn.commit()
```

---

## 第三层：Milvus（向量数据库）

### 用途
存储向量嵌入，支持语义搜索：

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
from sentence_transformers import SentenceTransformer

# 连接 Milvus
connections.connect(host="localhost", port="19530")

# 创建 Collection
fields = [
    FieldSchema("id", DataType.VARCHAR, max_length=100, is_primary=True),
    FieldSchema("vector", DataType.FLOAT_VECTOR, dim=384),
    FieldSchema("modality", DataType.VARCHAR, max_length=50),
]
schema = CollectionSchema(fields, "Chat Vectors")
collection = Collection("chat_vectors", schema)

# 生成向量
embedder = SentenceTransformer('all-MiniLM-L6-v2')
vector = embedder.encode(["你好世界"])[0].tolist()

# 插入向量
collection.insert([{
    "id": "msg_001",
    "vector": vector,
    "modality": "text"
}])

# 语义搜索
query_vector = embedder.encode(["问候"])[0].tolist()
results = collection.search(
    data=[query_vector],
    anns_field="vector",
    param={"metric_type": "COSINE", "params": {"nprobe": 10}},
    limit=5
)
```

---

## 完整数据流示例

### 用户发送带图片的消息

```python
async def send_message(content: str, image_file: UploadFile):
    # 1️⃣ 上传图片到 MinIO
    image_url = upload_to_minio(image_file)

    # 2️⃣ 保存元数据到 PostgreSQL
    message_id = save_message_to_postgres(
        content=content,
        file_url=image_url
    )

    # 3️⃣ 生成并保存向量到 Milvus
    # 文本向量
    text_vector = embedder.encode([content])[0].tolist()

    # 图片向量（使用 CLIP）
    image_vector = clip_model.encode(image=image_file)[0].tolist()

    # 拼接向量
    combined_vector = np.concatenate([text_vector, image_vector])

    # 保存到 Milvus
    save_vector_to_milvus(message_id, combined_vector)

    return {
        "message_id": message_id,
        "image_url": image_url
    }
```

---

## 本地演示

### 启动服务

```bash
cd ~/ai-agent-learning/three-tier-arch
./start.sh
```

### 服务地址

| 服务 | 地址 | 说明 |
|------|------|------|
| API 服务 | http://localhost:8000 | FastAPI 应用 |
| API 文档 | http://localhost:8000/docs | Swagger UI |
| MinIO 控制台 | http://localhost:9001 | 文件管理 |
| PostgreSQL | localhost:5432 | 数据库 |
| Milvus | localhost:19530 | 向量数据库 |

### 测试 API

```bash
# 1. 健康检查
curl http://localhost:8000/health

# 2. 上传文件
curl -X POST http://localhost:8000/upload \
  -F "file=@photo.jpg"

# 3. 保存消息
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "测试消息"}'

# 4. 搜索消息
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "测试"}'
```

---

## 验证三层存储

### 验证 MinIO
1. 打开 http://localhost:9001
2. 登录（minioadmin / minioadmin123）
3. 查看 `chat-files` bucket

### 验证 PostgreSQL
```bash
docker exec -it demo-postgres psql -U demo_user -d chat_db
SELECT * FROM messages ORDER BY created_at DESC;
```

### 验证 Milvus
1. 打开 Attu 应用
2. 连接 `localhost:19530`
3. 查看 `chat_vectors` collection

---

## 扩展学习

完成演示后，你可以：

1. ✅ 理解三层存储架构
2. ✅ 掌握文件上传处理
3. ✅ 学习向量检索
4. ✅ 实现多模态搜索
5. ✅ 构建完整聊天应用

---

**创建时间**: 2026-03-28
**难度**: ⭐⭐⭐ (中级)
**预计时间**: 2-3 小时
