---
layout: page
title: "Cases"
seo_title: "Cases | Enterprise Architecture & Technology Advisory"
description: "Selected engagements in enterprise architecture, technology strategy, and transformation — across aviation, energy, financial services, telecom, and IT services. Filter by industry, role, and functional domain."
keywords: "Enterprise Architecture Cases, Transformation Case Studies, Reorganization, M&A Integration, Cost Optimization, AI Adoption, Digital Transformation Portfolio"
lang: en
permalink: /cases/
---

Engagements from my practice, grouped around the kinds of decisions they involved — not the tools or frameworks used. Each card opens to a structured view: context, the decision challenge, constraints and trade-offs, the architectural or strategic perspective applied, and the outcome.

Most cases fall into one of two patterns:

- **BUILD** — launching a new business unit, product, or platform from zero, and designing the structure that lets it scale.
- **FIX** — restoring order after M&A, reorganization, or accumulated complexity: cost, risk, legacy exposure, or operational drag.

In practice, most engagements sit on the boundary between the two.

Use the filters below to narrow by industry, role, or functional domain.

**[→ Book a 30-min intro call](https://calendar.app.google/YwmXZytfSQ2qWX4Z7)**

---

## Featured case studies

A few engagements in depth — the decision, the trade-offs, and the outcome.

<div class="featured-cases">
{% assign featured = site.case_studies | sort: "order" %}
{% for case in featured %}
  <div class="featured-case">
    <h3><a href="{{ case.url | relative_url }}">{{ case.title }}</a></h3>
    {% if case.client_display %}<p class="featured-case-client">{{ case.client_display }}</p>{% endif %}
    <p class="featured-case-teaser">{{ case.teaser }}</p>
    <p class="featured-case-more"><a href="{{ case.url | relative_url }}">Read the case →</a></p>
  </div>
{% endfor %}
</div>

---

## Other engagements

The full list, with filters by industry, role, and functional domain, is below.

<style>
  /* Filter Container */
  .filter-section {
    margin-bottom: 30px;
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #e9ecef;
  }
  
  .filter-group {
    margin-bottom: 15px;
  }
  
  .filter-group:last-child {
    margin-bottom: 0;
  }

  .filter-label {
    font-weight: 600;
    font-size: 0.85em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #6c757d;
    margin-bottom: 8px;
    display: block;
  }

  /* Filter Buttons */
  .filter-btn {
    background: white;
    border: 1px solid #ced4da;
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 0.85em;
    margin: 0 5px 5px 0;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #495057;
  }

  .filter-btn:hover {
    background: #e9ecef;
    border-color: #adb5bd;
  }

  .filter-btn.active {
    background: #007bff;
    color: white;
    border-color: #007bff;
  }

  .filter-btn.clear-all {
    background: #dc3545;
    color: white;
    border-color: #dc3545;
  }

  /* Project Cards */
  .project-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .project-card {
    border: 1px solid #dee2e6;
    border-radius: 6px;
    overflow: hidden;
    background: white;
    transition: box-shadow 0.2s;
  }
  
  .project-card:hover {
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  }

  .project-card[hidden] {
    display: none;
  }

  .project-summary {
    padding: 15px;
    cursor: pointer;
    list-style: none; /* Hide default triangle */
    background: #fff;
    position: relative;
  }

  .project-summary::-webkit-details-marker {
    display: none;
  }

  .project-summary h3 {
    margin: 0;
    font-size: 1.1em;
    color: #212529;
    padding-right: 30px;
  }

  .project-meta {
    font-size: 0.85em;
    color: #6c757d;
    margin-top: 5px;
  }

  .project-content {
    border-top: 1px solid #f1f3f5;
    padding: 20px;
    background: #fff;
  }
  
  .project-content h1 { font-size: 1.5em; border-bottom: 2px solid #eee; padding-bottom: 10px; }
  .project-content h2 { font-size: 1.2em; color: #495057; margin-top: 20px; }
  .project-content p { color: #333; line-height: 1.6; }

  /* Plus icon for summary */
  .project-summary::after {
    content: '+';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.5em;
    color: #ced4da;
    font-weight: 300;
  }

  details[open] .project-summary::after {
    content: '-';
  }
  
  .project-count-label {
    font-size: 0.9em;
    color: #6c757d;
    margin-bottom: 10px;
  }
</style>

<div class="filter-section">
  <!-- Reset -->
  <div style="margin-bottom: 15px;">
    <button class="filter-btn clear-all" onclick="filterProjects('all')">Reset Filters</button>
    <span id="count-display" style="margin-left: 10px; font-size: 0.9em; color: #666;">Showing all projects</span>
  </div>

  <div class="filter-row">
    <!-- Industry -->
    <div class="filter-group">
      <span class="filter-label">Industry</span>
      {% assign industries = site.projects | map: "client_side_industry" | flatten | uniq | sort %}
      {% for item in industries %}
        <button class="filter-btn" data-filter-type="industry" data-value="{{ item }}" onclick="toggleFilter(this, 'industry', '{{ item }}')">{{ item }}</button>
      {% endfor %}
    </div>

    <!-- Functional Domain -->
    <div class="filter-group">
      <span class="filter-label">Functional Domain</span>
      {% assign functionals = site.projects | map: "functional" | flatten | uniq | sort %}
      {% for item in functionals %}
        <button class="filter-btn" data-filter-type="functional" data-value="{{ item }}" onclick="toggleFilter(this, 'functional', '{{ item }}')">{{ item | replace: '-', ' ' }}</button>
      {% endfor %}
    </div>

    <!-- Role -->
    <div class="filter-group">
      <span class="filter-label">Role</span>
      {% assign roles = site.projects | map: "roles" | flatten | uniq | sort %}
      {% for item in roles %}
        <button class="filter-btn" data-filter-type="role" data-value="{{ item }}" onclick="toggleFilter(this, 'role', '{{ item }}')">{{ item | replace: '-', ' ' | capitalize }}</button>
      {% endfor %}
    </div>
  </div>
</div>

<div class="project-list" id="project-list">
  {% for project in site.projects reversed %}
    <details class="project-card"
             data-industry="{{ project.client_side_industry | join: ',' }}"
             data-functional="{{ project.functional | join: ',' }}"
             data-role="{{ project.roles | join: ',' }}">
      <summary class="project-summary">
        <h3>{{ project.title }}</h3>
        <div class="project-meta">
          <strong>Industry:</strong> {{ project.client_side_industry | join: ', ' }} |
          <strong>Role:</strong> {{ project.roles | join: ', ' | replace: '-', ' ' | capitalize }}
        </div>
      </summary>
      <div class="project-content">
        {{ project.content | markdownify }}
      </div>
    </details>
  {% endfor %}
</div>

<script>
  let activeFilters = {
    industry: [],
    functional: [],
    role: []
  };

  function toggleFilter(btn, type, value) {
    // Toggle active class
    btn.classList.toggle('active');
    
    // Update state
    const index = activeFilters[type].indexOf(value);
    if (index === -1) {
      activeFilters[type].push(value);
    } else {
      activeFilters[type].splice(index, 1);
    }
    
    applyFilters();
  }

  function filterProjects(action) {
    if (action === 'all') {
      // Clear state
      activeFilters = { industry: [], functional: [], role: [] };
      // Remove all active classes
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    }
    applyFilters();
  }

  function applyFilters() {
    const cards = document.querySelectorAll('.project-card');
    let visibleCount = 0;

    cards.forEach(card => {
      const cardInd = card.dataset.industry.split(',');
      const cardFunc = card.dataset.functional.split(',');
      const cardRole = card.dataset.role.split(',');

      // Check if card matches ALL active filter categories (AND logic between categories, OR within category)
      const matchIndustry = activeFilters.industry.length === 0 || activeFilters.industry.some(f => cardInd.includes(f));
      const matchFunc = activeFilters.functional.length === 0 || activeFilters.functional.some(f => cardFunc.includes(f));
      const matchRole = activeFilters.role.length === 0 || activeFilters.role.some(f => cardRole.includes(f));

      if (matchIndustry && matchFunc && matchRole) {
        card.removeAttribute('hidden');
        visibleCount++;
      } else {
        card.setAttribute('hidden', '');
      }
    });

    // Update counter
    const total = cards.length;
    const text = visibleCount === total ? `Showing all ${total} projects` : `Showing ${visibleCount} of ${total} projects`;
    document.getElementById('count-display').innerText = text;
  }
</script>
