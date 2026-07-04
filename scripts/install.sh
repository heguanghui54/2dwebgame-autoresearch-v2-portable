#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="2dwebgame-autoresearch-v2"
SKILL_SRC="$ROOT_DIR/skill/$SKILL_NAME"
SKILLS_DIR="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"
DEST="$SKILLS_DIR/$SKILL_NAME"

if [ ! -f "$SKILL_SRC/SKILL.md" ]; then
  echo "ERROR: skill source not found: $SKILL_SRC" >&2
  exit 1
fi

mkdir -p "$SKILLS_DIR"

if [ -e "$DEST" ]; then
  BACKUP="$DEST.backup.$(date +%Y%m%d%H%M%S)"
  echo "Existing skill found. Moving it to: $BACKUP"
  mv "$DEST" "$BACKUP"
fi

mkdir -p "$DEST"
if command -v rsync >/dev/null 2>&1; then
  rsync -a "$SKILL_SRC/" "$DEST/"
else
  cp -R "$SKILL_SRC/." "$DEST/"
fi

echo "Installed $SKILL_NAME to $DEST"
echo 'Use it in Codex as: $2dwebgame-autoresearch-v2'
