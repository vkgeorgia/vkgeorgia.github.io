---
layout: page
title: "About this repository"
description: "Source of korobeinikov.consulting — practitioner site of Valerii Korobeinikov, Enterprise Architect."
lang: en
---

# About this repository

This repository hosts the source of **[korobeinikov.consulting](https://korobeinikov.consulting/)** — the practitioner site of **Valerii Korobeinikov**, Enterprise Architect. The repository name is the historical GitHub Pages host, which now serves a permanent redirect to the custom domain.

The site is the public surface of the practice: positioning, engagement formats, selected outcomes, and an AI assistant. It is not a technical documentation site.

## AI assistant

The site features an **AI assistant** that can answer questions about Valerii's professional experience, engagement formats, and help schedule a meeting. Open the chat from the icon at the bottom-right corner of any page.

The assistant backend lives in a separate, private repository; this repository contains the site frontend (Jekyll source, layouts, and the chat widget assets) only.

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

## Case content & deployment

Case studies are **not stored in this repo**. They are produced by a separate publication pipeline and copied in **at build time**:

- The `projects` collection (`_projects/*.md`) and the case PDFs (`downloads/*.pdf`) are fetched from a private intermediate repo during the build. They are gitignored here and never committed.
- Each case renders at `/cases/<id>/`; the `/cases/` index curates three featured studies plus a condensed list of the rest.

**Deployment.** `.github/workflows/build-deploy.yml` fetches the case content (via a read-only deploy key in Actions secrets), runs `bundle exec jekyll build`, and publishes `_site/` to the `gh-pages` branch. GitHub Pages is configured to serve from `gh-pages` (not the default branch auto-build, which can't use the deploy key).

**Local build with cases.** Clone the intermediate repo alongside this one, stage its content, then build:

```bash
script/stage-cases.sh ../cases-public-ready   # copies cases + PDFs in (gitignored)
bundle exec jekyll build
```

Without staging, the site still builds — the `/cases/` page is simply empty. Public-only work needs no access to the intermediate repo.
