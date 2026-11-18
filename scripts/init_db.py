# -*- coding: utf-8 -*-
"""Inicializa o banco SQLite de governança de missões e valida a trava Fail-Closed do Conselho."""

import argparse
import sqlite3
from pathlib import Path


def init_database(db_path: Path, seed: bool = False, reset: bool = False) -> list[tuple]:
    """Aplica o schema de forma idempotente; só apaga banco existente quando reset=True."""
    root = Path(__file__).resolve().parent.parent
    schema_sql = (root / "sql" / "schema-missoes.sql").read_text(encoding="utf-8")

    if db_path != Path(":memory:"):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        if reset and db_path.exists():
            db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    try:
        conn.executescript(schema_sql)
        if seed:
            seed_sql = (root / "examples" / "case-study-login-ratelimit" / "seed-case-study.sql").read_text(encoding="utf-8")
            conn.executescript(seed_sql)
        rows = conn.execute(
            "SELECT codigo_missao, rodada, total_pareceres, familias_distintas, status_consolidado "
            "FROM v_validacao_conselho ORDER BY codigo_missao, rodada"
        ).fetchall()
        conn.commit()
        return rows
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Inicializa SQLite da JARVIS Agent Company.")
    parser.add_argument("--db", default="data/missoes.db", help="Caminho do arquivo SQLite (ou :memory:).")
    parser.add_argument("--seed", action="store_true", help="Carrega o estudo de caso do Conselho para demonstração.")
    parser.add_argument("--reset", action="store_true", help="Apaga e recria um banco existente (exige confirmação).")
    parser.add_argument("--yes", action="store_true", help="Confirma --reset sem prompt interativo.")
    args = parser.parse_args()

    db_target = Path(":memory:") if args.db == ":memory:" else Path(args.db)
    if args.reset and db_target != Path(":memory:") and db_target.exists() and not args.yes:
        resp = input(f"ATENÇÃO: '{db_target}' será apagado e recriado. Continuar? [s/N]: ").strip().lower()
        if resp not in {"s", "sim", "y", "yes"}:
            print("Operação cancelada. Nenhum dado foi alterado.")
            return 1

    rows = init_database(db_target, seed=args.seed, reset=args.reset)
    print(f"Schema aplicado com sucesso em: {args.db}")
    if args.seed:
        print("Resultado da VIEW v_validacao_conselho:")
        for row in rows:
            print(" ", row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
