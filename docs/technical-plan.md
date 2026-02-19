# Atlas RAG Platform — Fase 0 (Planejamento Técnico)

## 1) Resumo do que será feito
Esta fase define **o contrato arquitetural** e os limites de implementação antes de qualquer código. O objetivo é estabelecer uma base técnica defensável para evolução incremental do projeto, com foco em:

- RAG factual single-hop para documentos TXT.
- Clean Architecture estrita (Domain → Application → Infrastructure/Interfaces por inversão de dependência).
- Observabilidade obrigatória (LangSmith) e avaliação obrigatória (RAGAS), sem tratá-las como opcionais.
- Vetor store inicial obrigatório: Qdrant local via Docker.
- LLM inicial: Gemini, com preparação de extensibilidade para fallback em IA local.

---

## 2) Definições validadas de escopo (Fase 0)

### 2.1 Tipo de RAG inicial
- **Tipo**: QA factual, **single-hop**.
- **Justificativa**: reduz complexidade inicial, facilita mensuração de recuperação e grounding, e melhora depuração de falhas.
- **Não entra agora**: multi-hop, agentes, roteamento entre múltiplas bases, e workflows autônomos.

### 2.2 Domínio documental inicial
- **Formato suportado inicialmente**: **TXT apenas**.
- **Fonte dos arquivos**: pasta na raiz do projeto (fornecida posteriormente).
- **Não entra agora**: PDF/MD/HTML, OCR e parsing avançado.

### 2.3 Modelo e provedores
- **LLM principal inicial**: **Gemini**.
- **Diretriz de extensibilidade**: design deve permitir fallback para IA local sem quebrar casos de uso.
- **Não entra agora**: implementação do fallback local; apenas preparação arquitetural (porta/contrato).

### 2.4 Vector Store
- **Obrigatório nesta iteração**: **Qdrant local via Docker**.
- **Diretriz**: criar abstração desde o início, porém com **uma única implementação concreta por fase**.

---

## 3) Escopo funcional inicial (in/out)

### 3.1 Entra no MVP arquitetural (por fases posteriores)
1. Ingestão de arquivos TXT.
2. Chunking configurável.
3. Indexação vetorial no Qdrant.
4. Recuperação Top-K.
5. Geração de resposta com fontes.
6. Rastreamento de execução (LangSmith).
7. Avaliação automatizada (RAGAS).

### 3.2 Fica explicitamente fora por enquanto
1. Interface web.
2. Autenticação/autorização multiusuário.
3. Pipelines multi-tenant.
4. Estratégias de reranking avançadas.
5. Fine-tuning de modelo.
6. Otimizações prematuras (cache distribuído, sharding etc.).

---

## 4) Riscos e decisões críticas

## 4.1 Riscos arquiteturais já identificados
1. **Acoplamento indevido ao framework de IA**
   - Risco: permitir que LangChain (ou SDKs) vaze para Domain/Application.
   - Mitigação: dependências concretas restritas à Infrastructure; Application depende apenas de portas.

2. **Observabilidade tratada como “extra”**
   - Risco: falta de rastreabilidade e baixa capacidade de diagnóstico.
   - Mitigação: definir requisitos mínimos de tracing/logging como critério de aceite de fase.

3. **Avaliação adiada indefinidamente**
   - Risco: produto vira demo sem mensuração objetiva.
   - Mitigação: reservar fases explícitas com critérios verificáveis para RAGAS e Promptfoo.

4. **Lock-in em provedor de LLM**
   - Risco: mudança de custo/latência sem alternativa.
   - Mitigação: contrato de gateway de geração já orientado a múltiplos providers.

5. **Chunking sem governança de qualidade**
   - Risco: baixa recall/precision e respostas não fundamentadas.
   - Mitigação: tornar chunk size/overlap parâmetros explícitos e avaliáveis por dataset.

6. **Logs inseguros com dados sensíveis**
   - Risco: vazamento de credenciais/dados.
   - Mitigação: mascaramento obrigatório de segredos e política de logs sem payload sensível bruto.

## 4.2 Alertas críticos (gate de avanço)
A progressão deve ser interrompida se ocorrer qualquer uma das situações abaixo:
- Domain contendo imports de frameworks externos.
- Falta de rastreamento mínimo por execução após fase de observabilidade.
- Ausência de baseline de métricas após fase de avaliação.
- Expansão de escopo sem validação humana explícita.

---

## 5) Trade-offs conscientes
1. **Single-hop primeiro vs. arquitetura para casos complexos**
   - Escolha: começar simples para garantir qualidade mensurável.
   - Trade-off: limita alguns casos avançados no curto prazo.

2. **Qdrant obrigatório vs. múltiplos stores na largada**
   - Escolha: uma implementação concreta por fase para reduzir complexidade operacional.
   - Trade-off: menos comparabilidade inicial entre stores.

3. **TXT-only inicial vs. suporte multimodal imediato**
   - Escolha: reduzir variabilidade de parsing para validar pipeline base.
   - Trade-off: cobertura de fontes limitada no início.

4. **Gemini primeiro vs. benchmark multi-modelo imediato**
   - Escolha: foco operacional inicial, mantendo contrato para fallback local.
   - Trade-off: benchmark comparativo completo fica para fases posteriores.

---

## 6) Critérios de aceite por fase (0 → 10)

## Fase 0 — Planejamento técnico (SEM CÓDIGO)
- Documento formal de escopo, riscos, trade-offs e critérios concluído.
- Aprovação humana explícita para avançar.

## Fase 1 — Fundação do projeto
- Estrutura base em camadas criada.
- Configuração de ambiente e logging estruturado.
- Projeto executa “vazio” com sucesso.

## Fase 2 — Modelo de domínio
- Entidades puras: `Document`, `Chunk`, `Query`, `Answer`.
- Zero dependências externas no domínio.

## Fase 3 — Vector Store (um)
- `VectorStorePort` definido.
- Adapter de Qdrant funcional local.
- Sem pipeline RAG completo.

## Fase 4 — Ingestão
- Loader TXT funcional.
- Chunking configurável.
- Indexação vetorial concluída.

## Fase 5 — RAG mínimo
- Retriever + prompt + geração integrados.
- Resposta inclui fontes.

## Fase 6 — Observabilidade
- LangSmith integrado ponta a ponta.
- Traces com versionamento (prompt/modelo) e metadados essenciais.

## Fase 7 — Avaliação
- Dataset versionado.
- Execução RAGAS com métricas mínimas (faithfulness, relevancy, context recall/precision).
- Export de resultados.

## Fase 8 — Testes de Prompt
- Promptfoo configurado.
- Comparações reprodutíveis entre variantes.

## Fase 9 — API
- Endpoints mínimos (`/ingest`, `/query`, `/health`) com contratos claros.
- Tratamento explícito de erros e logs estruturados.

## Fase 10 — Deploy
- Dockerfile(s) e Docker Compose funcionais.
- Stack local reprodutível com Qdrant.

---

## 7) Plano de configuração de ferramentas externas (preparatório)

> Esta seção é propositalmente instrucional para evitar bloqueios nas fases de implementação.

## 7.1 LangSmith (quando chegar na fase correspondente)
1. Criar conta em https://smith.langchain.com/.
2. Gerar API Key no painel.
3. Definir variáveis de ambiente:
   - `LANGCHAIN_TRACING_V2=true`
   - `LANGCHAIN_API_KEY=<sua_chave>`
   - `LANGCHAIN_PROJECT=atlas-rag-platform`
4. Validar recebimento de traces com uma execução controlada.

## 7.2 Qdrant local via Docker (fase de vector store)
1. Instalar Docker e Docker Compose.
2. Subir Qdrant:
   - `docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant`
3. Verificar health endpoint local (`http://localhost:6333`).
4. Parametrizar URL em variável de ambiente (`QDRANT_URL`).

## 7.3 Gemini API (fase de geração)
1. Criar/usar conta Google AI Studio.
2. Gerar API Key do Gemini.
3. Configurar variável de ambiente (`GEMINI_API_KEY`).
4. Garantir que chave nunca seja logada nem comitada.

---

## 8) O que conscientemente NÃO será implementado nesta fase
- Qualquer arquivo de código-fonte.
- Criação de diretórios de runtime da aplicação.
- Integrações reais com Qdrant, Gemini ou LangSmith.
- Testes de execução de pipeline.

Esta fase é exclusivamente de planejamento técnico e governança de arquitetura.

---

## 9) Próximo passo sugerido (após aprovação humana)
- Iniciar **Fase 1** com escopo estrito:
  1. estrutura base de pastas da Clean Architecture;
  2. configuração de ambiente;
  3. logging estruturado;
  4. execução “vazia” validável.

Sem avançar para domínio, vector store ou ingestão na mesma entrega.
