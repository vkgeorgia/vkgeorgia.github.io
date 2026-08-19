---
layout: page
title: "Articles"
seo_title: "Articles & Insights - Enterprise Architecture & Business Consulting"
description: "Thought leadership articles on enterprise architecture, digital transformation, TOGAF, and business consulting. Practical insights from 20+ years of cross-industry experience."
keywords: "Enterprise Architecture articles, TOGAF insights, Digital Transformation blog, Business Consulting, IT Strategy articles, ArchiMate best practices"
lang: en
permalink: /articles/
---

## Field Notes & System Design

I write about what actually works (and what fails) when building and fixing complex organizations.
No academic theory—just observations from the trenches of Enterprise Architecture, Crisis Management, and System Launching.

---

<ul class="article-list">
  {% for post in site.posts %}
  <li class="article-item">
    <span class="article-item-date">{{ post.date | date: "%B %-d, %Y" }}</span>
    <span class="article-item-body">
      <a class="article-item-title" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
      <p class="article-item-standfirst">{{ post.standfirst | escape }}</p>
    </span>
  </li>
  {% endfor %}
</ul>

<style>
  .article-list { list-style: none; margin: 24px 0; padding: 0; }
  .article-item {
    display: grid;
    grid-template-columns: 130px 1fr;
    gap: 4px 20px;
    padding: 16px 0;
    border-top: 1px solid #e9ecef;
    align-items: baseline;
  }
  .article-item:first-child { border-top: none; }
  .article-item-date { font-size: 0.82em; color: #6c757d; font-weight: 600; }
  .article-item-title { font-weight: 600; font-size: 1.05em; }
  .article-item-standfirst { margin: 4px 0 0; color: #495057; font-size: 0.92em; line-height: 1.5; }

  @media (max-width: 600px) {
    .article-item { grid-template-columns: 1fr; }
  }
</style>

---

## Facing a business challenge? Let's solve it.

Whether you're planning a reorganization, facing operational inefficiencies, or exploring IT-enabled growth, I help companies like yours find clear, practical solutions.

**[→ Book a 30-min architecture conversation]({{ site.cta_url }})**
