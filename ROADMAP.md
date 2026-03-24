---
title: "Digital Avatar & Knowledge Base Roadmap"
---

## 1. Аудит текущей базы знаний

- [x] Зафиксировать актуальное состояние директорий `knowledge-base/`, `_projects/` и `digital-avatar/backend/knowledge_base/` (какие типы контента где лежат).
- [x] Выписать все скрипты, которые читают/пишут файлы в этих директориях (RAG, deploy‑скрипты, утилиты).
- [x] Определить, какие части текстовой базы реально используются аватаром и сайтом сейчас (по коду и по факту).

**Фактический минимальный набор, который сейчас нужен:**

- **Для сайта (Jekyll):**
  - `_projects/*.md` — подробные проектные кейсы (источник для `cases.md` и портфеля).
  - `knowledge-base/projects/*.md` — тематические страницы `projects/*.md` (aviation, retail и т.п.).
  - `knowledge-base/domains/*.md`, `knowledge-base/roles/*.md`, `knowledge-base/1. bio/bio.md`, `knowledge-base/2. education/*.md`, `knowledge-base/experience/ai-ml-experience.md` — контент страниц “Profile / Services / Domains / Roles”.
- **Для аватара (RAG):**
  - Всё из `knowledge-base/` (через sync в `digital-avatar/backend/knowledge_base/`).
  - `_projects/*.md` как длинные нарративы (через RAG и/или будущий импорт в Neon).
  - Корневые файлы репозитория: `profile.md`, `business-challenges.md`, `index.md` (подтягиваются явно в `RAGService`).

## 2. Разделение источников правды (SoT) — решение принято (Mar 2026)

**Зафиксированная архитектура:**
- **Neon — единственный источник истины для структурированных данных о проектах.** Все метаданные (industry, domain, role, employer, title, key_result, technology, даты, STAR-поля, executive_md) живут в таблице `projects`.
- **`_projects/*.md` — нарративный архив.** Нужен для RAG (длинные тексты) и как резерв. При расхождении с Neon — Neon главнее.
- **Нарративный контент сайта** (манифест, статьи, биография) живёт в markdown (`knowledge-base/`).

- [ ] Описать в `PROJECT_RULES.md` финальные правила: куда добавлять новый проект (сначала Neon, потом опционально `.md`).
- [ ] Настроить автоматическую синхронизацию: при пуше в `main` скрипт проверяет расхождения между frontmatter `_projects/*.md` и записями в Neon (консистентность).

**Вытекающая архитектура динамических страниц:**

Т.к. Neon — источник истины для проектов, страницы с описанием опыта по отраслям, доменам и ролям формируются автоматически из данных Neon и не требуют ручного обновления:

- При добавлении нового проекта в Neon → страница `/industries/retail`, `/domains/analytics`, `/roles/enterprise-architect` и т.п. автоматически показывают его.
- При изменении описания проекта → страницы пересчитываются сами.
- Ручное поддержание отдельных `.md`-файлов для каждой страницы опыта не нужно.

- [ ] Перевести все `industries/*.md`, `domains/*.md`, `roles/*.md` на паттерн из пилота `projects/retail.md`: тонкий Jekyll-шаблон + JS fetch к `/api/projects?industry=...` (или `domain=`, `role=`).
- [ ] Добавить на каждую такую страницу секцию "Суммарный опыт" — автоматически считать кол-во проектов, диапазон лет, топ технологий из Neon.
- [ ] Обеспечить, что поля `industry`, `domain`, `role` в Neon покрывают все существующие фильтры на `cases.md`.

## 3. “Диета” для `knowledge-base/` и `_projects/`

- [ ] Оставить в `knowledge-base/` только:
  - [ ] Манифест / профиль (`profile.md`, `business-challenges.md`, ключевые страницы сайта).
  - [ ] Тематические статьи и заметки (Field Notes / System Design).
- [ ] В `_projects/` оставить проектные кейсы как длинные нарративы (Single Source of Truth для текстов).
- [ ] Перенести в `0. archive` все устаревшие/дублирующие текстовые материалы, которые не используются ни сайтом, ни аватаром.

## 3.1. Динамические страницы по индустриям / доменам / ролям

- [x] Выбрать архитектуру: тонкие Jekyll‑страницы + фронтенд через JS, дергающий `/api/projects`.
- [x] Обновить layout `page` так, чтобы он пробрасывал в `<body>` тип страницы и ключ фильтра (`page_type`, `page_key`).
- [x] Создать общий скрипт `assets/js/projects-dynamic.js`, который по `page_type/page_key` делает `fetch` к backend’у и рендерит список проектов.
- [x] Перевести пилотную страницу `projects/retail.md` на динамическую модель (без захардкоженного списка проектов).
- [x] Масштабировать паттерн на все `industries/*.md` (8 отраслей) и `domains/*.md` (11 доменов) — выполнено Mar 2026.
- [x] Добавить на каждой странице блок "Суммарный опыт": кол-во проектов, диапазон лет, список ключевых технологий — `assets/projects-dynamic.js` — выполнено Mar 2026.
- [x] Масштабировать паттерн на `roles/*.md` — выполнено Mar 2026.

## 4. Перенос метаданных проектов и контактов в Neon — выполнено (Mar 2026)

- [x] Junction-таблицы `project_industries`, `project_domains`, `project_roles` покрывают все 44 проекта.
- [x] API-фильтры `/api/projects?industry=`, `?domain=`, `?role=` переведены на slug-subquery (не text-match по колонке).
- [x] Страницы `industries/`, `domains/`, `roles/` синхронизированы со slug-справочником в Neon (добавлены 3 недостающих industry-страницы, 9 domain-страниц, 3 новые role-страницы; исправлены 3 несовпадавших `page_key`; удалены 4 orphan-страницы).
- [ ] Настроить автоматическую проверку консистентности `_projects/*.md` ↔ Neon (не выполнено).

## 5. RAG и загрузка знаний — выполнено (Mar 2026)

- [x] `RAGService` упрощён: удалён мёртвый код Google Drive, pdfplumber, python-docx (574 → 304 строки).
- [x] Читает только `.md`/`.txt` из `knowledge_base/` + корневые `profile.md`, `business-challenges.md`, `index.md`.
- [x] `requirements.txt` очищен от неиспользуемых зависимостей (`pdfplumber`, `python-docx`, `google-api-python-client` и т.п.).

## 6. Чистка и архивирование скриптов — выполнено (Mar 2026)

- [x] Устаревшие скрипты перемещены в `0. archive/`: `fix_kb_metadata.py`, `test_avatar.py`, `did_service.py`.
- [x] Актуальный скрипт генерации эмбеддингов: `scripts/generate_embeddings.py`.

## 7. Наблюдение и эволюция

- [ ] Добавить короткий чек‑лист “перед изменениями backend’а и знания” (линк из `AI_AVATAR_BACKEND_TROUBLESHOOTING.md`).
- [ ] Раз в квартал проводить мини‑аудит: какие новые типы данных появились и должны ли они жить в Neon или в markdown.
- [ ] При необходимости добавить новые таблицы в Neon (например, `leads`, `offers`) и прописать их связь с текстовой базой.
- [x] Сессии чата в Neon: таблицы `chat_sessions` / `chat_messages` (см. §9).

## 8. Укрепление backend после код‑ревью (Mar 2026) — выполнено

- [x] Исправить повреждённый YAML frontmatter в `assets/main.scss` (корректные `---` + `@import "minima";`).
- [x] Сделать фильтры `GET /api/projects` регистронезависимыми для полей `industry`, `domain`, `employer`, `role` (`LOWER(...) = LOWER(%s)`).
- [x] Удалить временный диагностический эндпоинт `/debug/routes` из production‑кода.
- [x] Обновить `PROJECT_STATUS.md`: дата, блок про стабилизацию Neon/API/деплоя и исправление SCSS.

## 9. Логи разговоров в БД и уведомления в Telegram

### 9.1. Запись логов чата в Neon — выполнено (код + репозиторий)

- [x] SQL‑схема: `digital-avatar/backend/sql/chat_logs.sql` — таблицы `chat_sessions`, `chat_messages`, индексы.
- [x] Модуль `digital-avatar/backend/app/chat_log.py`: создание сессии, запись сообщений (`user` / `assistant`), закрытие сессии (`ended_at`).
- [x] Интеграция в WebSocket `/ws/chat` в `app/main.py`: логирование каждого хода; вызовы БД через `asyncio.to_thread`, чтобы не блокировать event loop.
- [x] При отсутствии таблиц в Neon — best‑effort: предупреждения в логах, чат продолжает работать.
- [x] Документация: раздел **§6** в `AI_AVATAR_BACKEND_TROUBLESHOOTING.md` (как применить SQL и проверить данные).
- [x] Docker: `COPY sql/ ./sql/` в `digital-avatar/backend/Dockerfile`, чтобы скрипт миграции был в образе для справки.

### 9.2. Операционный шаг (один раз на окружение)

- [x] Выполнить `sql/chat_logs.sql` в **Neon SQL Editor** для боевой БД.

### 9.3. Telegram — уведомления о завершённой сессии

- [x] Создать бота в Telegram, получить токен; задать секреты **`TELEGRAM_BOT_TOKEN`** и **`TELEGRAM_CHAT_ID`** в GitHub Actions (прокидываются в Cloud Run через `deploy-backend.yml`).
- [x] После завершения сессии чата отправлять в Telegram **краткое уведомление**: `session_id`, счётчики user/assistant, IP, время начала/конца, признак упоминания ссылки календаря в ответах ассистента (без полного лога — приватность).
- [x] Опционально отключать уведомления переменной **`TELEGRAM_NOTIFY_ENABLED=false`**.
- [ ] **Встречи (продвинуто):** интеграция с **Google Calendar API** для фактически созданных слотов (сейчас только эвристика по тексту ответа).

---

## 10. Архитектурные улучшения backend (из код-ревью Mar 2026)

### 10.1. Connection pooling для Neon — выполнено (Mar 2026)

**Проблема:** каждый HTTP-запрос и шаг WebSocket открывает новое соединение с Neon (~100–300 ms cold-start на Serverless Postgres).

- [x] Заменить `get_db_connection()` в `app/db.py` на `psycopg_pool.ConnectionPool`.
- [x] Настроить `min_size=1`, `max_size=5`.
- [x] Пул инициализируется при старте FastAPI через `lifespan` context manager.
- [x] `psycopg-pool` добавлен в `requirements.txt`.

### 10.2. История разговора в контексте Gemini — выполнено (Mar 2026)

**Проблема:** `generate_response(data)` получал только последнее сообщение. ИИ не помнил предыдущих ходов.

- [x] Накапливать историю per-session в памяти в `chat.py` WebSocket-хэндлере.
- [x] Передавать историю в `generate_response(query, history=history)` и включать в промпт к Gemini.
- [x] Глубина истории ограничена `MAX_HISTORY_TURNS=10` (последние 20 сообщений).

### 10.3. Разбить `main.py` на FastAPI routers — выполнено (Mar 2026)

**Проблема:** один файл содержал WebSocket-чат, REST API проектов, REST API контактов и диагностические эндпоинты.

- [x] Выделен `app/routers/chat.py` — `/ws/chat`.
- [x] Выделен `app/routers/projects.py` — `/api/projects`, `/api/projects/{code}`.
- [x] Выделен `app/routers/contacts.py` — `/api/contacts`, `/api/contacts/{contact_id}`.
- [x] Выделен `app/routers/health.py` — `/api/health`, `/api/internal/telegram-test`, `/`.
- [x] Добавлен `app/deps.py` — singleton `RAGService`.
- [x] Роутеры зарегистрированы в `main.py` через `app.include_router(...)`.

### 10.4. Векторный поиск (pgvector) для RAG — выполнено (Mar 2026)

- [x] Расширение `pgvector` включено в Neon; таблица `knowledge_chunks (id, content, embedding vector(768), source, chunk_index)` создана с HNSW-индексом.
- [x] `scripts/generate_embeddings.py` — генерирует эмбеддинги через Gemini Embedding API (`gemini-embedding-001`, REST v1beta) и делает upsert в `knowledge_chunks`. Запускается в GitHub Actions при каждом деплое.
- [x] 587 чанков загружено (88 из проектов в Neon + 499 из файлов KB).
- [x] `RAGService._vector_select_context()` — косинусный поиск `ORDER BY embedding <=> %s::vector LIMIT 8`.
- [x] `RAGService._select_context()` — keyword-fallback сохранён.
- [x] `RAGService._check_vector_search()` — автодетект: если `knowledge_chunks` пустая или Neon недоступен, используется keyword-fallback.

---

## 11. Code Review — Security & Quality Hardening (Mar 2026)

Результат code review бэкенда. Три волны приоритетности.

### 11.1. Волна 1 — Быстрые фиксы — выполнено (Mar 2026)

#### Безопасность
- [x] `resume.py`: заменить `!=` на `hmac.compare_digest()` для сравнения API-ключа (timing attack)
- [x] `health.py`: то же для `TELEGRAM_DIAG_SECRET`

#### Стабильность
- [x] `chat.py`: trim истории делать **до** `append` — история теперь строго ≤ `MAX_HISTORY_TURNS * 2`
- [x] `deploy-backend.yml`: добавить health check шаг после деплоя (5 попыток × 10s)

#### Размер образа
- [x] `Dockerfile`: убрать `gcc` — не нужен при `psycopg[binary]`

### 11.2. Волна 2 — Безопасность и надёжность

#### Безопасность
- [ ] `contacts.py`: `/api/contacts` публичный — отдаёт всю базу контактов без аутентификации; добавить `x-api-key` как в `resume.py`
- [ ] `rag_service.py`: user query вставляется в промпт plain string — возможен prompt injection; перейти на структурированный `contents=[{"role": "user", "content": query}]`
- [ ] `chat.py`: URL-валидация не блокирует Unicode homograph атаки (`gооgle.com` с кириллицей); добавить IDNA-нормализацию домена

#### Надёжность
- [ ] `rag_service.py`: добавить timeout на вызов Gemini API — сейчас WebSocket зависает при медленном ответе
- [ ] `telegram_notify.py`: добавить exponential backoff retry (до 3 попыток) при временной недоступности Telegram API
- [ ] `resume_service.py`: при невалидном JSON от LLM — silent fallback без уведомления пользователя; добавить явную обработку

#### Зависимости
- [ ] `requirements.txt`: добавить верхние границы версий (`>=X,<X+1`) — сейчас мажорный апгрейд может сломать прод-билд

### 11.3. Волна 3 — Качество кода

- [ ] `projects.py`: добавить пагинацию (`limit` + `offset`) — сейчас `/api/projects` отдаёт все записи без лимита
- [ ] `projects.py`, `contacts.py`: добавить валидацию slug/search параметров (только `[a-z0-9-]`, max length)
- [ ] `deps.py`: `RAGService` инициализируется при импорте до старта пула — перенести инициализацию в `lifespan`
- [ ] `generate_embeddings.py`: добавить checkpoint/resume — при падении скрипт стартует с нуля
- [ ] `generate_embeddings.py`: заменить линейный retry на exponential backoff
- [ ] `Dockerfile`: заменить `python:3.12-slim` на конкретный патч-версию (`python:3.12.9-slim`) для воспроизводимых сборок
- [ ] Вынести `"gemini-2.5-flash"` в константу — имя модели дублируется в `rag_service.py` и `resume_service.py`
