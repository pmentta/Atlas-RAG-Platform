# Fase 1 — Checklist de validação

## Objetivo
Garantir a fundação do projeto com Clean Architecture, configuração de ambiente e logging estruturado, sem implementar domínio de negócio.

## Itens
- [x] Estrutura de pastas em camadas criada (`src/domain`, `src/application`, `src/infrastructure`, `src/interfaces`).
- [x] Arquivo `.env.example` criado com variáveis iniciais e placeholders para fases futuras.
- [x] Bootstrap executável em `src/main.py`.
- [x] Logging estruturado configurável (JSON/texto).
- [x] Erros de configuração tratados com exceção específica (`SettingsError`).

## Validação manual sugerida
1. `python -m src.main`
2. `LOG_LEVEL=INVALID python -m src.main` (deve falhar de forma explícita)
