# Anchor case studies — long-form case pages

- **Status:** Accepted
- **Date:** 2026-06-27
- **Task:** [strategy#216](https://github.com/vkgeorgia/strategy/issues/216) (part of epic [#104](https://github.com/vkgeorgia/strategy/issues/104) — personal-brand inbound engine)

## Purpose

Publish 2–3 long-form "anchor" case studies with operational and product-domain depth, individually addressable, so the site carries proof that converts inbound — and so the home "Selected outcomes" and the deep dives tell one coherent story.

## Decision

### Format — a dedicated `case_studies` collection

A new Jekyll collection `case_studies` (`output: true`, `permalink: /cases/:name/`) renders each anchor case as its own page at `/cases/<slug>/`, via `_layouts/case.html`.

Why a new collection rather than reusing `projects`: the existing `projects` collection is `output: false` (brief filterable cards only, no individual URLs). Flipping it to `output: true` would generate 44 thin URLs with no long-form layout. A separate collection gives the anchor cases real URLs without disturbing the existing cards.

### Information architecture of `/cases/`

`/cases/` stays the index:

1. **Featured case studies** — teaser cards generated from `site.case_studies` (title, client descriptor, one-line outcome, "Read the case →" link).
2. **Other engagements** — the existing filterable `projects` cards (unchanged).

The home page keeps `_includes/highlights.html` ("Selected outcomes") as three one-line outcomes; each one maps to a featured case study, so the elevator pitch and the deep dives stay aligned.

### Initial set (3)

1. Product portfolio harmonisation (aviation hub) — product-domain anchor (§2.7).
2. Cashless fuel settlement (energy / fuel retail) — operational depth.
3. Subscription business-model transformation (industrial manufacturing) — business-model / product depth.

Home "Selected outcomes" updated to match: the former HR-assistant outcome was replaced by the subscription/manufacturing one, for a single narrative across home → `/cases/`. The AI/product anchor is carried elsewhere (the architecture-as-code section and the AaC narrative), so nothing is lost.

## Confidentiality

- Client names follow `endeavours/client_alternatives.yaml` and `client_name_visibility`: the aviation hub is named (public, §2.6 DME exception); the other two render as their canonical alternatives ("a major national oil company", "a European industrial equipment manufacturer") — real names never appear.
- No internal project codes on any public surface (§5.6).
- Russia-deprioritised framing (§2.6): no country markers beyond the approved alternatives.
- Copy written to the §3.2 voice tests (senior-partner / proof / fit).

## Consequences

- Anchor cases are now first-class, shareable URLs; adding another is one file in `_case_studies/`.
- `docs/` is excluded from the Jekyll build so these ADRs are not published as site pages.
- Source of truth for the case content is the `endeavours/` STAR records; if those numbers change, the case pages and `highlights.html` must be updated together.
