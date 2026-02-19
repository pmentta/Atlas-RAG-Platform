# Fase 3 — Checklist de validação

## Objetivo
Introduzir a abstração de vector store e implementação concreta inicial com Qdrant local, sem pipeline RAG.

## Itens
- [x] `VectorStorePort` definido na camada de aplicação.
- [x] Implementação concreta `QdrantVectorStore` criada na infraestrutura.
- [x] Configuração de Qdrant validada em fail-fast (`QDRANT_URL`, `EMBEDDING_SIZE`).
- [x] Bootstrap valida readiness da coleção no Qdrant.
- [x] Testes unitários do adapter adicionados sem depender de serviço externo real.

## Validação manual sugerida
1. `python -m unittest discover -s tests -p 'test_*.py'`
2. `QDRANT_URL=http://localhost:6333 python -m src.main`
