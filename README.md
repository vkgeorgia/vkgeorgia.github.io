---
layout: page
title: "About this repository"
description: "Source of vkgeorgia.github.io — practitioner site of Valerii Korobeinikov, Enterprise Architect."
lang: en
---

# About this repository

This repository hosts the source of **[vkgeorgia.github.io](https://vkgeorgia.github.io/)** — the practitioner site of **Valerii Korobeinikov**, Enterprise Architect.

The site is the public surface of the practice: positioning, engagement formats, selected outcomes, and an AI assistant. It is not a technical documentation site.

## AI assistant

The site features an **AI assistant** that can answer questions about Valerii's professional experience, engagement formats, and help schedule a meeting. Open the chat from the icon at the bottom-right corner of any page.

The assistant backend lives in a separate repository (`vkgeorgia/Jeeves`); this repository contains the site frontend (Jekyll source, layouts, and the chat widget assets) only.

## Local build

Requires **Ruby 3.3.x** (the `github-pages` / `commonmarker` chain is not yet compatible with Ruby 4). Easiest via Homebrew:

```bash
brew install ruby@3.3
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"   # on Intel Mac: /usr/local/opt/ruby@3.3/bin
cd /path/to/vkgeorgia.github.io
bundle install
bundle exec jekyll serve
```

A `.ruby-version` file is included (for rbenv / chruby / asdf). Gems install into `vendor/` (gitignored).
