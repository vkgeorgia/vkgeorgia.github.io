#!/usr/bin/env bash
#
# Enforces the public-metadata boundary on a pull request, or on a push to the
# default branch, on the pushed commit messages and diff. Reads the current PR
# title, body, commit range, added diff, and public comments at run time, so a
# title/body edit re-runs against the current text. Any rule failure exits
# nonzero (not green); a missing input also exits nonzero so a check that did
# not run is never reported as passing.
#
# Requires in the environment: GH_TOKEN (or an authenticated gh), REPO.
# PR mode:  PR_NUMBER.
# Push mode: BASE_SHA and HEAD_SHA.
set -euo pipefail
cd "$(dirname "$0")"
. ./public-metadata-rules.sh

REPO="${REPO:?public-metadata: REPO is required}"
PR_NUMBER="${PR_NUMBER:-}"
BASE_SHA="${BASE_SHA:-}"
HEAD_SHA="${HEAD_SHA:-}"

fail=0
err() { echo "::error::public-metadata: $1"; fail=1; }

# check_section_text <location> <text>
# Fails when any line of <text> is a banned narrative section heading.
check_section_text() {
  local loc="$1" text="$2" line
  while IFS= read -r line; do
    if is_banned_section_line "$line"; then
      err "banned narrative section in $loc: ${line}"
      return
    fi
  done <<<"$text"
}

# check_title <location> <title>
check_title() {
  local loc="$1" title="$2"
  if ! title_is_outcome "$title"; then
    err "$loc must state the delivered outcome (non-empty, single-line, no heading, no narrative lead): '$(printf '%s' "$title" | head -c 120)'"
  fi
}

# check_commit_subjects — stdin carries one commit subject per line.
check_commit_subjects() {
  local loc="$1" subj
  while IFS= read -r subj; do
    check_title "$loc" "$subj"
  done
}

# check_commit_bodies — stdin carries the concatenated commit bodies.
check_commit_bodies() {
  local loc="$1"
  check_section_text "$loc" "$(cat)"
}

# extract_added_md_lines — reads a unified diff on stdin, prints added lines of
# markdown files, skipping fenced code blocks. Used for the PR diff and a git
# range diff alike.
extract_added_md_lines() {
  awk '
    /^diff --git / {
      path = $0; sub(/^diff --git a\/[^ ]* b\//, "", path)
      is_md = (path ~ /\.md$/)
      in_fence = 0
      next
    }
    is_md && /^\+/ && $0 !~ /^\+\+\+/ {
      line = $0; sub(/^\+/, "", line)
      if (line ~ /^```/) { in_fence = !in_fence; next }
      if (!in_fence) print line
    }
  '
}

check_diff() {  # stdin = unified diff
  local tmp
  tmp="$(mktemp)"
  extract_added_md_lines > "$tmp"
  if [ -s "$tmp" ]; then
    check_section_text "an added line in a markdown file" "$(cat "$tmp")"
  fi
  rm -f "$tmp"
}

pr_mode() {
  [ -n "$PR_NUMBER" ] || { err "PR_NUMBER is empty on a pull-request run"; return; }
  check_title "PR title" "$(gh pr view "$PR_NUMBER" -R "$REPO" --json title --jq '.title')"
  check_section_text "the PR body" "$(gh pr view "$PR_NUMBER" -R "$REPO" --json body --jq '.body // ""')"

  gh pr view "$PR_NUMBER" -R "$REPO" --json commits --jq '.commits[].messageHeadline' \
    | check_commit_subjects "a commit message"
  gh pr view "$PR_NUMBER" -R "$REPO" --json commits --jq '.commits[] | (.messageBody // "")' \
    | check_commit_bodies "a commit message"

  # Public comments: top-level PR conversation and inline review comments.
  check_section_text "a public comment" "$(
    gh api "repos/$REPO/issues/$PR_NUMBER/comments" --paginate --jq '.[].body'
    gh api "repos/$REPO/pulls/$PR_NUMBER/comments" --paginate --jq '.[].body'
  )"

  gh pr diff "$PR_NUMBER" -R "$REPO" | check_diff
}

push_mode() {
  [ -n "$HEAD_SHA" ] || { err "HEAD_SHA is empty on a push run"; return; }
  local range=""
  if [ -n "$BASE_SHA" ] && [ "$BASE_SHA" != "0000000000000000000000000000000000000000" ]; then
    range="$BASE_SHA..$HEAD_SHA"
  fi
  if [ -n "$range" ]; then
    git log "$range" --reverse --format=%s | check_commit_subjects "a commit message"
    git log "$range" --reverse --format=%b | check_commit_bodies "a commit message"
    git diff "$range" | check_diff
  else
    # First push to a branch: only the head commit can be judged.
    git log -1 --format=%s "$HEAD_SHA" | check_commit_subjects "a commit message"
    git log -1 --format=%b "$HEAD_SHA" | check_commit_bodies "a commit message"
  fi
}

if [ -n "$PR_NUMBER" ]; then
  pr_mode
else
  push_mode
fi

if [ "$fail" -ne 0 ]; then
  echo "::error::public-metadata: blocking check failed. Fix the flagged text and push again."
  exit 1
fi
echo "public-metadata: clean."
