-- Schema Operacional de Missões — JARVIS Agent Company (SQLite)
-- Separa a disponibilidade do agente ("ready") do estado real da entrega
-- e aplica governança Fail-Closed para o Conselho Independente via VIEW SQL.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS missoes_empresa (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  codigo_missao TEXT NOT NULL UNIQUE,
  projeto TEXT NOT NULL,
  objetivo TEXT NOT NULL,
  versao_escopo TEXT NOT NULL DEFAULT 'v1',
  estado TEXT NOT NULL CHECK (
    estado IN (
      'Em planejamento',
      'Em execução',
      'Em revisão',
      'Em revisão pelo Conselho',
      'Aguardando decisão do CEO',
      'Bloqueada',
      'Concluída'
    )
  ),
  responsavel_atual TEXT NOT NULL,
  dependencias TEXT,
  artefatos TEXT,
  evidencias TEXT,
  aprovacoes_escopo TEXT,
  bloqueio TEXT,
  ultimo_evento TEXT NOT NULL,
  atualizado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS etapas_missao (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  chave_etapa TEXT NOT NULL UNIQUE,
  codigo_missao TEXT NOT NULL,
  ordem INTEGER NOT NULL CHECK (ordem >= 1),
  agente_nome TEXT NOT NULL,
  agente_id TEXT NOT NULL,
  papel_etapa TEXT NOT NULL,
  estado TEXT NOT NULL CHECK (
    estado IN (
      'Pendente',
      'Em execução',
      'Em revisão',
      'Bloqueada',
      'Concluída'
    )
  ),
  resumo_entrega TEXT,
  evidencia_verificada TEXT,
  atualizado_em TEXT NOT NULL,
  FOREIGN KEY (codigo_missao) REFERENCES missoes_empresa(codigo_missao) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pareceres_conselho (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  chave_parecer TEXT NOT NULL UNIQUE,
  codigo_missao TEXT NOT NULL,
  rodada INTEGER NOT NULL DEFAULT 1 CHECK (rodada >= 1),
  conselheiro_nome TEXT NOT NULL,
  modelo_familia TEXT NOT NULL CHECK (modelo_familia IN ('claude', 'gemini', 'gpt')),
  veredito TEXT NOT NULL CHECK (
    veredito IN (
      'APROVA',
      'APROVA COM RESSALVAS',
      'REPROVA',
      'INCONCLUSIVO'
    )
  ),
  achados_principais TEXT NOT NULL,
  exclusividades TEXT,
  incertezas TEXT,
  registrado_em TEXT NOT NULL,
  UNIQUE (codigo_missao, rodada, conselheiro_nome),
  FOREIGN KEY (codigo_missao) REFERENCES missoes_empresa(codigo_missao) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_missoes_estado ON missoes_empresa(estado);
CREATE INDEX IF NOT EXISTS idx_etapas_missao_ordem ON etapas_missao(codigo_missao, ordem);
CREATE INDEX IF NOT EXISTS idx_pareceres_missao_rodada ON pareceres_conselho(codigo_missao, rodada);

-- VIEW determinística: garante regra Fail-Closed (LEFT JOIN expõe missões sem parecer como CONSELHO INCOMPLETO)
CREATE VIEW IF NOT EXISTS v_validacao_conselho AS
SELECT
  m.codigo_missao,
  COALESCE(p.rodada, 1) AS rodada,
  COUNT(p.id) AS total_pareceres,
  COUNT(DISTINCT lower(trim(p.modelo_familia))) AS familias_distintas,
  CASE
    WHEN COUNT(p.id) < 2 OR COUNT(DISTINCT lower(trim(p.modelo_familia))) < 2 THEN 'CONSELHO INCOMPLETO'
    WHEN SUM(CASE WHEN p.veredito = 'REPROVA' THEN 1 ELSE 0 END) > 0 THEN 'REPROVA'
    WHEN SUM(CASE WHEN p.veredito = 'INCONCLUSIVO' THEN 1 ELSE 0 END) > 0 THEN 'INCONCLUSIVO'
    WHEN SUM(CASE WHEN p.veredito = 'APROVA COM RESSALVAS' THEN 1 ELSE 0 END) > 0 THEN 'APROVA COM RESSALVAS'
    ELSE 'APROVA'
  END AS status_consolidado
FROM missoes_empresa m
LEFT JOIN pareceres_conselho p ON p.codigo_missao = m.codigo_missao
GROUP BY m.codigo_missao, COALESCE(p.rodada, 1);
