# -*- coding: utf-8 -*-
"""Audita e mede de forma reproduzível os artefatos reais e invariantes Fail-Closed deste repositório."""

import json
import re
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "skills" / "mentor-estudo-80-20" / "scripts"))
from extrair_transcricao import clean_vtt, pick_best_vtt, validate_http_url  # noqa: E402
from init_db import init_database  # noqa: E402
from security_scan import run_security_scan  # noqa: E402


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Frontmatter ausente em {skill_md}")
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def main() -> int:
    roster = json.loads((ROOT / "agents" / "roster.json").read_text(encoding="utf-8"))
    agents = roster["agents"]
    skills_dirs = sorted([d for d in (ROOT / "skills").iterdir() if d.is_dir()])

    kebab_re = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    total_skill_bytes = 0
    for sdir in skills_dirs:
        sfile = sdir / "SKILL.md"
        fm = parse_frontmatter(sfile)
        if fm.get("name") != sdir.name or not kebab_re.match(sdir.name):
            raise ValueError(f"Nome inválido em {sfile}: name={fm.get('name')!r}, pasta={sdir.name!r}")
        total_skill_bytes += sfile.stat().st_size

    # 1. Valida SQLite + VIEW Fail-Closed em memória com seed
    rows = init_database(Path(":memory:"), seed=True)
    status_map = {r[0]: r[4] for r in rows}
    assert status_map.get("PILOTO-CASE-INCOMPLETO-000") == "CONSELHO INCOMPLETO", status_map
    assert status_map.get("PILOTO-CASE-LOGIN-001") == "REPROVA", status_map

    # 2. Valida idempotência do init_db (não apaga dados existentes sem --reset) e LEFT JOIN para 0 pareceres
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "missoes.db"
        init_database(db_file, seed=True)
        conn = sqlite3.connect(str(db_file))
        conn.execute(
            "INSERT INTO missoes_empresa (codigo_missao, projeto, objetivo, estado, responsavel_atual, ultimo_evento, atualizado_em) "
            "VALUES ('MISSAO-SEM-PARECER', 'Demo', 'Validar 0 pareceres', 'Em revisão pelo Conselho', 'Conselho Independente', 'Aguardando', '2026-11-18T12:00:00Z')"
        )
        conn.commit()
        conn.close()

        # Reexecuta init_database sem reset: deve preservar MISSAO-SEM-PARECER e listá-la como CONSELHO INCOMPLETO
        rows_after = init_database(db_file, seed=True, reset=False)
        after_map = {r[0]: r for r in rows_after}
        assert "MISSAO-SEM-PARECER" in after_map, after_map
        assert after_map["MISSAO-SEM-PARECER"][2] == 0 and after_map["MISSAO-SEM-PARECER"][4] == "CONSELHO INCOMPLETO", after_map

    # 3. Valida CHECK constraints e UNIQUE por conselheiro/rodada
    conn = sqlite3.connect(":memory:")
    conn.executescript((ROOT / "sql" / "schema-missoes.sql").read_text(encoding="utf-8"))
    conn.executescript((ROOT / "examples" / "case-study-login-ratelimit" / "seed-case-study.sql").read_text(encoding="utf-8"))
    checks = {"invalid_verdict": False, "invalid_family_case": False, "duplicate_counselor": False}
    try:
        conn.execute(
            "INSERT INTO pareceres_conselho (chave_parecer, codigo_missao, rodada, conselheiro_nome, modelo_familia, veredito, achados_principais, registrado_em) "
            "VALUES ('BAD-V', 'PILOTO-CASE-LOGIN-001', 2, 'Teste', 'claude', 'INVALIDO', 'x', '2026-11-18T00:00:00Z')"
        )
    except sqlite3.IntegrityError:
        checks["invalid_verdict"] = True

    try:
        conn.execute(
            "INSERT INTO pareceres_conselho (chave_parecer, codigo_missao, rodada, conselheiro_nome, modelo_familia, veredito, achados_principais, registrado_em) "
            "VALUES ('BAD-F', 'PILOTO-CASE-LOGIN-001', 2, 'Teste', 'Claude', 'APROVA', 'x', '2026-11-18T00:00:00Z')"
        )
    except sqlite3.IntegrityError:
        checks["invalid_family_case"] = True

    try:
        conn.execute(
            "INSERT INTO pareceres_conselho (chave_parecer, codigo_missao, rodada, conselheiro_nome, modelo_familia, veredito, achados_principais, registrado_em) "
            "VALUES ('DUP-C', 'PILOTO-CASE-LOGIN-001', 1, 'Conselheiro Claude', 'gemini', 'APROVA', 'x', '2026-11-18T00:00:00Z')"
        )
    except sqlite3.IntegrityError:
        checks["duplicate_counselor"] = True
    finally:
        conn.close()
    assert all(checks.values()), f"Falha nas travas SQLite: {checks}"

    # 4. Valida segurança e parsing do extrair_transcricao.py
    for bad in ("--version", "--exec=whoami", "file:///etc/passwd", ""):
        try:
            validate_http_url(bad)
            raise AssertionError(f"URL perigosa não foi bloqueada: {bad!r}")
        except ValueError:
            pass
    proc_bad = subprocess.run(
        [sys.executable, str(ROOT / "skills" / "mentor-estudo-80-20" / "scripts" / "extrair_transcricao.py"), "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc_bad.returncode == 1, proc_bad

    vtt_sample = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nOlá\n\n00:00:02.000 --> 00:00:03.000\nOlá\n\n00:00:03.000 --> 00:00:04.000\nMundo\n\n00:00:04.000 --> 00:00:05.000\nOlá\n"
    assert clean_vtt(vtt_sample) == "Olá\nMundo\nOlá"
    assert pick_best_vtt([Path("vid.en.vtt"), Path("vid.pt.vtt")], "pt,pt-BR,en").name == "vid.pt.vtt"

    # 5. Varredura estática de segurança em 8 pontos
    scan = run_security_scan(ROOT)
    assert scan["ok"], f"Falha na varredura de segurança: {scan}"

    families = {}
    for ag in agents:
        families[ag["model_family"]] = families.get(ag["model_family"], 0) + 1

    print("=== Auditoria Reproduzível — JARVIS Agent Company ===")
    print(f"Agentes no roster.json: {len(agents)} em {len(roster['departments'])} departamentos")
    print(f"Distribuição por família: {families}")
    print(f"Core Skills válidas (kebab-case): {len(skills_dirs)} ({total_skill_bytes} bytes totais nos SKILL.md)")
    print(f"SQLite VIEW v_validacao_conselho (seed): {rows}")
    print(f"Travas SQLite validadas: {checks}")
    print(f"Varredura de segurança 8 pontos: {scan['passed']}/{scan['total']} OK ({scan['files_scanned']} arquivos)")
    print("Segurança CLI & VTT do extrair_transcricao.py: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
