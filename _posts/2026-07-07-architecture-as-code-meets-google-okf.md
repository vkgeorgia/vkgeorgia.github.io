---
title: "When Architecture-as-Code Meets Google's Open Knowledge Format"
standfirst: "Notes from the first adoption — an ArchiMate-typed graph in YAML, enterprise knowledge in OKF, and an agent doing the ingestion."
description: "How Google's Open Knowledge Format fits an architecture-as-code repository — canon, knowledge, codex — what it makes easy, and what it does not replace."
lang: en
---

You need to automate enterprise architecture management. Where does a typical enterprise architect at a mid-size company start? They need to gather information about their company. Naturally, they'll gather all their existing Visio and Draw.io diagrams into a single repository and try to organize them.

Architectural repositories created in the traditional way are clunky and ineffective. Let's look at how our developer colleagues manage their codebases. They use a version control system—it's cheap and reliable. They always know who made a change, why, and who approved it. It's easy to create a change approval workflow, and it's practically free. But how can we provide similar convenience for an enterprise architecture repository?

We need to store two types of documents: a structured portion—objects and relationships—and an unstructured portion—organizational documents, interview results, and meeting minutes. I used to store the unstructured portion in .md format with front matter so it could be displayed on GitHub Pages. But Google's Open Knowledge Format specification was recently released—it's perfect for enterprise knowledge storage, and I immediately decided to put it into practice.

In my work, I use a simple approach: there's no need to invent a new enterprise metamodel—one already exists in ArchiMate notation. We use it as a basis and build the enterprise knowledge base as a multidimensional graph of objects and relationships, with the ontology defined by ArchiMate. Everyone knows ArchiMate, so there's nothing new to learn. I store objects and relationships as primitives in YAML, and knowledge in Markdown files in OKF format.

I'm currently helping colleagues create an enterprise architecture repository—a chance to apply this approach with Google's OKF and build a true enterprise knowledge graph on text formats and AI agents. The repository has several parts: Canon (canonical objects and relationships, ArchiMate-typed), Knowledge (enterprise knowledge in OKF), Codex (internal and external rules), plus Operation, Field, and Intake. An agent runs the ingestion: it parses each incoming document, extracts the objects and relationships, and files them—documents to Knowledge, laws and standards to Codex, objects to Canon. Views are generated projections onto the graph (just like in Archi), stored as text in PlantUML or Mermaid, so you can see the model from any perspective.

How did OKF help? It lets you organize not only objects and relationships, but also enterprise documents and quickly build a knowledge base you can query with an agent—essentially, talk to your enterprise model and get answers about your business. An OKF knowledge graph won't replace a real RAG, but it's fast, accessible, and lets you build a POC and get a taste of working with an enterprise knowledge graph.

If you're interested in how the methodology works, it is open at transitrix.com; you can use ready-made implementation patterns and get a quick start.
