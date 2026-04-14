---
layout: page
title: "Cases"
seo_title: "Project Portfolio & Case Studies - Enterprise Architecture Projects"
description: "Browse 44+ enterprise architecture projects across Retail, Finance, Healthcare, Telecom, and Oil & Gas industries. Explore detailed project descriptions, architecture approaches, and implementation outcomes."
keywords: "Enterprise Architecture projects, TOGAF projects, ArchiMate diagrams, Business Transformation case studies, IT Strategy projects, Digital Transformation portfolio"
lang: en
permalink: /cases/
---

Browse my project portfolio organized by industry, role, and functional domain. Each project includes detailed context, decision challenges, architectural perspectives, and measurable outcomes.

---

## Operational Philosophy: Build & Fix

My portfolio is a history of **entropy reduction**.

I do not just "manage projects." I intervene to:
1.  **BUILD**: Launch new systems, products, and capabilities from zero to one (The Launcher).
2.  **FIX**: Stabilize chaotic environments, restructure failing processes, and stop bleeding (The Crisis Manager).

In every case below, the outcome is the same: **order is established, and the system becomes capable of running without me.**

---

## Project Portfolio

Browse my portfolio of **entropy reduction**. 

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
