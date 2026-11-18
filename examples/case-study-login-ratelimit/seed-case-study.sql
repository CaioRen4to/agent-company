-- Seed reproduzível para o estudo de caso do Conselho Independente
-- Demonstra duas situações na VIEW v_validacao_conselho:
--   1) PILOTO-CASE-INCOMPLETO-000 -> 1 único parecer -> 'CONSELHO INCOMPLETO' (Fail-Closed)
--   2) PILOTO-CASE-LOGIN-001      -> 2 famílias distintas -> 'REPROVA'

INSERT OR IGNORE INTO missoes_empresa (
  codigo_missao, projeto, objetivo, versao_escopo, estado, responsavel_atual,
  dependencias, artefatos, evidencias, aprovacoes_escopo, bloqueio, ultimo_evento, atualizado_em
) VALUES
(
  'PILOTO-CASE-INCOMPLETO-000',
  'Auth Security Demo',
  'Demonstrar trava Fail-Closed quando apenas 1 família responde ao Conselho',
  'v1',
  'Bloqueada',
  'Conselho Independente',
  'Nenhuma',
  'examples/case-study-login-ratelimit/prompt-rodada-cega.md',
  'Apenas 1 parecer registrado — bloqueio automático esperado',
  'Somente leitura',
  'CONSELHO INCOMPLETO: falta parecer da segunda família',
  'Registrado 1 de 2 pareceres para teste Fail-Closed',
  '2026-11-18T12:00:00Z'
),
(
  'PILOTO-CASE-LOGIN-001',
  'Auth Security Demo',
  'Avaliar proposta de elevar limite de login de 5 para 10 tentativas',
  'v1',
  'Bloqueada',
  'JARVIS — Maestro',
  'Nenhuma',
  'examples/case-study-login-ratelimit/prompt-rodada-cega.md',
  'Convergência REPROVA em 5 achados estruturais',
  'Somente leitura',
  'Proposta reprovada pelo Conselho por ausência de escopo, janela, backoff e monitoramento',
  'Conselho convergiu em REPROVA na 1a rodada cega',
  '2026-11-18T12:05:00Z'
);

INSERT OR IGNORE INTO pareceres_conselho (
  chave_parecer, codigo_missao, rodada, conselheiro_nome, modelo_familia,
  veredito, achados_principais, exclusividades, incertezas, registrado_em
) VALUES
(
  'PILOTO-INCOMPLETO-R1-CLAUDE',
  'PILOTO-CASE-INCOMPLETO-000',
  1,
  'Conselheiro Claude',
  'claude',
  'APROVA',
  'Registro unitário para validar que a VIEW v_validacao_conselho bloqueia aprovação sem segunda família.',
  'Nenhuma',
  'Falta parecer da família Gemini.',
  '2026-11-18T12:00:00Z'
),
(
  'PILOTO-LOGIN-R1-CLAUDE',
  'PILOTO-CASE-LOGIN-001',
  1,
  'Conselheiro Claude',
  'claude',
  'REPROVA',
  'Falta escopo (IP/conta), janela temporal, duração do bloqueio, backoff/CAPTCHA e logs de monitoramento.',
  'Verificação HIBP, limite/MFA específico para administradores e testes automatizados.',
  'Não foi enviado código da rota de login.',
  '2026-11-18T12:05:00Z'
),
(
  'PILOTO-LOGIN-R1-GEMINI',
  'PILOTO-CASE-LOGIN-001',
  1,
  'Conselheiro Gemini',
  'gemini',
  'REPROVA',
  'Falta escopo (IP/conta), janela temporal, ação de bloqueio, controles compensatórios e alertas.',
  'Risco de bloqueio intencional de contas alheias (Account Lockout DoS) sem desbloqueio por e-mail/MFA.',
  'Não foi informada a taxa atual de chamados de suporte.',
  '2026-11-18T12:05:00Z'
);
