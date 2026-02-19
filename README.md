# Atlas-RAG-Platform

Plataforma de Retrieval-Augmented Generation (RAG) construída incrementalmente com foco em arquitetura limpa, observabilidade e avaliação automatizada.

## Status atual

- Fase concluída: **Fase 0 — Planejamento técnico (sem código)**.
- Fase concluída: **Fase 1 — Fundação do projeto**.
- Fase concluída: **Fase 2 — Modelo de domínio**.
- Fase concluída: **Fase 3 — Vector Store (Qdrant)**.
- Fase concluída: **Fase 5 — Pipeline RAG mínimo**.
- Fase ativa: **Fase 6 — Observabilidade (LangSmith)**.
- Plano técnico oficial: `docs/technical-plan.md`.
- Checklist da fase atual: `docs/phase-6-checklist.md`.

## Execução local

```bash
python -m pip install -e .
python -m unittest discover -s tests -p 'test_*.py'
```

## Base de conhecimento

Use a pasta `knowledge_base/` para inserir os arquivos `.txt` que serão usados nas próximas etapas de ingestão.
