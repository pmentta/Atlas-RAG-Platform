# Atlas-RAG-Platform

Plataforma de Retrieval-Augmented Generation (RAG) construída incrementalmente com foco em arquitetura limpa, observabilidade e avaliação automatizada.

## Status atual

- Fase concluída: **Fase 0 — Planejamento técnico (sem código)**.
- Fase concluída: **Fase 1 — Fundação do projeto**.
- Fase concluída: **Fase 2 — Modelo de domínio**.
- Fase ativa: **Fase 3 — Vector Store (Qdrant)**.
- Plano técnico oficial: `docs/technical-plan.md`.
- Checklist da fase atual: `docs/phase-3-checklist.md`.

## Execução local

```bash
python -m pip install -e .
python -m unittest discover -s tests -p 'test_*.py'
QDRANT_URL=http://localhost:6333 python -m src.main
```
