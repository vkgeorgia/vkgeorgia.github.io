## AI Avatar Backend: разбор типичной проблемы деплоя

Этот файл описывает последовательность действий, если сервис `ai-avatar` на Cloud Run не поднимается (ошибка вида *“failed to start and listen on PORT=8080”* или `/api/projects` / `/api/contacts` возвращают `{"detail": "Not Found"}`).

### 1. Проверить, что ревизия вообще стартует

1. Открыть **Cloud Run → Services → ai-avatar**.
2. На вкладке **Revisions**:
   - зелёная галочка и `Traffic: 100%` у последней ревизии → контейнер стартует;
   - красный значок (ERROR) → контейнер падает при старте, смотреть логи.

Если ревизия не стартует:

1. Нажать **Logs** (или ссылку *Logs URL* из сообщения Cloud Run).
2. В фильтре выбрать:
   - *Resource type*: `Cloud Run Revision`,
   - *Service name*: `ai-avatar`,
   - *Revision name*: последняя ревизия (`ai-avatar-0003x-...`).
3. Найти запись с `Traceback (most recent call last)` и посмотреть причину.

Самый частый кейс: 

```text
File "/app/app/db.py", line 15, in <module>
  raise RuntimeError("NEON_DATABASE_URL is not set. Please configure it in the environment.")
RuntimeError: NEON_DATABASE_URL is not set. Please configure it in the environment.
```

### 2. Настроить NEON_DATABASE_URL в Cloud Run

Если в traceback видно `NEON_DATABASE_URL is not set`:

1. Войти в **Cloud Run → ai-avatar → Edit & deploy new revision**.
2. Пролистать до **Variables, Secrets & Connections** → блок **Environment variables**.
3. Добавить/проверить две переменные:
   - `GEMINI_API_KEY` — ключ Gemini.
   - `NEON_DATABASE_URL` — **полная строка подключения к Neon**, БЕЗ префикса `psql`, например:

     ```text
     postgresql://neondb_owner:...@ep-...neon.tech/neondb?sslmode=require
     ```

4. Нажать **Deploy** и дождаться, пока новая ревизия станет `Ready`.

> Важно: эту строку никогда не коммитить в репозиторий. Она должна храниться только в переменных окружения или секретах.

### 3. Убедиться, что образ содержит новые эндпоинты

Если ревизия зелёная, но `https://ai-avatar-...run.app/api/projects` или `/api/contacts` отвечают `{"detail":"Not Found"}`:

1. Проверить, что в `digital-avatar/backend/app/main.py` действительно есть:

   - `@app.get("/api/projects")`
   - `@app.get("/api/projects/{code}")`
   - `@app.get("/api/contacts")`
   - `@app.get("/api/contacts/{contact_id}")`

2. Убедиться, что GitHub Actions workflow `.github/workflows/deploy-backend.yml`:
   - собирает образ из `digital-avatar/backend`:

     ```bash
     cd digital-avatar/backend
     docker build -t gcr.io/${GCP_PROJECT_ID}/ai-avatar:latest .
     docker push gcr.io/${GCP_PROJECT_ID}/ai-avatar:latest
     ```

   - деплоит именно этот образ:

     ```bash
     gcloud run deploy ai-avatar \
       --image gcr.io/${GCP_PROJECT_ID}/ai-avatar:latest \
       --set-env-vars GEMINI_API_KEY=...,NEON_DATABASE_URL=...
     ```

3. Запустить workflow **Deploy AI Avatar Backend to Cloud Run** заново (через Actions → Run workflow).
4. После успешного запуска проверить:

   ```text
   https://ai-avatar-103512681014.us-central1.run.app/api/projects
   https://ai-avatar-103512681014.us-central1.run.app/api/contacts
   ```

   Ожидание — JSON со списками, а не `Not Found`.

### 4. Временный обход: использование стабильной ревизии

Пока новая ревизия не работает, можно использовать предыдущую стабильную:

1. На вкладке **Revisions** Cloud Run посмотреть, у какой ревизии статус зелёный и был трафик раньше (например, `ai-avatar-00032-bwt` с URL `https://ai-avatar-fgv7vwypqq-uc.a.run.app`).
2. В локальных клиентах (Sam‑UI, сайт) временно указывать именно этот URL как базовый backend:

   ```env
   PROJECTS_API_BASE_URL_CLOUD=https://ai-avatar-fgv7vwypqq-uc.a.run.app
   ```

3. После починки и успешного деплоя новой ревизии вернуться к «каноническому» URL `https://ai-avatar-103512681014.us-central1.run.app`.

### 5. Чек‑лист при следующем изменении backend’а

Перед пушем изменений в `digital-avatar/backend`:

1. Локально запустить backend:

   ```bash
   uvicorn app.main:app --reload
   ```

2. Убедиться, что локально работают:

   - `GET http://localhost:8000/`
   - `GET http://localhost:8000/api/projects`
   - `GET http://localhost:8000/api/contacts`

3. Только после этого пушить в `main` и запускать GitHub Actions деплой.

### 6. Логи разговоров в Neon (`chat_sessions` / `chat_messages`)

Backend пишет каждый ход WebSocket‑чата (`/ws/chat`) в PostgreSQL:

- `chat_sessions` — одна строка на подключение (время старта/окончания, опционально IP и `User-Agent`).
- `chat_messages` — пары «user» / «assistant» (текст сообщения).

**Первичная настройка (один раз):**

1. Открыть **Neon → SQL Editor**.
2. Выполнить скрипт из репозитория: `digital-avatar/backend/sql/chat_logs.sql`.

Если таблицы ещё не созданы, в логах Cloud Run могут появляться предупреждения вида `chat_log: create_session failed` — чат при этом продолжит работать, записи в БД просто не будут создаваться.

**Проверка:**

```sql
SELECT id, started_at, ended_at FROM chat_sessions ORDER BY started_at DESC LIMIT 5;
SELECT session_id, role, left(content, 80), created_at FROM chat_messages ORDER BY created_at DESC LIMIT 10;
```

### 7. Уведомления в Telegram после сессии чата

После закрытия WebSocket‑сессии backend отправляет **краткое** сообщение в Telegram (без полного текста диалога): `session_id`, число сообщений user/assistant, признак упоминания ссылки календаря в ответах ассистента, IP, время начала/конца.

**Что сделать один раз:**

1. Создать бота через **@BotFather**, получить **токен**.
2. Узнать **chat_id** (личный чат: напиши боту `/start`, затем открой `https://api.telegram.org/bot<TOKEN>/getUpdates` и найди `"chat":{"id":...}`).
3. В **GitHub → Settings → Secrets and variables → Actions** добавить:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID` (строка, для групп часто отрицательное число)
4. Убедиться, что workflow **Deploy AI Avatar Backend** передаёт их в Cloud Run (см. `.github/workflows/deploy-backend.yml` — переменные в `--set-env-vars`).
5. Запустить деплой backend’а заново.

**Отключить без удаления секретов:** в Cloud Run задать `TELEGRAM_NOTIFY_ENABLED=false`.

**Если сообщения не приходят:** смотреть логи Cloud Run на строки `telegram_notify:` (ошибки HTTP от Telegram API).

