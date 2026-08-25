#!/usr/bin/env bash
#
# Shared rule functions for the public-metadata gate (workflow
# public-metadata.yml). Sourced, not executed: defines the check functions and
# prints nothing on import.
#
# The boundary (root AGENTS.md, "Public surface"): a public PR title states only
# the delivered outcome; the body states only the resulting behaviour and how it
# was verified; commit messages and public comments follow the same boundary.
# This library encodes the subset that is mechanically decidable: banned
# narrative section headings and leading narrative words. Narrative carried as
# ordinary prose, and headings that place the narrative word in mid-title
# ("## Why we changed X"), are not decidable and are intentionally left to
# review; the fixtures document which forms are covered.

# Words that name a narrative section when they lead a heading or a "Word:"
# line. Kept to the boundary vocabulary. Technical prose uses of the same words
# (a "background image", a "context menu") are not section markers and pass:
# the matcher only fires when the word is the entire heading or is followed by
# a colon.
BANNED_SECTION_WORDS='why|motivation|background|context|discovery|narrative|remediation|history|rationale|reason'

# Words that mark a PR title or commit subject as narrative when they lead it.
# "Background" / "Context" / "History" are excluded because they are plausible
# outcome subjects ("Background image on the hero"); those forms are not
# mechanically decidable and are left to review.
BANNED_TITLE_LEAD='why|motivation|rationale|reason'

# is_banned_section_line <line>
# True (0) when the line is a banned narrative section: a markdown heading whose
# text is exactly a banned word or a banned word followed by a colon
# ("## Why", "**Motivation:**", "## Background:"), or a bare "Word:" opener
# ("Why: ..."). Prose lines, allowed headings ("## Outcome", "## Verification"),
# and headings that continue after the banned word ("## Why we changed X") pass.
is_banned_section_line() {
  local line t word rest
  line="$(printf '%s' "$1" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
  [ -n "$line" ] || return 1

  # The line must look like a heading before we judge its text: a markdown
  # heading, a bold heading, or a bare "Word:" opener. A plain sentence that
  # merely starts with a banned word ("Background images are lazy-loaded") is
  # not a section and passes.
  local looks_like_heading=0
  [[ "$line" =~ ^#{1,6}[[:space:]] ]] && looks_like_heading=1
  [[ "$line" =~ ^\*\* ]] && looks_like_heading=1
  [[ "$line" =~ ^[A-Za-z]+[:：] ]] && looks_like_heading=1
  [ "$looks_like_heading" -eq 1 ] || return 1

  # Normalize: drop the markdown heading / bold prefix and any trailing bold.
  t="$(printf '%s' "$line" | sed -E 's/^#{1,6}[[:space:]]*//; s/^\*\*//; s/\*\*[[:space:]]*$//')"
  t="$(printf '%s' "$t" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"

  word="$(printf '%s' "$t" | sed -E 's/^([A-Za-z]+).*/\1/' | tr '[:upper:]' '[:lower:]')"
  [ -n "$word" ] || return 1
  rest="$(printf '%s' "$t" | sed -E 's/^[A-Za-z]+//' | sed 's/^[[:space:]]*//')"

  case "$word" in
    why|motivation|background|context|discovery|narrative|remediation|history|rationale|reason)
      if [ -z "$rest" ] || [[ "$rest" =~ ^[:：] ]]; then
        return 0
      fi
      ;;
  esac
  return 1
}

# title_is_outcome <title>
# True (0) when the title is a non-empty single line that does not lead with a
# banned narrative word and carries no markdown heading marker.
title_is_outcome() {
  local t="$1"
  t="${t//$'\r'/}"
  [ -n "$t" ] || return 1
  [[ "$t" == *$'\n'* ]] && return 1
  [[ "$t" =~ ^[[:space:]]*# ]] && return 1
  local lead
  lead="$(printf '%s' "$t" | sed -E 's/^[[:space:]]*([A-Za-z]+).*/\1/' | tr '[:upper:]' '[:lower:]')"
  case "$lead" in
    why|motivation|rationale|reason) return 1 ;;
  esac
  return 0
}
