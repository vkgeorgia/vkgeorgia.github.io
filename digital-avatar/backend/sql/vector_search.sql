-- §10.4 pgvector: semantic search for RAG
-- Run once against Neon to enable vector search.
-- After running, execute scripts/generate_embeddings.py to populate knowledge_chunks.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id          SERIAL PRIMARY KEY,
    source      TEXT NOT NULL,        -- e.g. "project:HR-BOT", "file:knowledge-base/1. bio/bio.md"
    chunk_index INTEGER NOT NULL,
    content     TEXT NOT NULL,
    embedding   vector(768),          -- Gemini text-embedding-004 produces 768-dim vectors
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (source, chunk_index)
);

-- HNSW index for fast approximate nearest-neighbour search (cosine distance)
CREATE INDEX IF NOT EXISTS knowledge_chunks_embedding_idx
ON knowledge_chunks USING hnsw (embedding vector_cosine_ops);
