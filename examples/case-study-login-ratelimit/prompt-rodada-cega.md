# Prompt da 1ª Rodada Cega — Estudo de Caso: Alteração de Limite de Login

**Missão:** `PILOTO-CASE-LOGIN-001`  
**Regra da rodada:** Nenhum conselheiro visualiza o parecer do outro na 1ª rodada.

---

## Pacote Enviado ao Conselho (`Conselheiro Claude` + `Conselheiro Gemini`)

1. **Proposta sob avaliação:** Alterar o limite máximo de tentativas de login malsucedidas na rota `POST /api/auth/login` de **5 tentativas** para **10 tentativas** antes de qualquer bloqueio.
2. **Contexto informado:** A mudança foi sugerida para reduzir chamados de usuários que erram a senha algumas vezes seguidas. Não foram informados escopo do contador (IP vs. conta), janela de tempo, duração de bloqueio, *backoff*, CAPTCHA, MFA ou alertas de monitoramento.
3. **Critérios de avaliação:**
   - Emitir veredito explícito (`APROVA`, `APROVA COM RESSALVAS`, `REPROVA` ou `INCONCLUSIVO`).
   - Listar achados técnicos de segurança, evidência e correção recomendada.
   - Apontar riscos não cobertos pela proposta.
