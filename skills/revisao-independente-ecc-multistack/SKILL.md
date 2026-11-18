---
name: revisao-independente-ecc-multistack
description: Procedimento de revisão de código, contratos, falhas silenciosas, segurança defensiva e rubrica de aceite para Python, FastAPI, TypeScript, React e PostgreSQL. Use antes de aprovar entregas técnicas.
---

# revisao-independente-ecc-multistack

Consolida os procedimentos de `code-reviewer`, `python-reviewer`, `fastapi-reviewer`, `typescript-reviewer`, `react-reviewer`, `database-reviewer`, `silent-failure-hunter` e `agent-evaluator`.

## 1. Regras gerais de revisão
- Analise apenas evidências reais (diff, arquivos citados, logs de teste e critérios da missão).
- Todo apontamento deve conter: **arquivo e linha**, **gravidade** (`CRÍTICO`, `ALTO`, `MÉDIO`, `BAIXO`), **evidência do problema** e **correção concreta recomendada**.
- Não aprove por suposição quando testes obrigatórios não foram executados.

## 2. Checklist por tecnologia
- **Python / FastAPI / Flask:** validação de entrada (Pydantic/schemas), tratamento explícito de exceções, fechamento de conexões/transações, tipagem, ausência de segredos hardcoded e autenticação/autorização por rota.
- **TypeScript / React:** tipagem estrita (sem `any` silencioso), dependências corretas em hooks, tratamento de estados de carregamento/erro/vazio, acessibilidade (teclado, semântica, ARIA) e prevenção de re-renders desnecessários.
- **PostgreSQL / Supabase / SQLite:** queries parametrizadas (zero interpolação de strings), chaves estrangeiras (`FOREIGN KEY`), constraints (`CHECK`), índices em FKs e filtros frequentes, políticas RLS quando aplicável e plano de rollback para migrações.
- **Caça a Falhas Silenciosas (Silent Failure Hunter):** proibir blocos `try/except` ou `.catch()` vazios, retornos `null`/`false` que escondem erro de infraestrutura e fallbacks que mascaram dados corrompidos.

## 3. Rubrica de Aceite (Veredito)
Finalize sempre com um veredito explícito:
- `APROVADO`: todos os critérios de aceite cumpridos e sem achados críticos ou altos.
- `APROVADO COM RESSALVAS`: funcional e seguro, com melhorias não bloqueantes registradas.
- `REPROVADO`: falha funcional, risco de segurança, falha silenciosa ou critério obrigatório ausente.
