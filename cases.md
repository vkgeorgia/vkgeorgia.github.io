---
layout: page
title: "Cases"
seo_title: "Cases | Enterprise Architecture & Technology Advisory"
description: "Selected engagements in enterprise architecture, technology strategy, and transformation — across aviation, retail, manufacturing, energy, telecom, and financial services. Three detailed studies plus a full track record."
keywords: "Enterprise Architecture Cases, Transformation Case Studies, Reorganization, M&A Integration, Cost Optimization, AI Adoption, Digital Transformation Portfolio"
lang: en
permalink: /cases/
---

Engagements from my practice, grouped around the kinds of decisions they involved — not the tools or frameworks used.

Most cases fall into one of two patterns:

- **BUILD** — launching a new business unit, product, or platform from zero, and designing the structure that lets it scale.
- **FIX** — restoring order after M&A, reorganization, or accumulated complexity: cost, risk, legacy exposure, or operational drag.

In practice, most engagements sit on the boundary between the two.

**[→ Book a 30-min intro call](https://calendar.app.google/YwmXZytfSQ2qWX4Z7)**

---

## Featured engagements

Three studies that show how the work plays out end to end — the decision, the trade-offs, and the outcome.

<div class="featured-cases">
  {% assign featured = site.case_studies | sort: "order" %}
  {% for case in featured %}
  <a class="featured-card" href="{{ case.url | relative_url }}">
    <span class="featured-tag">{{ case.engagement_type }}</span>
    <h3>{{ case.title | escape }}</h3>
    <p class="featured-client">{{ case.client_alt | escape }}</p>
    <p class="featured-meta">{{ case.period | escape }}</p>
    <p class="featured-teaser">{{ case.teaser | escape }}</p>
    <span class="featured-link">Read the case →</span>
  </a>
  {% endfor %}
</div>

---

## Other engagements

A condensed view of the broader track record — one line each, most recent first.

<details class="other-engagements">
  <summary>Show the full list ({{ site.data.other_engagements | size }} engagements)</summary>
  <ul class="engagement-list">
    {% for e in site.data.other_engagements %}
    <li>
      <span class="eng-period">{{ e.period }}</span>
      <span class="eng-sector">{{ e.industry }} · {{ e.client }}</span>
      <span class="eng-outcome">{{ e.outcome }}</span>
    </li>
    {% endfor %}
  </ul>
</details>

<p class="cases-note" markdown="1">
Most engagements are rendered with neutral, industry-level descriptors rather than client names. Where you need specifics for a relevant decision, [ask my assistant](javascript:void(0)) or [book a call](https://calendar.app.google/YwmXZytfSQ2qWX4Z7).
</p>

<style>
  /* Featured cards */
  .featured-cases {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 18px;
    margin: 24px 0;
  }
  .featured-card {
    display: flex;
    flex-direction: column;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    background: #fff;
    text-decoration: none;
    color: inherit;
    transition: box-shadow 0.2s, transform 0.2s, border-color 0.2s;
  }
  .featured-card:hover {
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    transform: translateY(-2px);
    border-color: #adb5bd;
  }
  .featured-tag {
    align-self: flex-start;
    font-size: 0.7em;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #007bff;
    border: 1px solid #007bff;
    border-radius: 4px;
    padding: 2px 8px;
    margin-bottom: 12px;
  }
  .featured-card h3 { margin: 0 0 6px; font-size: 1.15em; line-height: 1.3; color: #212529; }
  .featured-client { margin: 0 0 2px; font-weight: 600; color: #495057; font-size: 0.95em; }
  .featured-meta { margin: 0 0 12px; font-size: 0.82em; color: #6c757d; }
  .featured-teaser { margin: 0 0 16px; font-size: 0.92em; line-height: 1.55; color: #333; flex-grow: 1; }
  .featured-link { font-weight: 600; color: #007bff; font-size: 0.9em; }

  /* Other engagements list */
  .other-engagements {
    border: 1px solid #e9ecef;
    border-radius: 8px;
    background: #f8f9fa;
    padding: 0 18px;
    margin: 16px 0;
  }
  .other-engagements summary {
    cursor: pointer;
    font-weight: 600;
    color: #495057;
    padding: 16px 0;
    list-style: none;
  }
  .other-engagements summary::-webkit-details-marker { display: none; }
  .other-engagements summary::before { content: "▸ "; color: #adb5bd; }
  .other-engagements[open] summary::before { content: "▾ "; }
  .engagement-list { list-style: none; margin: 0 0 16px; padding: 0; }
  .engagement-list li {
    padding: 12px 0;
    border-top: 1px solid #e9ecef;
    display: grid;
    grid-template-columns: 80px 1fr;
    gap: 2px 14px;
    align-items: baseline;
  }
  .eng-period { grid-row: span 2; font-size: 0.82em; color: #6c757d; font-weight: 600; }
  .eng-sector { font-weight: 600; color: #343a40; font-size: 0.9em; }
  .eng-outcome { grid-column: 2; color: #495057; font-size: 0.9em; line-height: 1.5; }
  .cases-note { font-size: 0.88em; color: #6c757d; margin-top: 24px; }

  @media (max-width: 600px) {
    .engagement-list li { grid-template-columns: 1fr; }
    .eng-period { grid-row: auto; }
    .eng-outcome { grid-column: 1; }
  }
</style>
