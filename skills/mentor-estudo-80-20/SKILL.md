---
name: mentor-estudo-80-20
description: Protocolo de aprendizagem ativa para Engenharia de Software e Engenharia de IA: revisa tarefas/códigos como mentor, aplica a regra 80/20 em vídeos extensos e gera perguntas de verificação e exercícios práticos.
---

# mentor-estudo-80-20

Use este procedimento sempre que o usuário pedir revisão didática de uma tarefa/código, estudo guiado em Engenharia de Software ou IA, ou destilação 80/20 de vídeos longos e documentações técnicas.

## 1. Revisão Didática de Tarefa ou Código
1. **O que acertou:** valide as boas decisões técnicas tomadas na tarefa.
2. **O porquê das melhorias:** explique cada ajuste conceitual (complexidade, arquitetura, segurança, contratos ou trade-offs) sem apenas entregar código pronto.
3. **Mapa conceitual curto:** conecte a tarefa atual aos fundamentos de Engenharia de Software / Engenharia de IA.

## 2. Destilação 80/20 de Vídeos Extensos
Quando receber uma URL de vídeo (ex.: YouTube) ou transcrição longa:
1. Extraia a transcrição/legendas sem baixar o vídeo pesado (ex.: `python scripts/extrair_transcricao.py <URL>` usando `yt-dlp`).
2. Se a transcrição for grande, indexe/consulte em sandbox (ex.: `context-mode`) para não desperdiçar janela de contexto.
3. Entregue a síntese seguindo estritamente a **Regra 80/20**:
   - **Os 20% essenciais que geram 80% do resultado:** conceitos centrais, arquitetura, decisões práticas e armadilhas reais.
   - **O que pode ignorar com segurança:** introdução, repetição e detalhes secundários.

## 3. Verificação Ativa e Prática Autônoma
Feche toda sessão de estudo com:
- **3 a 5 Perguntas de Verificação Ativa (*Active Recall*):** perguntas abertas ou de cenário para o usuário responder e testar o entendimento antes de ver o gabarito.
- **1 a 2 Mini-Atividades Práticas:** exercícios curtos e verificáveis para o usuário praticar por conta própria e depois trazer para correção comentada.
- **Registro opcional de estudo:** consolidar aprendizados duradouros no Obsidian (via `Pena`, sem segredos).
