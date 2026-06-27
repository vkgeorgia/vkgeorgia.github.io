---
layout: case
title: "Architecting the shift from equipment sales to a subscription business"
seo_title: "Subscription Business-Model Transformation — Enterprise Architecture Case Study"
description: "How an enterprise architect designed the subscription-management blueprint a European industrial equipment manufacturer needed to move from product sales to a service business — bridging CRM, subscription, and ERP."
client_display: "A European industrial equipment manufacturer"
industry: "Industrial manufacturing"
role: "Enterprise Architect (solo engagement)"
period: "2024 (4 months)"
order: 3
teaser: "Designed the subscription-management blueprint for a move from equipment sales to a service business — bridging CRM, subscription, and ERP into one order-to-quote flow, with vendor selection anchored on architectural fit."
lang: en
---

**Designed the subscription-management blueprint a European industrial equipment manufacturer needed to evolve from a product-sales business into a service business — bridging CRM, the new subscription layer, and ERP into a single order-to-quote flow, with vendor selection anchored on architectural fit rather than feature lists.**

## Context

A European industrial equipment manufacturer faced a strategic imperative to move beyond selling equipment. The market was shifting toward service-based offerings, and capturing recurring revenue through subscriptions required more than a feature — it required a new operating model. Underneath the strategy sat an architectural problem: any subscription solution had to bridge the customer-facing CRM, where orders originate, and the back-end ERP, where billing, revenue recognition, and fulfilment live — through a new subscription layer handling flexible pricing, packaging, and contract lifecycle. The two systems had no shared order-to-quote flow for subscriptions.

## The decision

Leadership wanted the robust, integrated, buy-not-build path. That made architecture-first sequencing essential: choosing a vendor well was impossible until the target capabilities and integration model were clear. I held the line on capability before system, against real pressure to evaluate feature-rich vendor solutions first.

## Constraints and trade-offs

- **Solo, four months.** No team to delegate to — scope had to be deliverable by one architect at sustained quality.
- **Cross-functional stakeholders.** Sales, finance, operations, and IT each held a local view; the blueprint needed a global one.
- **Vendor-marketing pressure.** Vendors were already pitching. The pull to shortlist before the architecture was settled was strong.
- **Trade-off I accepted.** A comprehensive blueprint took longer than a quick fix, but the clarity it gave made every later decision — vendor, integration, sequencing — cleaner.

## Approach

I worked from capability before system, in five layers.

1. **Landscape.** Surveyed the current architecture, business rules, CRM/ERP integration touchpoints, and capability gaps.
2. **Stakeholder alignment.** Interviews across sales, operations, IT, and finance; conflicting priorities surfaced and resolved rather than averaged.
3. **Capability design.** Current-state (equipment sales) and future-state (subscription) capability maps, naming the new capabilities required — contract lifecycle, recurring billing, revenue recognition, dynamic pricing.
4. **Solution blueprint.** Data models for subscription contracts, pricing, and billing; integration patterns for CRM ↔ subscription ↔ ERP; the order-to-quote workflow.
5. **Implementation strategy.** A prioritised roadmap and a vendor-selection framework anchored on architectural fit, not feature checklists. I stayed into early build to validate the blueprint under real pressure.

## Outcome

- A current- and future-state capability map giving leadership a clear view of what the subscription model required.
- A solution blueprint and CRM ↔ subscription ↔ ERP integration design that kept the new system from becoming an isolated silo.
- A vendor-selection framework built on architectural-fit criteria — a foundation for choosing the platform on fit, not marketing.
- The blueprint held up under early build: the architecture survived contact with implementation.

## What it shows

When a company changes its business model, it is not buying a new system — it is adopting a new operating model, and the architecture has to start from business capability rather than vendor features. The integration strategy is what decides whether subscription transformation succeeds, which is exactly why it has to precede vendor selection, not follow it.
