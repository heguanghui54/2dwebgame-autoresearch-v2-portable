#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE_NAME="$(basename "$ROOT_DIR")"
VERSION="${VERSION:-$(date +%Y%m%d)}"
OUT_DIR="$ROOT_DIR/dist"
OUT_FILE="$OUT_DIR/$BASE_NAME-$VERSION.tar.gz"

mkdir -p "$OUT_DIR"
rm -f "$OUT_FILE" "$OUT_FILE.sha256"

(
  cd "$ROOT_DIR/.."
  tar \
    --exclude "$BASE_NAME/.git" \
    --exclude "$BASE_NAME/dist" \
    --exclude "$BASE_NAME/dist/*" \
    --exclude "$BASE_NAME/node_modules" \
    --exclude "$BASE_NAME/node_modules/*" \
    --exclude "$BASE_NAME/templates/phaser-vite/dist" \
    --exclude "$BASE_NAME/templates/phaser-vite/dist/*" \
    --exclude "$BASE_NAME/templates/phaser-vite/node_modules" \
    --exclude "$BASE_NAME/templates/phaser-vite/node_modules/*" \
    -czf "$OUT_FILE" \
    "$BASE_NAME"
)

if command -v shasum >/dev/null 2>&1; then
  shasum -a 256 "$OUT_FILE" > "$OUT_FILE.sha256"
elif command -v sha256sum >/dev/null 2>&1; then
  sha256sum "$OUT_FILE" > "$OUT_FILE.sha256"
else
  echo "WARN: no sha256 command found; checksum skipped" >&2
fi

echo "Created $OUT_FILE"
