#!/usr/bin/env bash
# Stage sanitized case content for a LOCAL build.
#
# Case bodies + PDFs are NOT committed to this public repo — they live in the
# private `cases-public-ready` repo (Layer 2 of the publication pipeline) and are
# copied in at build time. CI does this via the deploy key; locally this script
# does it from a sibling clone.
#
# Usage:
#   script/stage-cases.sh [path-to-cases-public-ready]
# Default source: ../cases-public-ready
#
# The staged files are gitignored (_projects/*.md, downloads/*.pdf), so they will
# not be accidentally committed.
set -euo pipefail

SRC="${1:-../cases-public-ready}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -d "$SRC/_projects" ]; then
  echo "error: '$SRC/_projects' not found." >&2
  echo "Clone the sanitized-cases repo first, e.g.:" >&2
  echo "  git clone git@github.com:vkgeorgia/cases-public-ready.git $SRC" >&2
  exit 1
fi

mkdir -p "$ROOT/_projects" "$ROOT/downloads"
cp "$SRC"/_projects/*.md "$ROOT/_projects/"
if compgen -G "$SRC/downloads/*.pdf" > /dev/null; then
  cp "$SRC"/downloads/*.pdf "$ROOT/downloads/"
fi

echo "Staged $(ls "$ROOT"/_projects/*.md | wc -l | tr -d ' ') case files and \
$(ls "$ROOT"/downloads/*.pdf 2>/dev/null | wc -l | tr -d ' ') PDFs from $SRC."
