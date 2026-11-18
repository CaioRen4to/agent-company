---
name: obsidian-triagem
description: Recupera contexto seletivo de um cofre Obsidian com baixo consumo de tokens. Use antes de tarefas sobre projetos, preferências, arquitetura, agentes ou decisões anteriores.
---

# obsidian-triagem

Protocolo de leitura seletiva para evitar carregar notas inteiras na janela de contexto antes de saber o que é relevante.

## Passos

1. Leia primeiro o manifesto ou índice do projeto no cofre (`<OBSIDIAN_VAULT>/00-Hub-Memoria/context-manifest.json` ou `00-INDICE.md`).
2. Use `entries`, resumos e caminhos para abrir **apenas** as notas diretamente ligadas ao pedido.
3. Para trabalho de um especialista, leia somente `00-INDICE.md` e `01-CONTEXTO.md`; abra `02-ARQUITETURA.md`, `03-DECISOES.md`, `04-PENDENCIAS.md` ou `05-TESTES.md` apenas se a tarefa exigir.
4. Resolva links internos contra a raiz `<OBSIDIAN_VAULT>` somente quando faltar contexto essencial.
5. Compare sempre as notas com o código e o estado atual do repositório; o código atual prevalece sobre notas antigas.
6. Nunca leia ou reproduza arquivos `.env`, credenciais, chaves de API ou notas fora do escopo.
7. Cite quais notas influenciaram decisões materiais.
