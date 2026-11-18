# -*- coding: utf-8 -*-
"""Extrai legendas/transcrição em texto limpo de um vídeo público usando yt-dlp (sem baixar o arquivo de vídeo)."""

import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse


def validate_http_url(url: str) -> str:
    """Garante que a URL seja http(s) válida e nunca comece com '-' (evita injeção de opções CLI)."""
    cleaned = url.strip()
    if not cleaned or cleaned.startswith("-"):
        raise ValueError("URL inválida: não pode ser vazia nem iniciar com '-'.")
    parsed = urlparse(cleaned)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("URL inválida: informe uma URL completa começando com http:// ou https://.")
    return cleaned


def clean_vtt(raw: str) -> str:
    """Remove metadados/timestamps VTT e deduplica apenas repetições consecutivas."""
    lines: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:")) or "-->" in line or line.isdigit():
            continue
        text = re.sub(r"<[^>]+>", "", line).strip()
        if text and (not lines or text != lines[-1]):
            lines.append(text)
    return "\n".join(lines)


def pick_best_vtt(vtts: list[Path], langs: str) -> Path:
    """Seleciona o arquivo .vtt respeitando a ordem de prioridade solicitada em `langs`."""
    ordered_langs = [lang.strip().lower() for lang in langs.split(",") if lang.strip()]
    for lang in ordered_langs:
        suffix = f".{lang}.vtt"
        for candidate in vtts:
            if candidate.name.lower().endswith(suffix):
                return candidate
    return vtts[0]


def main() -> int:
    if len(sys.argv) < 2:
        print("Uso: python extrair_transcricao.py <URL_DO_VIDEO> [idioma=pt,pt-BR,en]", file=sys.stderr)
        return 1

    try:
        url = validate_http_url(sys.argv[1])
    except ValueError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    langs = sys.argv[2] if len(sys.argv) > 2 else "pt,pt-BR,en"

    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            langs,
            "--sub-format",
            "vtt",
            "-o",
            str(Path(tmpdir) / "%(id)s.%(ext)s"),
            "--",
            url,
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        except FileNotFoundError:
            print("Erro: 'yt-dlp' não encontrado no PATH. Instale com: pip install yt-dlp", file=sys.stderr)
            return 3

        vtts = sorted(Path(tmpdir).glob("*.vtt"))
        if not vtts:
            print(f"Nenhuma legenda encontrada (exit={proc.returncode}). {proc.stderr.strip()}", file=sys.stderr)
            return 2

        chosen = pick_best_vtt(vtts, langs)
        cleaned = clean_vtt(chosen.read_text(encoding="utf-8", errors="replace"))
        print(cleaned)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
