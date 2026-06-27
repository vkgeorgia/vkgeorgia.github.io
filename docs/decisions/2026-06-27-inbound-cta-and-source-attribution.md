# Inbound CTA and source attribution

- **Status:** Accepted
- **Date:** 2026-06-27
- **Task:** [strategy#217](https://github.com/vkgeorgia/strategy/issues/217) (part of epic [#104](https://github.com/vkgeorgia/strategy/issues/104) — personal-brand inbound engine)

## Purpose

Define the site's primary inbound call-to-action (CTA) and how an inbound inquiry is attributed to its channel, so the epic's success signal — *1–2 attributable qualified inquiries per quarter* — is measurable.

## Decision

### 1. Primary CTA

The single primary CTA across the site is **"Book a 30-min intro call"**, pointing to the Google Calendar appointment link `https://calendar.app.google/YwmXZytfSQ2qWX4Z7`. It is present on every key surface:

- **Nav** — persistent styled button (`site-cta` in `_includes/header.html`), on every page via the layout.
- **Footer** — "Schedule a Meeting" link (`_includes/footer.html`), on every page.
- **In-body** — top and/or closing CTA on Home, Cases, Business Challenges, Articles, Services index, and all service sub-pages.

One canonical link is reused everywhere (no per-page variants) to keep the funnel single and unambiguous.

### 2. Source attribution

Attribution combines two lightweight signals, no new tooling:

- **Inbound channel — Cloudflare Web Analytics referrers** (live since [#391](https://github.com/vkgeorgia/strategy/issues/391)). The dashboard shows how a visitor reached the site (LinkedIn vs direct vs search vs other) plus top countries — enough to attribute site traffic to a channel.
- **Conversion ground-truth — declaration at the intro call.** Because booking completes off-site on Google Calendar, the booking itself is confirmed by asking the prospect where they found Valerii (the epic explicitly allows "declared at intro call").

### 3. Explicitly not done (and why)

- **No UTM parameters on the calendar link.** Google Calendar appointment short-links do not reliably surface UTM tags to the organiser, and appending params to the single most important conversion link carries breakage risk for no confirmed benefit. The conversion link is left untouched.
- **No Cloudflare custom event on CTA click.** Custom events in Cloudflare Web Analytics are limited/unguaranteed and were deferred in #391. Referrers + intro-call declaration are sufficient for the current success signal.

## Consequences

- Attribution is lightweight, privacy-friendly, and uses only tooling already in place.
- Limitation: there is no automatic CTA-click → booking conversion count. Acceptable at current scale; revisit with a Cloudflare custom event (or a booking tool that captures UTM) if funnel-level conversion analysis is later needed.
- **LinkedIn-side counterpart (separate, `proj:linkedin`):** the LinkedIn Featured "Book a call" link should carry its own channel marker so LinkedIn-origin sessions are distinguishable in referrers; tracked outside this repo.
- Feeds the semi-annual review routine — see [strategy#394](https://github.com/vkgeorgia/strategy/issues/394) (add a Cloudflare-dashboard trends check).
