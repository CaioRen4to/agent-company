#!/usr/bin/env bash
set -euo pipefail

FORCE=0
TARGET_DIR="$HOME/.claude/skills"

for arg in "$@"; do
  case "$arg" in
    --force|-f)
      FORCE=1
      ;;
    *)
      TARGET_DIR="$arg"
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"

if [ ! -d "$SKILLS_SRC" ]; then
  echo "Erro: diretório de skills não encontrado em $SKILLS_SRC" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

installed=0
skipped=0
for skill_dir in "$SKILLS_SRC"/*/; do
  skill_clean="${skill_dir%/}"
  skill_name="$(basename "$skill_clean")"
  dest="${TARGET_DIR:?}/$skill_name"
  if [ -e "$dest" ]; then
    if [ "$FORCE" -ne 1 ]; then
      echo "[AVISO] Skill já existe e foi preservada (use --force para sobrescrever): $dest" >&2
      skipped=$((skipped + 1))
      continue
    fi
    rm -rf "$dest"
  fi
  cp -R "$skill_clean" "$dest"
  find "$dest" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
  find "$dest" -type f -name "*.pyc" -delete 2>/dev/null || true
  echo "[OK] Skill instalada: $skill_name -> $dest"
  installed=$((installed + 1))
done

echo ""
echo "Resumo: $installed instalada(s), $skipped preservada(s) em $TARGET_DIR"
