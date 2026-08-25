#!/usr/bin/env bash
#
# Self-test for the public-metadata rules. One positive and one negative fixture
# per mechanically-enforced rule, plus edge cases that document the determinism
# limit. Exits nonzero on any surprise so a rule regression fails CI instead of
# silently relaxing the gate. Runs from the workflow before the gate itself.
#
# Conventions: is_banned_section_line returns 0 when the line IS banned,
# 1 otherwise. title_is_outcome returns 0 when the title IS a valid outcome,
# 1 otherwise. Failing calls return nonzero on purpose, so the harness tracks
# expectations itself rather than relying on `set -e`.
set -uo pipefail
cd "$(dirname "$0")"
. ./public-metadata-rules.sh

pass=0
fail=0

check() {  # $1 = description, $2 = actual (0/1), $3 = expected (0/1)
  if [ "$2" -eq "$3" ]; then
    echo "ok   - $1"
    pass=$((pass + 1))
  else
    echo "FAIL - $1 (got $2, want $3)"
    fail=$((fail + 1))
  fi
}

# --- Title rule (PR title / commit subject): outcome-only ---
title_is_outcome "Link footer nav to section hubs"
check "title: a plain outcome title is valid" $? 0
title_is_outcome ""
check "title: empty is not valid" $? 1
title_is_outcome "Why the footer links changed"
check "title: leading 'Why' is narrative" $? 1
title_is_outcome "Motivation: change the footer"
check "title: leading 'Motivation:' is narrative" $? 1
title_is_outcome "## Link footer nav to section hubs"
check "title: a markdown heading is not a title" $? 1

# --- Body / commit / comment section rule: banned narrative section headings ---
is_banned_section_line "## Outcome"
check "section: '## Outcome' is allowed" $? 1
is_banned_section_line "## Verification"
check "section: '## Verification' is allowed" $? 1
is_banned_section_line "## Why"
check "section: '## Why' is banned" $? 0
is_banned_section_line "**Motivation:** the earlier build was slower"
check "section: bold 'Motivation:' is banned" $? 0
is_banned_section_line "Background: the site grew several hubs"
check "section: 'Background:' opener is banned" $? 0
is_banned_section_line "History: the footer used to be inline"
check "section: 'History:' opener is banned" $? 0
is_banned_section_line "The background image now scales"
check "section: prose 'background' is allowed" $? 1
is_banned_section_line "## Why this change was made"
check "section: '## Why <content>' is not decidable and is allowed" $? 1

# --- Commit message rule (subject + body lines) ---
title_is_outcome "fix: link footer nav to section hubs"
check "commit: conventional subject is valid" $? 0
title_is_outcome "Why we changed the footer"
check "commit: narrative subject is invalid" $? 1
is_banned_section_line "Footer links now resolve to section hubs."
check "commit: prose body line is allowed" $? 1
is_banned_section_line "## Motivation"
check "commit: narrative body heading is banned" $? 0

# --- Public comment rule ---
is_banned_section_line "Build passes; links verified."
check "comment: prose is allowed" $? 1
is_banned_section_line "## Motivation"
check "comment: narrative heading is banned" $? 0
is_banned_section_line "Reason: see the build log"
check "comment: 'Reason:' opener is banned" $? 0

# --- Added-diff rule (added lines in markdown files) ---
is_banned_section_line "The footer links resolve to section hubs."
check "diff: added prose line is allowed" $? 1
is_banned_section_line "## Outcome"
check "diff: added allowed heading is allowed" $? 1
is_banned_section_line "## Why"
check "diff: added '## Why' is banned" $? 0
is_banned_section_line "Background: the old build lacked checks"
check "diff: added 'Background:' opener is banned" $? 0

echo
if [ "$fail" -ne 0 ]; then
  echo "public-metadata-fixtures: $fail failed, $pass passed"
  exit 1
fi
echo "public-metadata-fixtures: all $pass fixtures passed."
