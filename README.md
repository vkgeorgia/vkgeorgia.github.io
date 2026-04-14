---
layout: page
title: "Welcome"
description: "Technical site of Valerii Korobeinikov, Enterprise Architect and Strategic Consultant"
lang: en
permalink: /
---

# Welcome

This is the technical site of **Valerii Korobeinikov**, Enterprise Architect and Strategic Consultant.

Here I publish:
- detailed project documentation,
- architecture diagrams,
- capability models,
- notes on enterprise transformation and product management.

## AI Avatar

This site features an **AI-powered digital avatar** that can answer questions about my professional experience, consulting services, and help schedule meetings. Click the chat icon in the bottom-right corner to start a conversation!

The backend for the avatar is maintained in a separate repository:
- [`vkgeorgia/Jeeves`](https://github.com/vkgeorgia/Jeeves)

This repository contains the website/content side and frontend widget assets.

</p>

## Project structure

1.  **`_projects/`** — портфолио: Jekyll строит страницу **Cases**; тексты проектов также использует бэкенд (Jeeves).
2.  **`vkgeorgia/Jeeves`** — runtime (чат, RAG, интеграции); этот репозиторий — только сайт и виджет.

## Локальная сборка

```bash
bundle install
bundle exec jekyll serve
```

Гемы ставятся в `vendor/` (каталог в `.gitignore`), в репозиторий они не коммитятся.
