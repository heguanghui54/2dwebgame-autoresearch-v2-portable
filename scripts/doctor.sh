#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="2dwebgame-autoresearch-v2"
SKILL_DIR="$ROOT_DIR/skill/$SKILL_NAME"
SKILLS_DIR="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"
FAIL=0

ok() { printf "OK       %s\n" "$1"; }
warn() { printf "WARN     %s\n" "$1"; }
fail() { printf "MISSING  %s\n" "$1"; FAIL=1; }

check_required() {
  if command -v "$1" >/dev/null 2>&1; then
    ok "$1: $(command -v "$1")"
  else
    fail "$1"
  fi
}

check_recommended() {
  if command -v "$1" >/dev/null 2>&1; then
    ok "$1: $(command -v "$1")"
  else
    warn "$1 is not installed; related pipeline stages will be disabled or SKIPPED_NO_SCORE"
  fi
}

echo "2DWebGame AutoResearch v2 portable doctor"
echo "Root: $ROOT_DIR"
echo

for cmd in bash git node npm python3; do
  check_required "$cmd"
done

for cmd in ffmpeg ffprobe rg gh; do
  check_recommended "$cmd"
done

echo
if [ -f "$SKILL_DIR/SKILL.md" ]; then
  ok "portable skill exists: $SKILL_DIR/SKILL.md"
else
  fail "portable skill missing: $SKILL_DIR/SKILL.md"
fi

if grep -q "^name: $SKILL_NAME$" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
  ok "skill frontmatter name matches folder"
else
  fail "skill frontmatter name mismatch"
fi

if [ -d "$SKILLS_DIR" ]; then
  ok "Codex skills dir exists: $SKILLS_DIR"
else
  warn "Codex skills dir does not exist yet: $SKILLS_DIR"
fi

for peer in generate2dmap generate2dsprite; do
  if [ -d "$SKILLS_DIR/$peer" ]; then
    ok "optional peer skill installed: $peer"
  else
    warn "optional peer skill not found: $peer"
  fi
done

echo
if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    ok "GitHub CLI authenticated"
  else
    warn "GitHub CLI installed but not authenticated; run: gh auth login"
  fi
fi

echo
if [ "$FAIL" -eq 0 ]; then
  echo "Doctor result: portable package is installable. Optional generators/benchmarks may still need setup."
else
  echo "Doctor result: missing required dependencies."
fi

exit "$FAIL"

