# Fase 2 — Checklist de validação

## Objetivo
Definir entidades de domínio puras para o núcleo do RAG, sem dependências de framework.

## Itens
- [x] Entidade `Document` criada com rastreabilidade mínima obrigatória (`id`, `source_path`, `created_at`, `metadata`).
- [x] Entidades `Chunk`, `Query` e `Answer` criadas no domínio.
- [x] Sem dependência de LangChain, Qdrant, FastAPI ou SDKs externos no domínio.
- [x] Validações básicas de invariantes adicionadas em cada entidade.
- [x] Testes unitários de domínio criados.

## Validação manual sugerida
1. `python -m unittest discover -s tests -p 'test_*.py'`
2. `python -m src.main`
