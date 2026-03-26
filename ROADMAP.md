---
title: "Digital Avatar & Knowledge Base Roadmap"
---

## 0. Scope (after migration)

This roadmap now tracks only work for **this repository** (`vkgeorgia.github.io`) as a website/content repo.

- In scope here: Jekyll pages, `_projects`, `knowledge-base`, styles/assets, widget frontend.
- Out of scope here: chatbot backend runtime, Cloud Run deployment, DB schema/migrations, Telegram automations.
- Backend moved to: **`vkgeorgia/Jeeves`**.

---

## 1. Website content quality

- [ ] Refresh homepage copy to plain business language (reduce niche jargon).
- [ ] Align `services/`, `approach`, `articles` tone and CTA structure.
- [ ] Audit internal links and eliminate dead/legacy references.
- [ ] Continue improving case narratives in `_projects/`.

## 2. Dynamic experience pages (website side only)

- [ ] Keep dynamic pages stable (`projects/`, `domains/`, `roles/`) against backend API changes.
- [ ] Add graceful fallback UI when API is unavailable (user-friendly message + retry hint).
- [ ] Add lightweight caching strategy for repeated API calls on same page.

## 3. Knowledge-base hygiene in this repo

- [ ] Remove/archive duplicate markdown content that is not used by site pages.
- [ ] Keep `knowledge-base/` focused on profile, domains, education, and editorial content.
- [ ] Maintain `_projects/` as the narrative archive for case descriptions.

## 4. Documentation alignment (multi-repo)

- [ ] Ensure all docs in this repo clearly state: backend is external (`vkgeorgia/Jeeves`).
- [ ] Remove stale instructions that reference local backend runtime/deploy scripts.
- [ ] Add a short “integration contracts” section with links to backend API docs in external repo.

## 5. SEO and analytics

- [ ] Normalize `seo_title` and `description` quality across top pages.
- [ ] Add analytics configuration and privacy-friendly event tracking for key CTA clicks.
- [ ] Improve structured data consistency (person/service schema coverage).

## 6. Operational discipline

- [ ] Keep quarterly content audit cadence (articles, cases, metadata freshness).
- [ ] Track GitHub Pages build health and cache quirks.
- [ ] Keep `PROJECT_STATUS.md` and this roadmap in sync after major architecture changes.
