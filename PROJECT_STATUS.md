# Project Status: vkgeorgia.github.io

**Last Updated:** 2026-01-16  
**Site URL:** https://vkgeorgia.github.io

---

## Overview

Personal portfolio and consulting website for Valerii Korobeinikov, positioned as an **M-Shape Architect** specializing in **Entropy Reduction**, **System Launching**, and **Crisis Management**.

---

## Current Site Structure

### Pages (Navigation)
1. **Profile** (`index.md`) — Homepage, M-Shape manifesto
2. **Business Challenges** (`business-challenges.md`) — Problem-solution framing
3. **Services** (`services/index.md`) — Launcher & Troubleshooter offerings
4. **Cases** (`cases.md`) — Dynamic project portfolio with filtering
5. **Approach** (`approach.md`) — Philosophy: Entropy Reduction, Build & Fix
6. **Articles** (`articles.md`) — Field Notes & System Design

### Key Directories
- `_projects/` — **Single source of truth** for case studies (44 projects)
- `knowledge-base/` — Bio, education, articles, domains (not for projects)
- `digital-avatar/` — AI chatbot backend (FastAPI + Gemini)
- `assets/` — CSS/SCSS, images

---

## Recent Major Changes (Jan 2026)

### 1. M-Shape Persona Implementation
- **Completed**: `index.md`, `services/index.md`, `cases.md`, `approach.md`, `articles.md`
- **Tone**: Pragmatic, direct, "Launcher & Troubleshooter" (not advisory)
- **Key Concepts**: Entropy Reduction, Build & Fix, Self-Redundancy

### 2. Cases Page Refactoring
- **Before**: 4000+ lines of static HTML accordion
- **After**: Dynamic Liquid templating with JavaScript filtering
- **Features**: Filter by Industry, Functional Domain, Role
- **Tag Consolidation**: Reduced ~40 functional tags to 10 groups (e.g., `marketing-automation`, `analytics`, `retail-technologies`)

### 3. Project Code Scrubbing
- **Rule**: Internal codes (e.g., `RTK-PROTEUS`) are **hidden** from titles and headers
- **Storage**: Codes remain in `project_code` frontmatter field only
- **Files Cleaned**: 44 projects

### 4. Typography & Layout
- **Width**: 1024px (standard professional width)
- **Heading Scale**: Major Third (1.25 ratio)
  - H1: 2.44rem (≈39px)
  - H2: 1.95rem (≈31px)
  - H3: 1.56rem (≈25px)
  - H4: 1.25rem (≈20px)
  - H5/H6: 1rem (≈16px)
- **CSS File**: `assets/main.scss` (renamed from `.css` for Jekyll processing)

### 5. Content Updates
- **Section Rename**: "Reflection (Optional but Recommended)" → "Lessons Learned" (all 44 projects)
- **Articles Header**: "Articles & Insights" → "Field Notes & System Design"

---

## Technical Configuration

### Jekyll Setup
- **Theme**: Minima
- **Collections**: `_projects` (output: false)
- **Custom CSS**: `assets/main.scss` (overrides Minima defaults)
- **Plugins**: `jekyll-feed`, `jekyll-sitemap`

### AI Avatar (Digital Assistant)
- **Backend**: FastAPI (Python) + Google Gemini API
- **Deployment**: Google Cloud Run (Docker, linux/amd64)
- **Knowledge Base**: Auto-synced from `_projects` and `knowledge-base` via `deploy.sh`
- **Persona**: M-Shape Architect (same as website)

### Deployment
- **Platform**: GitHub Pages
- **Build Time**: 2-3 minutes after push
- **Deploy Script**: `digital-avatar/backend/deploy.sh` (for AI backend)

---

## Project Rules (see PROJECT_RULES.md)

1. **Project Codes**: Never display in titles/headers, only in `project_code` frontmatter
2. **Single Source of Truth**: `_projects/` for portfolio, `knowledge-base/` for other content
3. **AI Avatar Knowledge Base**: Auto-generated, do not edit manually
4. **CSS File**: Must be `.scss` (not `.css`) for Jekyll to process

---

## Known Issues & Quirks

### CSS Frontmatter Corruption
- **Problem**: `replace_file_content` tool sometimes corrupts YAML frontmatter in `assets/main.scss`
- **Symptom**: First line becomes `--- --- @import "minima";` (breaks Jekyll)
- **Fix**: Use Python script to force-overwrite with correct 3-line format:
  ```
  ---
  ---
  @import "minima";
  ```

### GitHub Pages Caching
- **Issue**: Sometimes serves old CSS even after successful deploy
- **Solution**: Force rebuild with empty commit: `git commit --allow-empty -m "Force rebuild" && git push`

---

## Next Steps / Backlog

- [ ] Add more articles to `articles.md`
- [ ] Consider adding testimonials/recommendations
- [ ] Optimize AI avatar response time
- [ ] Add analytics (Google Analytics or similar)
- [ ] Review SEO metadata across all pages

---

## Quick Reference Commands

```bash
# Local Jekyll development
bundle exec jekyll serve

# Deploy AI avatar backend
cd digital-avatar/backend
./deploy.sh

# Force GitHub Pages rebuild
git commit --allow-empty -m "Force rebuild" && git push
```

---

## Contact & Links

- **Email**: vkgeorgia@icloud.com
- **LinkedIn**: https://www.linkedin.com/in/valeriikorobeinikov/
- **GitHub**: https://github.com/vkgeorgia
- **Calendar**: https://calendar.app.google/YwmXZytfSQ2qWX4Z7
