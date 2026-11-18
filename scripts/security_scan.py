# -*- coding: utf-8 -*-
"""Varredura estática de segurança em 8 pontos para skills, scripts e templates do repositório."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ALLOWED_EXTENSIONS = {
    ".md",
    ".py",
    ".ps1",
    ".sh",
    ".sql",
    ".json",
    ".svg",
    ".html",
    ".yml",
    ".yaml",
    ".txt",
    "",
}

IGNORE_DIRS = {".git", "__pycache__", "data", ".venv", "venv", "node_modules"}

DANGEROUS_PATTERNS = [
    ("subprocess com shell=True", re.compile(r"shell\s*=\s*True")),
    ("execução via os.system", re.compile(r"\bos\.system\s*\(")),
    ("Invoke-Expression / iex", re.compile(r"\bInvoke-Expression\b|\biex\b")),
    ("pipe remoto para shell", re.compile(r"(?:curl|wget)\s+[^|\n]+\|\s*(?:sh|bash|pwsh|powershell)")),
    ("remoção recursiva raiz", re.compile(r"rm\s+-rf\s+/(?:\s|$)")),
]

SECRET_PATTERNS = [
    ("chave OpenAI/Anthropic", re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("token GitHub", re.compile(r"\b(?:ghp|ghu|ghs|gho|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("chave Google AI", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("chave privada PEM", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
]

ENV_READ_PATTERNS = [
    ("leitura direta de os.environ/getenv", re.compile(r"\bos\.(?:environ|getenv)\b")),
    ("leitura direta de $env: no PowerShell", re.compile(r"\$env:[A-Za-z_][A-Za-z0-9_]*")),
]

NETWORK_PATTERNS = [
    ("cliente HTTP/rede em script", re.compile(r"\b(?:urllib\.request|requests\.(?:get|post)|httpx\.|Invoke-WebRequest|Invoke-RestMethod)\b")),
]

OBFUSCATION_PATTERNS = [
    ("execução de payload base64", re.compile(r"base64\s+(?:-d|--decode)\s*\|\s*(?:sh|bash|python)|FromBase64String")),
    ("execução dinâmica eval(compile(...))", re.compile(r"\beval\s*\(\s*compile\s*\(|\bexec\s*\(\s*base64")),
]

INJECTION_PATTERNS = [
    ("override de instruções", re.compile(r"ignore\s+(?:all\s+)?previous\s+instructions|disregard\s+system\s+prompt", re.IGNORECASE)),
    ("caractere bidi/zero-width oculto", re.compile(r"[\u200b\u200c\u200d\u202a-\u202e\u2066-\u2069]")),
]


def iter_repo_files(base: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(base.rglob("*")):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def scan_patterns(
    files: list[Path],
    patterns: list[tuple[str, re.Pattern[str]]],
    *,
    only_suffixes: set[str] | None = None,
    exclude_paths: set[str] | None = None,
) -> list[str]:
    findings: list[str] = []
    for fpath in files:
        rel = fpath.relative_to(ROOT).as_posix()
        if exclude_paths and rel in exclude_paths:
            continue
        if only_suffixes and fpath.suffix.lower() not in only_suffixes:
            continue
        try:
            text = fpath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"{rel}: arquivo não UTF-8 / binário inesperado")
            continue
        for label, rx in patterns:
            if rx.search(text):
                findings.append(f"{rel}: {label}")
    return findings


def run_security_scan(base: Path = ROOT) -> dict[str, object]:
    files = iter_repo_files(base)
    self_rel = "scripts/security_scan.py"
    bench_rel = "bench/measure_repo.py"
    code_suffixes = {".py", ".ps1", ".sh"}
    md_suffixes = {".md"}

    # 1. Estrutura e tipos de arquivo permitidos
    bad_types = [
        f"{p.relative_to(ROOT).as_posix()}: extensão não permitida ({p.suffix or 'sem extensão'})"
        for p in files
        if p.name not in {"LICENSE", ".gitignore"} and p.suffix.lower() not in ALLOWED_EXTENSIONS
    ]

    # 2. Comandos perigosos em scripts (ignora definições de regex no próprio scanner)
    dangerous = scan_patterns(files, DANGEROUS_PATTERNS, only_suffixes=code_suffixes, exclude_paths={self_rel})

    # 3. Segredos hardcoded em todo o repositório
    secrets = scan_patterns(files, SECRET_PATTERNS, exclude_paths={self_rel})

    # 4. Leitura de variáveis de ambiente em skills/scripts
    skill_scripts = [p for p in files if p.relative_to(ROOT).as_posix().startswith(("skills/", "scripts/"))]
    env_reads = scan_patterns(skill_scripts, ENV_READ_PATTERNS, only_suffixes=code_suffixes, exclude_paths={self_rel})

    # 5. Acesso de rede não declarado em scripts de skills/scripts
    network_calls = scan_patterns(skill_scripts, NETWORK_PATTERNS, only_suffixes=code_suffixes, exclude_paths={self_rel})

    # 6. Código ofuscado
    obfuscated = scan_patterns(files, OBFUSCATION_PATTERNS, only_suffixes=code_suffixes, exclude_paths={self_rel})

    # 7. Prompt injection / Unicode oculto em Markdown e skills
    injections = scan_patterns(files, INJECTION_PATTERNS, only_suffixes=md_suffixes, exclude_paths={self_rel})

    # 8. Integridade CLI (extrair_transcricao.py deve exigir validação de URL e usar '--')
    extractor = ROOT / "skills" / "mentor-estudo-80-20" / "scripts" / "extrair_transcricao.py"
    cli_issues: list[str] = []
    if not extractor.exists():
        cli_issues.append("extrair_transcricao.py ausente")
    else:
        ext_text = extractor.read_text(encoding="utf-8")
        if '"--"' not in ext_text or "validate_http_url" not in ext_text:
            cli_issues.append("extrair_transcricao.py sem trava '--' ou validate_http_url")
    # Verifica também que scripts não contêm path traversal literal '../' em alvos de escrita
    for p in skill_scripts:
        rel = p.relative_to(ROOT).as_posix()
        if rel in {self_rel, bench_rel} or p.suffix.lower() not in code_suffixes:
            continue
        if "../" in p.read_text(encoding="utf-8"):
            cli_issues.append(f"{rel}: possível traversal literal '../'")

    checks = [
        {"id": 1, "name": "Estrutura e tipos de arquivo", "passed": not bad_types, "findings": bad_types},
        {"id": 2, "name": "Comandos perigosos", "passed": not dangerous, "findings": dangerous},
        {"id": 3, "name": "Segredos no código", "passed": not secrets, "findings": secrets},
        {"id": 4, "name": "Leitura de variáveis de ambiente", "passed": not env_reads, "findings": env_reads},
        {"id": 5, "name": "Acesso de rede em scripts", "passed": not network_calls, "findings": network_calls},
        {"id": 6, "name": "Código ofuscado", "passed": not obfuscated, "findings": obfuscated},
        {"id": 7, "name": "Prompt injection e Unicode oculto", "passed": not injections, "findings": injections},
        {"id": 8, "name": "Integridade CLI e validação de URL", "passed": not cli_issues, "findings": cli_issues},
    ]

    passed_count = sum(1 for c in checks if c["passed"])
    return {
        "files_scanned": len(files),
        "passed": passed_count,
        "total": len(checks),
        "ok": passed_count == len(checks),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Varredura estática de segurança em 8 pontos.")
    parser.add_argument("--json", action="store_true", help="Imprime o relatório em JSON.")
    args = parser.parse_args()

    report = run_security_scan(ROOT)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"=== Varredura de Segurança 8 Pontos ({report['files_scanned']} arquivos) ===")
        for chk in report["checks"]:  # type: ignore[union-attr]
            mark = "OK" if chk["passed"] else "FALHA"
            print(f"[{mark}] {chk['id']}/8 {chk['name']}")
            for item in chk["findings"]:
                print(f"   - {item}")
        print(f"Resultado: {report['passed']}/{report['total']} checks aprovados")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
