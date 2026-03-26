# Project Status: vkgeorgia.github.io

**Last Updated:** 2026-03-26  
**Site URL:** https://vkgeorgia.github.io

---

## Overview

`vkgeorgia.github.io` is now the **website/content repository** (GitHub Pages).  
The AI backend (chatbot, API, leads/contacts logic) was moved out to a separate project: **`vkgeorgia/sam`**.

---

## Current Repository Scope

### In Scope (this repo)
- Jekyll website pages and content (`index.md`, `cases.md`, `services/`, etc.)
- Portfolio source files (`_projects/`)
- Knowledge and article markdown (`knowledge-base/`)
- Website styles/assets (`assets/`, images)
- Frontend widget/static files under `digital-avatar/frontend/`

### Out of Scope (moved to external repo)
- FastAPI backend
- Cloud Run deployment workflow for chatbot backend
- Neon DB schema/migrations for backend services
- Telegram notifications, contact verification, proposal/lead APIs

---

## Recent Major Change (Mar 2026)

### Site + AI became parts of a larger multi-repo system
- **Backend moved:** old chatbot backend removed from this repo and relocated to `vkgeorgia/sam`.
- **Old backend deploy workflow removed:** this repo no longer deploys backend to Cloud Run.
- **Separation of concerns:** website/content stays here; runtime AI services evolve in external backend repo.

---

## Technical Configuration (Current)

### Frontend / Site
- **Platform:** GitHub Pages
- **Engine:** Jekyll (theme: Minima)
- **Collections:** `_projects` (output: false)
- **Custom CSS:** `assets/main.scss`
- **Plugins:** `jekyll-feed`, `jekyll-sitemap`

### AI Integration
- Site embeds frontend widget/static assets.
- Backend/API endpoints are provided by external project (`vkgeorgia/sam`) and configured there.

---

## Known Issues & Quirks

### CSS Frontmatter Corruption
- **Problem:** editing tools can corrupt YAML frontmatter in `assets/main.scss`
- **Correct header must be exactly:**
  ```
  ---
  ---
  @import "minima";
  ```

### GitHub Pages Caching
- **Issue:** old CSS may persist after successful deploy
- **Workaround:** force rebuild with empty commit

---

## Next Steps / Backlog (Website Repo)

- [ ] Continue content and case updates
- [ ] Improve SEO metadata consistency
- [ ] Add analytics for site usage
- [ ] Keep docs aligned with multi-repo architecture

---

## Quick Reference Commands

```bash
# Local Jekyll development
bundle exec jekyll serve

# Force GitHub Pages rebuild
git commit --allow-empty -m "Force rebuild" && git push
```
