# Cloud Resources & Configuration

This document lists the Google Cloud and Google AI Studio resources used for this project (Website + AI Avatar).

## Google Cloud Platform (GCP)

| Resource Type | Name / URI | Project ID | Location / Region | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Project** | [gen-lang-client-0202538697](https://console.cloud.google.com/home/dashboard?project=gen-lang-client-0202538697) | `gen-lang-client-0202538697` | - | Primary project for backend hosting |
| **Cloud Run** | `ai-avatar` | `gen-lang-client-0202538697` | `us-central1` | Hosts the FastAPI backend for the AI Avatar |
| **Container Registry** | `gcr.io/gen-lang-client-0202538697/ai-avatar` | `gen-lang-client-0202538697` | - | Stores Docker images for deployment |
| **Cloud Build** | - | `gen-lang-client-0202538697` | - | (Implicitly used by GCR/Cloud Run) |

## Google AI Studio (Gemini)

| Resource Type | Resource Detail | Purpose |
| :--- | :--- | :--- |
| **Gemini API Key** | `AIzaSy...dt0` | Authentication for Generative AI requests |
| **Model** | `gemini-2.5-flash` | The LLM powering the RAG (Retrieval-Augmented Generation) |
| **Service** | Google AI SDK (`google-generativeai`) | Interaction with Gemini models |

## Other Services

| Service | Detail | Purpose |
| :--- | :--- | :--- |
| **GitHub Pages** | `vkgeorgia.github.io` | Hosts the static frontend of the personal website |
| **Google Drive API** | (Optional Integration) | Configured in `rag_service.py` to pull extra knowledge if needed |

---
**Note:** API keys and credentials should be managed via environment variables (like `GEMINI_API_KEY`) and not committed directly to version control.
