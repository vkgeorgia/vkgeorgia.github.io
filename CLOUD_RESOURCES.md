# Cloud Resources: AI Avatar & Website

Этот файл описывает облачные ресурсы Google Cloud Platform (GCP), используемые для обеспечения работы ИИ-аватара на сайте **vkgeorgia.github.io**.

## 🚀 Общая информация
*   **Имя проекта:** Digital Avatar
*   **Project ID:** `gen-lang-client-0202538697`
*   **Статус:** Активен

## 🏗 Характеристики ИИ-аватара (Cloud Run)
*   **Сервис:** `ai-avatar`
*   **Регион:** `us-central1`
*   **URL:** [https://ai-avatar-103512681014.us-central1.run.app](https://ai-avatar-103512681014.us-central1.run.app)
*   **Технологии:** FastAPI (Python), WebSockets для связи в реальном времени.

## 🤖 Интеграция с Gemini
*   **API:** Использует `Generative Language API`.
*   **Модель:** `gemini-2.5-flash` для генерации ответов на основе M-Shape философии и базы знаний.
*   **Хранилище:** `gs://gen-lang-client-0202538697_cloudbuild/` для сборки.

---
*Примечание: Статический контент сайта хостится на GitHub Pages. Cloud Run используется только для динамической логики аватара.*
