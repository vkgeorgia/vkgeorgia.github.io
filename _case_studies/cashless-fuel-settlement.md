---
layout: case
title: "Replacing paper fuel vouchers with a cashless platform for 70,000+ corporate clients"
seo_title: "Cashless Corporate Payment Platform — Enterprise Architecture Case Study"
description: "How an enterprise architect replaced paper fuel-voucher settlements with a cashless corporate card platform for 70,000+ clients, cutting reconciliation sixfold and fraud losses tenfold."
client_display: "A major national oil company — fuel retail with 70,000+ B2B counterparties"
industry: "Energy & fuel retail"
role: "Enterprise Architect"
period: "Solutions Architect / Enterprise Architect"
order: 2
teaser: "Reconciliation time cut 6× and fraud-related losses cut 10× — by replacing paper-coupon settlement with a cashless platform that builds control and traceability into the payment lifecycle."
lang: en
---

**Replaced paper fuel vouchers with a cashless corporate card platform for 70,000+ clients — reconciliation cut from weeks to days (6× faster) and fraud-related losses cut roughly 10× — by building control and traceability into the payment lifecycle rather than bolting it on afterwards.**

## Context

A major national oil company managed cashless fuel payments for a very large base of corporate customers — over 70,000 legal entities. Paper fuel coupons and manual reconciliation created constant operational drag and opened space for fraud, producing direct losses and slow settlement cycles. At that scale, edge cases could no longer be handled by hand.

## The decision

The obvious framing was "replace paper with plastic." I reframed it as a control-system design: the real question was whether compliance should keep depending on retrospective oversight, or be designed into every issuance, transaction, and settlement so that an invalid action is rejected at the point of authorisation rather than caught weeks later.

## Constraints and trade-offs

- **Scale.** At 70,000+ entities and hundreds of thousands of weekly transactions, manual exception-handling was not an option — the design had to be scale-resistant.
- **Integration.** The platform had to fit existing financial systems and stay compatible with the gas-station network and corporate-client adoption.
- **Trade-off I accepted.** More upfront architectural work and stakeholder alignment, in exchange for a repeatable, fraud-resistant process — rather than digitising the existing workflow and carrying its structural weaknesses forward.

## Approach

I designed a three-layer platform and brought the client's security team into the architecture from the start, so audit trails and limits were designed in, not retrofitted.

1. **Payment-instrument lifecycle** — card issuance, activation, limits, blocking, and status managed as a state machine.
2. **Real-time rules engine** — balance, limit, approved-merchant, and compromise checks at the point of sale, with fraud thresholds the client's compliance team could adjust without code changes.
3. **Automated settlement and reconciliation** — structured transaction data matched against client invoices, with discrepancies flagged algorithmically.

Through migration, paper vouchers and cards ran in parallel for the 70,000+ clients — risk reduction, not waste.

## Outcome

- **Reconciliation:** 4–6 weeks of manual verification to 3–4 days automated — **6× faster**.
- **Fraud losses:** reduced roughly **10×**, via point-of-authorisation controls rather than after-the-fact detection.
- **Scale:** the platform carried 70,000+ active corporate clients and hundreds of thousands of weekly transactions, with faster per-account onboarding.
- The client formally recognised the business impact.

## What it shows

Controls belong inside the process, not on top of it: a rules engine that rejects an invalid transaction in real time prevents the loss; a review that catches it days later cannot undo it. And reconciliation turned out to be a process-design problem, not a reporting one — engineering structured data and algorithmic matching into settlement is what took it from weeks to days and made it defensible.
