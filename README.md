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

The avatar uses:
- Google Gemini AI for natural language understanding
- RAG (Retrieval-Augmented Generation) with my professional knowledge base
- Real-time WebSocket communication

[Learn more about the Digital Avatar project →](digital-avatar/)

</p>

## Project Structure & Data Sources

To avoid confusion between website content and AI knowledge base:

1.  **`_projects/`**
    *   **Purpose**: The **Single Source of Truth** for the project portfolio.
    *   **Usage**: Jekyll reads this directory to generate the `Cases` page. The AI avatar also learns from these files.
    *   **Rule**: Always edit project descriptions here.

2.  **`knowledge-base/`**
    *   **Purpose**: Stores general knowledge (bio, education, articles, domains).
    *   **Usage**: Used by the AI avatar for context.
    *   **Rule**: Do **NOT** put project files here (duplicate).

3.  **`digital-avatar/backend/knowledge_base/`**
    *   **Purpose**: The actual folder the AI reads at runtime.
    *   **Usage**: This is **automatically populated** during deployment.
    *   **Rule**: Do **NOT** edit files here manually; they will be overwritten by `deploy.sh`.

### Data Flow
`_projects` + `knowledge-base`  --> [deploy.sh] --> `digital-avatar/backend/knowledge_base` --> [Docker Image]
