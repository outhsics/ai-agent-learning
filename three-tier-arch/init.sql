-- PostgreSQL 初始化脚本
-- 创建聊天应用所需的表

-- 对话表
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 消息表
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT,
    file_url VARCHAR(1000),
    file_type VARCHAR(50),
    file_size BIGINT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at DESC);
CREATE INDEX idx_conversations_user ON conversations(user_id);

-- 插入测试数据
INSERT INTO conversations (user_id, title) VALUES
    ('test_user', '测试对话');

INSERT INTO messages (conversation_id, role, content) VALUES
    ((SELECT id FROM conversations WHERE user_id = 'test_user' LIMIT 1), 'user', '你好，我想了解一下 AI 技术'),
    ((SELECT id FROM conversations WHERE user_id = 'test_user' LIMIT 1), 'assistant', '你好！AI（人工智能）是计算机科学的一个分支，致力于创建能够模拟人类智能的系统。主要包括机器学习、深度学习、自然语言处理等领域。你想了解哪个方面？');
