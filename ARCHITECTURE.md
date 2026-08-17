# AEON 1.0: arquitetura adotada

## Núcleo ativo

| Componente | Função | Estado |
|---|---|---|
| LangGraph | Estado persistente, retomada, checkpoints e human-in-the-loop | Validado |
| Langfuse | Traces, prompts, custos e observabilidade principal | Validado |
| Promptfoo | Testes de prompts, regressões e segurança | CLI validado |
| Mem0 | Memória de longo prazo local | Validado com Ollama + Qdrant |
| Ruff | Lint e formatação Python | Validado |

## Não duplicar agora

- OpenLIT não será instalado: cobre observabilidade que já está atendida pelo Langfuse.
- Temporal não será instalado nesta fase: LangGraph com checkpoints atende a operação atual.

## Critério para reabrir a decisão

Reavaliar OpenLIT se houver necessidade de OpenTelemetry/guardrails que o Langfuse não cubra.
Reavaliar Temporal quando existirem workflows distribuídos longos, com workers independentes e necessidade de garantia de execução além do checkpoint local.
