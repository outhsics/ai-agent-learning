# 🏗️ 三层架构完整演示

MinIO + PostgreSQL + Milvus 实际应用演示

---

## 📐 架构说明

### 完整数据流

```
用户发送消息
    │
    ├─► [第一层] MinIO
    │   存储原始文件（图片、视频、文档）
    │   返回: file_url
    │
    ├─► [第二层] PostgreSQL
    │   存储元数据
    │   - message_id
    │   - conversation_id
    │   - content (文本内容)
    │   - file_url (文件链接)
    │   - file_type (文件类型)
    │   - created_at
    │
    └─► [第三层] Milvus
        存储向量嵌入
        - message_id
        - vector (384维)
        - modality (text/image/audio)
```

---

## 🚀 快速开始

### 1. 启动所有服务

```bash
cd ~/.claude/three-tier-demo

# 启动 Docker Compose
docker-compose up -d

# 查看日志
docker-compose logs -f demo-app
```

### 2. 访问服务

| 服务 | 地址 | 说明 |
|------|------|------|
| **API 服务** | http://localhost:8000 | 演示应用 |
| **API 文档** | http://localhost:8000/docs | Swagger UI |
| **MinIO 控制台** | http://localhost:9001 | 对象存储管理 |
| **Attu** | 打开 Attu 应用 | Milvus 可视化 |
| **PostgreSQL** | localhost:5432 | 数据库连接 |

**MinIO 登录**：
- 用户名: `minioadmin`
- 密码: `minioadmin123`

---

## 📚 API 使用示例

### 1. 健康检查

```bash
curl http://localhost:8000/health
```

**返回**：
```json
{
  "app": "healthy",
  "minio": "healthy",
  "postgres": "healthy",
  "milvus": "healthy"
}
```

---

### 2. 上传文件（第一层）

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@/path/to/your/image.jpg"
```

**返回**：
```json
{
  "success": true,
  "file_url": "http://localhost:9000/chat-files/abc123.jpg",
  "file_name": "abc123.jpg",
  "file_size": 245678
}
```

---

### 3. 保存消息（三层存储）

```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "content": "我想学习 AI 应用开发"
  }'
```

**返回**：
```json
{
  "success": true,
  "message_id": "msg_abc123",
  "conversation_id": "conv_xyz789",
  "content": "我想学习 AI 应用开发",
  "created_at": "2026-03-28T21:00:00",
  "storage": {
    "minio": "无文件上传",
    "postgres": "消息元数据已保存 (ID: msg_abc123)",
    "milvus": "向量已保存 (维度: 384)"
  }
}
```

---

### 4. 语义搜索（第三层）

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "人工智能 学习",
    "limit": 5
  }'
```

**返回**：
```json
{
  "query": "人工智能 学习",
  "results": [
    {
      "message_id": "msg_abc123",
      "content": "我想学习 AI 应用开发",
      "similarity": "85.23%",
      "created_at": "2026-03-28T21:00:00"
    }
  ],
  "count": 1
}
```

---

### 5. 获取对话历史（第二层）

```bash
curl http://localhost:8000/messages/{conversation_id}
```

---

## 🔍 验证三层存储

### 验证第一层：MinIO

1. 打开 http://localhost:9001
2. 登录（minioadmin / minioadmin123）
3. 查看 `chat-files` bucket
4. 可以看到上传的文件

### 验证第二层：PostgreSQL

```bash
# 连接到 PostgreSQL
docker exec -it demo-postgres psql -U demo_user -d chat_db

# 查询消息
SELECT * FROM messages ORDER BY created_at DESC LIMIT 5;

# 退出
\q
```

### 验证第三层：Milvus

1. 打开 Attu 应用
2. 连接 `localhost:19530`
3. 查看 `chat_vectors` collection
4. 可以看到向量数据

---

## 🎯 实际操作流程

### 场景：用户发送带图片的消息

**步骤 1**: 上传图片到 MinIO
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@photo.jpg"
```

**步骤 2**: 保存消息（包含图片 URL）
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是什么？",
    "file_url": "http://localhost:9000/chat-files/photo.jpg"
  }'
```

**步骤 3**: 搜索相关消息
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "图片 照片"}'
```

---

## 📊 数据存储位置

| 数据类型 | 存储位置 | 查看方式 |
|---------|---------|---------|
| 原始文件 | MinIO | http://localhost:9001 |
| 元数据 | PostgreSQL | `docker exec -it demo-postgres psql ...` |
| 向量 | Milvus | Attu 应用 |

---

## 🛠️ 开发说明

### 本地运行（不使用 Docker）

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export MINIO_ENDPOINT=localhost:9000
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export MILVUS_HOST=localhost

# 运行应用
python demo_app.py
```

### 测试 API

访问 http://localhost:8000/docs 使用 Swagger UI 测试

---

## 🧹 清理

```bash
# 停止所有服务
docker-compose down

# 删除数据卷
docker-compose down -v

# 删除数据目录
rm -rf ~/.claude/three-tier-demo/data
```

---

## 📚 扩展学习

完成这个演示后，你可以：

1. ✅ 理解三层存储架构
2. ✅ 掌握 MinIO 文件上传
3. ✅ 熟悉 PostgreSQL 操作
4. ✅ 学会 Milvus 向量搜索
5. ✅ 实现完整的聊天应用

**下一步**：
- 学习 `~/.claude/MILVUS-LEARNING-PLAN.md`
- 研究 `~/.claude/PROJECT-RECOMMENDATION.md`
- 实践 Langchain-Chatchat 项目

---

**创建时间**: 2026-03-28
**难度**: ⭐⭐⭐ (中级)
**预计时间**: 2-3 小时完成
