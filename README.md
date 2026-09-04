---
layout: page
title: "About this repository"
description: "Source of korobeinikov.consulting — practitioner site of Valerii Korobeinikov, Enterprise Architect."
lang: en
---

# About this repository

This repository hosts the source of **[korobeinikov.consulting](https://korobeinikov.consulting/)** — the practitioner site of **Valerii Korobeinikov**, Enterprise Architect. The repository name is the historical GitHub Pages host, which now serves a permanent redirect to the custom domain.

The site is the public surface of the practice: positioning, engagement formats, selected outcomes. It is not a technical documentation site.

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

Case studies are **not stored in this repo**. They are copied in **at publish time** on the 24/7 build host from a private clone:

- The `projects` collection (`_projects/*.md`) and the PDFs (`downloads/*.pdf`, including the résumé) are gitignored here and never committed.
- Each case renders at `/cases/<id>/`; the `/cases/` index curates three featured studies plus a condensed list of the rest.

**Deployment.** The host stages those files, runs `bundle exec jekyll build`, and pushes `_site/` to the `gh-pages` branch. GitHub Pages serves `gh-pages`. GitHub Actions does **not** fetch private case content and does **not** publish.

**CI.** `.github/workflows/build-deploy.yml` builds the public tree (cases empty) and runs crawlability checks on pull requests and `main`.

**Local build with cases.** The site builds without case content — the `/cases/` page is simply empty. Maintainers who need the full site locally copy the case markdown and PDFs into `_projects/` and `downloads/` from the private clone, then build as above.

## Link, sitemap, and robots.txt verification

`script/verify-crawlability.rb` checks the *built* site for the class of regression where a page moves and a link, a sitemap entry, or a `robots.txt` rule is left pointing at the old location: internal 404s, internal links that 301 (usually a missing trailing slash) or land on a redirect stub, invalid or non-indexable sitemap entries, reachable pages missing from the sitemap, sitemap URLs with no internal link path from `/`, and `robots.txt` paths that don't correspond to anything in the build. It reads only the local build output — no network access.

```bash
bundle exec jekyll build
bundle exec ruby script/verify-crawlability.rb
```

Runs in CI after the public-tree build, and on the build host after a full publish build.
