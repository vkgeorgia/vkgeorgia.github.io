# Project Rules & Guidelines

This document serves as the operational manual for the `vkgeorgia.github.io` project.

## 1. Source of Truth — Neon DB

> **Neon DB — единственный источник правды для всех структурированных данных о проектах.**

*   Метаданные проектов (title, industry, domain, role, employer, technology, STAR, key_result и т.д.) живут в таблице `projects` и junction-таблицах (`project_industries`, `project_domains`, `project_roles`).
*   Проекты добавляются и редактируются **в первую очередь в Neon**. Файлы `_projects/*.md` могут отставать.
*   При любом расхождении между Neon и `_projects/*.md` — **Neon главнее**. Не «исправляй» Neon по данным из файлов.
*   Число проектов, теги, индустрии, роли — всё берётся из Neon.

## 2. Project Portfolio (`_projects/`)
*   **Роль**: нарративный архив — длинные тексты кейсов для RAG и резервный источник. Не источник правды для метаданных.
*   **Structure**: Each project is a separate `.md` file.
*   **Project Codes**:
    *   **One project = one code. Codes must be unique across all projects.**
    *   Codes (e.g., `RTK-PROTEUS`, `SKY-BARS`) must **NEVER** appear in the visible Title or Content Header.
    *   Codes must **ONLY** be stored in the `project_code` field in the frontmatter.
    *   If a project historically had a second code, store it in the `notes` field: `notes: "Legacy secondary code: EPM-ECO"`.
    *   *Correct*: `title: "Traffic analytics system"`
    *   *Incorrect*: `title: "Traffic analytics system (RTK-PROTEUS)"`
    *   *Incorrect*: `project_code: [EPM-PSR, EPM-ECO]` — multiple codes in one field are not allowed.
*   **Notes** (`notes`):
    *   Free-text field for internal remarks (legacy codes, context, caveats).
    *   Stored in Neon DB as `notes TEXT` and in frontmatter as `notes: "..."`.
    *   Not shown publicly.
*   **Client visibility** (`client_name_visibility`):
    *   `[public]` — имя клиента можно показывать публично.
    *   `[hidden]` — имя клиента конфиденциально; на сайте и в боте отображать как «Confidential client».
    *   Поле должно присутствовать в каждом `.md` файле.
    *   **В Neon DB**: колонка `client_public BOOLEAN` (миграция: `sql/add_client_public.sql`). Именно она управляет поведением API и бота — фронтматтер вторичен.

## 3. Knowledge Base Structure
*   **`_projects/`**: нарративные тексты кейсов. Jekyll строит страницу Cases из этих файлов.
*   **`knowledge-base/`**: биография, статьи, домены. Не для проектных данных.
*   **`digital-avatar/backend/knowledge_base/`**: авто-генерируется при деплое. **НЕ редактировать вручную.**

## 4. AI Avatar Persona
*   **Identity**: "M-Shape Architect", "Launcher", "Troubleshooter".
*   **Core Philosophy**: "Entropy Reduction".
*   **Tone**: Pragmatic, direct, result-oriented. NOT a passive assistant.
*   **Context**: The avatar relies on `profile.md`, `business-challenges.md`, and `index.md` (copied to root during build) for its core instructions.

### Project Codes in Bot Responses — NEVER EXPOSE
*   Project codes (e.g. `RTK-PROTEUS`, `SKY-BARS`, `TRANS-AIPOC`, `HR-BOT`) are **internal identifiers** used only in the database and admin tools.
*   The bot **MUST NEVER** mention, display, or reference project codes in any user-facing response.
*   Project codes are stored in Neon DB for unambiguous identification; they appear only in the admin panel.
*   *Correct*: "In the AI Agent-Based Process Automation project I built..."
*   *Incorrect*: "In project TRANS-AIPOC I built..."
*   This rule is enforced in the bot system prompt (§8 in `rag_service.py`).

## 5. Deployment
*   **Trigger**: Push to `main` → GitHub Actions `.github/workflows/deploy-backend.yml` builds and deploys automatically.
*   **Platform**: Google Cloud Run, `linux/amd64`, service `ai-avatar`, region `us-central1`.
*   **Never commit secrets**: `GEMINI_API_KEY`, `NEON_DATABASE_URL`, `TELEGRAM_BOT_TOKEN` — only in GitHub Secrets / Cloud Run env vars.


## 7. Agent Rules (что можно и нельзя)

### Можно
*   Добавлять новые эндпоинты и фильтры в `app/routers/`.
*   Добавлять/изменять Jekyll-страницы и шаблоны.
*   Добавлять новые таблицы в Neon через SQL-миграции (не трогая существующие столбцы без крайней необходимости).
*   Обновлять документацию (`ARCHITECTURE.md`, `PROJECT_RULES.md`, `ROADMAP.md`).

### Нельзя
*   Коммитить реальные значения API-ключей, токенов, DSN в репозиторий.
*   Ломать или удалять существующие API-маршруты: `/ws/chat`, `/api/projects`, `/api/contacts`.
*   Изменять `digital-avatar/frontend/widget.js` в части WebSocket-контракта без согласования.
*   "Исправлять" данные в Neon по данным из файлов — Neon всегда главнее.
