# Fase 6 — Checklist de validação

## Objetivo
Adicionar observabilidade completa com LangSmith e rastreamento por versão no pipeline RAG.

## Itens
- [x] Porta de observabilidade (`ObservabilityPort`) definida na camada de aplicação.
- [x] Instrumentação de eventos do pipeline RAG (embedding, retrieval, prompt, status final).
- [x] Rastreamento por versão incluído (`prompt_version`, `model_version`, `dataset_version`).
- [x] Adapter `LangSmithObservabilityAdapter` implementado na infraestrutura.
- [x] Configuração fail-fast para tracing (`LANGCHAIN_TRACING_V2` + `LANGCHAIN_API_KEY`).
- [x] Testes cobrindo instrumentação e adapter de observabilidade.

## Validação manual sugerida
1. `python -m unittest discover -s tests -p 'test_*.py'`
2. `LANGCHAIN_TRACING_V2=true LANGCHAIN_API_KEY=<key> QDRANT_URL=http://localhost:6333 GEMINI_API_KEY=<key> python -m src.main`
