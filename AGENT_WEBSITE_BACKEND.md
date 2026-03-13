## Агент: Website & Backend Maintainer

Этот агент отвечает за разработку и поддержку **статического сайта** и **backend‑сервиса на Cloud Run** для проекта `vkgeorgia.github.io`. Его цель — поддерживать единый, согласованный слой презентации (сайт) и данных (Neon + Cloud Run), не ломая существующую инфраструктуру.

### 1. Технологический стек и общая архитектура

- **Фронтенд сайта**
  - Jekyll (GitHub Pages), корень репозитория `vkgeorgia.github.io`.
  - Коллекция `_projects/*.md` — исходные Executive‑описания проектов.
  - Страницы `industries/`, `domains/`, `roles/`, `cases.md`, `services/` и т.п. — витрины поверх проектов.
  - Виджет `digital-avatar/frontend` — UI для AI‑аватара, использующий Cloud Run backend.

- **Backend (Digital Avatar API)**
  - Расположен в `digital-avatar/backend`.
  - FastAPI (`app/main.py`), uvicorn.
  - Развёрнут на **Google Cloud Run** как сервис `ai-avatar`.
  - Подключается к **Neon/PostgreSQL** через переменную окружения `NEON_DATABASE_URL`.
  - Основные эндпоинты (для Sam‑UI, сайта и агентов):
    - `GET /api/projects` — список проектов с фильтрами.
    - `GET /api/projects/{code}` — детали проекта (Executive + STAR).
    - `GET /api/contacts` — список контактов.
    - `GET /api/contacts/{id}` — детали контакта.
    - `GET /` и `ws://.../ws/chat` — существующий API для AI‑аватара.

- **База данных**
  - **Neon** (PostgreSQL), база `neondb`.
  - Таблицы:
    - `projects` — объединённый источник правды по проектам (коды, названия, годы, Executive, STAR, связи с тегами).
    - `project_industries`, `project_domains`, `project_roles` — связи проектов с индустриями/доменами/ролями.
    - `contacts` — контакты (структура определяется приложением `apps/contacts` в репозитории Sam).

### 2. Версии и среды

- **Локальная среда разработки backend’а**
  - Рабочая директория: `digital-avatar/backend`.
  - Зависимости: `requirements.txt`.
  - Локальный запуск:
    ```bash
    cd digital-avatar/backend
    python -m venv .venv        # при необходимости
    source .venv/bin/activate
    pip install -r requirements.txt

    # В .env задать:
    # GEMINI_API_KEY=...
    # NEON_DATABASE_URL=postgresql://...neon...

    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

- **Продакшн (Cloud Run)**
  - Сервис: `ai-avatar` в проекте GCP `gen-lang-client-0202538697`.
  - Регион: `us-central1`.
  - Переменные окружения (минимально необходимые):
    - `GEMINI_API_KEY` — ключ Gemini для генерации ответов.
    - `NEON_DATABASE_URL` — полный DSN подключения к Neon (`postgresql://...`).
  - Образ: `gcr.io/GEN_LANG_PROJECT_ID/ai-avatar:latest`.
  - Деплой происходит через GitHub Actions (см. `.github/workflows/deploy-backend.yml`).

### 3. Работа с данными (Neon)

- **Источник данных по проектам**
  - Таблица `projects` в Neon — единый источник правды для:
    - кода проекта (`code`),
    - старого номера (`num_legacy`, если есть),
    - названия (`title`),
    - работодателя / клиента (`employer`, `client`),
    - временных рамок (`year_start`, `month_start`, `year_end`, `month_end`),
    - описаний:
      - Executive (`executive_md` — текст из `_projects/*.md`),
      - STAR (`star_situation`, `star_task`, `star_action`, `star_result`),
    - ключевого результата (`key_result`),
    - технологий (`technology`).

- **Теги**
  - `project_industries` — индустрии (источники: `client_side`, `my_side`).
  - `project_domains` — функциональные домены (`functional`).
  - `project_roles` — роли, в которых велась работа (`roles`).

- **Контакты**
  - Таблица `contacts` пополняется отдельно (приложение `apps/contacts` из Sam).
  - Backend не должен менять схему `contacts`, только читать и, при необходимости, добавлять новые поля _по согласованию_.

### 4. Правила для агента (что можно и нельзя)

#### 4.1. Что агент может делать

- Обновлять и расширять:
  - эндпоинты `app/main.py` (добавлять новые маршруты, фильтры, поля в JSON),
  - логику чтения из Neon (`app/db.py` и SQL‑запросы),
  - Jekyll‑шаблоны и страницы, если требуется отобразить новые поля/виды данных.
- Добавлять новые представления:
  - страницы/виджеты на сайте (например, новые витрины по индустриям/ролям),
  - дополнительные API‑методы (например, агрегированные статистики, поиск).
- Улучшать UX:
  - дополнять frontend `digital-avatar/frontend` (не ломая существующий контракт `/ws/chat`),
  - расширять документацию (`CLOUD_RESOURCES.md`, `ARCHITECTURE.md`, этот файл).

#### 4.2. Чего делать нельзя

- **Нельзя**:
  - коммитить в репозиторий реальные значения ключей/секретов:
    - `GEMINI_API_KEY`,
    - `NEON_DATABASE_URL`,
    - любые другие токены и пароли.
  - изменять параметры Cloud Run и Neon **напрямую** из кода (всё через переменные окружения и Terraform/консоль/Actions).
  - ломать или удалять существующие API‑маршруты, которые уже используются:
    - `/ws/chat`,
    - существующий фронтовый JavaScript (`digital-avatar/frontend/widget.js`).

- Изменения в схеме БД (Neon) агент должен:
  - описывать явно (миграции SQL),
  - согласовывать: новые таблицы/столбцы добавлять, не трогая действующие без крайней необходимости.

### 5. Потоки деплоя и CI/CD

- **Github Actions** (`.github/workflows/deploy-backend.yml`):
  - Триггеры:
    - `push` в ветки `main` и `test-minima` по путям:
      - `digital-avatar/backend/**`
      - `knowledge-base/**`
    - `workflow_dispatch` (ручной запуск).
  - Шаги:
    1. Checkout репозитория.
    2. Копирование `knowledge-base` в `digital-avatar/backend/knowledge_base`.
    3. Аутентификация в GCP через `secrets.GCP_SA_KEY`.
    4. Сборка и push Docker‑образа `gcr.io/${GCP_PROJECT_ID}/ai-avatar:latest`.
    5. Деплой в Cloud Run:
       - `--set-env-vars GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }},NEON_DATABASE_URL=${{ secrets.NEON_DATABASE_URL }}`.

- **Обязанности агента по CI/CD**:
  - следить, чтобы backend собирался и запускался локально перед пушем;
  - не вносить изменения, которые ломают совместимость workflow (пути, имена файлов, Dockerfile);
  - при добавлении новых зависимостей — обновлять `digital-avatar/backend/requirements.txt`.

### 6. Как агенту использовать этот backend для сайта и Sam

- Сайт:
  - может получать данные о проектах/контактах через backend‑API и использовать их при генерации страниц:
    - например, скрипт в `sources/` или `digital-avatar/scripts` может вычитывать `/api/projects` и пересобирать Jekyll‑страницы.

- Sam:
  - уже использует backend как источник проектов/контактов через:
    - `PROJECTS_API_BASE_URL_LOCAL` (локальный `http://localhost:8000`),
    - `PROJECTS_API_BASE_URL_CLOUD` (Cloud Run URL).
  - Агент, развивающий Sam, должен считать backend на Cloud Run **единым источником правды** для проектов/контактов.

### 7. Приоритеты развития (что делать в первую очередь)

1. Поддерживать стабильность существующих эндпоинтов:
   - `/`, `/ws/chat`, `/api/projects`, `/api/projects/{code}`, `/api/contacts`, `/api/contacts/{id}`.
2. Обеспечить согласованность данных:
   - коды проектов (`code`), номера (`num_legacy`), теги, контакты — один к одному с Neon и Sam.
3. Постепенно переводить Jekyll‑страницы на использование данных из Neon через backend (вместо «жёстко зашитых» списков).
4. Поддерживать документацию актуальной:
   - обновлять `CLOUD_RESOURCES.md`, `ARCHITECTURE.md` и `AGENT_WEBSITE_BACKEND.md` при существенных изменениях.

