# Fase 5 — Checklist de validação

## Objetivo
Implementar pipeline RAG mínimo (retriever + prompt + geração + resposta com fontes).

## Itens
- [x] Caso de uso `RAGPipelineService` implementado na camada de aplicação.
- [x] Retriever via `VectorStorePort.search_similar`.
- [x] Prompt mínimo com contexto recuperado.
- [x] Geração via porta `GenerationPort`.
- [x] Resposta retorna fontes (`source_chunk_ids`).
- [x] Adapters Gemini para embedding e geração adicionados na infraestrutura.
- [x] Pasta `knowledge_base/` criada para upload futuro de arquivos TXT.

## Validação manual sugerida
1. `python -m unittest discover -s tests -p 'test_*.py'`
2. `python -m pip install -e .`
3. Configurar `GEMINI_API_KEY` e `QDRANT_URL` no ambiente.
