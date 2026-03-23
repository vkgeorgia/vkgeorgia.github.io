# Finance — Projects by Domain

Domain tag: `finance`  
Projects: 6

### Private Blockchain POC – National Stablecoin (EPM-AST)
- **Period:** 2025
- **Role:** Enterprise Architect
- **Employer:** EPAM
- **Client:** Bank, Integrator
- **Industry:** Finance
- **Domain:** Blockchain, Finance, Payments
- **Domain tags:** finance, architecture
- **Industry tags:** finance, consulting
- **Role tags:** business-analyst, enterprise-architect

**Key Result:** A solution designed to meet requirements and constraints, along with a roadmap for future changes, was delivered to the Client, leading to the start of the implementation project.

# Stablecoin proof-of-concept framing under delivery constraints

## Context
A leading bank in Asia explored a national stablecoin concept and needed to validate feasibility through a proof of concept. The engagement required rapid clarity on what a POC can prove, and what it cannot, given surrounding regulatory and operational realities.

## The Decision Challenge
The decision challenge was to define a POC scope that meaningfully reduces uncertainty: demonstrating a coherent operating model and the core system behaviors while avoiding premature commitment to a full-scale architecture. Over-scoping would delay learning; under-scoping would produce a demo with little decision value.

## Constraints and Trade-offs
Time constraints demanded prioritization of the most decision-relevant capabilities. A private ledger approach introduces governance questions about issuance, circulation, and control. The solution concept needed to remain adaptable so future regulatory or business decisions can be incorporated without a full redesign.

## Architectural / Strategic Perspective
The work focused on requirements and a solution concept that makes responsibilities explicit: how value is issued, how transactions are represented, what constraints matter, and what interfaces and controls are required. A roadmap clarified the sequence from POC learning to implementation decisions.

## Outcome and Impact
A solution concept aligned to requirements and constraints, together with a roadmap for next steps, enabled the client to move from exploration to an implementation initiative.

## Lessons Learned
Financial POCs create value when they turn “is it possible?” into “what decisions must be made next, and what risks do those decisions carry?”—not when they optimize a prototype.

### Business Transformation (DANF-L2C)
- **Period:** 2024
- **Role:** Enterprise Architect
- **Employer:** EPAM
- **Client:** Danfoss
- **Industry:** Manufacturing
- **Domain:** Digital Transformation, Business Transformation
- **Domain tags:** finance
- **Industry tags:** manufacturing, consulting
- **Role tags:** business-analyst, enterprise-architect, product-manager

**Key Result:** A comprehensive solution blueprint and capability map were delivered, providing the client with a clear roadmap for implementing a subscription management solution that aligns with business objectives and technological capabilities.

# Subscription management blueprint for lead-to-cash transformation

## Context
Danfoss moved toward a service-based business model, which required subscription management as a connective layer between customer engagement and enterprise operations. The organization needed a coherent blueprint before committing to implementation.

## The Decision Challenge
The decision challenge was how to design a subscription capability that supports the business shift without creating a brittle integration layer. A weak design would lock the organization into expensive workarounds between commercial processes and operational fulfillment.

## Constraints and Trade-offs
Existing systems and processes set constraints on what could change first. A “perfect” target state would delay the transition; a minimal approach risked pushing complexity into manual processes. Vendor selection required a clear articulation of required capabilities and an understanding of where differentiation matters.

## Architectural / Strategic Perspective
The work framed the subscription solution as a capability map and a blueprint of responsibilities and interfaces. The roadmap prioritized steps that unlock the transition: sequencing capabilities, clarifying ownership, and establishing a pragmatic integration approach between commercial and operational domains.

## Outcome and Impact
A solution blueprint, capability map, and prioritized roadmap were established, providing a clear basis for selecting a provider and proceeding into development with aligned expectations.

## Lessons Learned
Business model shifts are rarely blocked by technology alone; they are blocked by unclear responsibility boundaries. A good blueprint makes those boundaries explicit before the organization starts buying or building.

### Informing clients about the debt on their account (SPDZ) (RTK-SPDZ)
- **Period:** 2017–2019
- **Role:** Solution Architect
- **Employer:** Rostelecom
- **Client:** Rostelecom
- **Industry:** Telecom
- **Domain:** Account Management
- **Domain tags:** finance, omni-channel, process-automation
- **Industry tags:** telecom, telecom
- **Role tags:** business-analyst, solution-architect

**Key Result:** A unified approach for managing client notifications was proposed. A solution architecture was created, and documentation was handed over for implementation, which significantly reduced accounts receivable (by three times) and brought significant economic benefits.

# Debtor notifications as a lever to reduce accounts receivable

## Context
Rostelecom faced growing accounts receivable, reducing operational flexibility and tying up funds. The existing debtor-informing practice relied on manual reconciliation statements and email correspondence, which was slow, inconsistent, and expensive to run.

## The Decision Challenge
The decision challenge was whether to treat receivables as a purely financial control problem or to address it as a communication and behavioral problem: timely, accurate notifications that change client behavior. If approached incorrectly, automation could increase disputes and dissatisfaction, while manual processes could not scale to the needed coverage.

## Constraints and Trade-offs
Accuracy and timing were both critical: wrong or late notifications undermine trust and can increase operational load. The organization needed a consistent set of notification rules without building a fragile web of exceptions. The solution also had to reduce manual effort in reconciliation and paperwork, not shift it elsewhere.

## Architectural / Strategic Perspective
The approach framed notifications as a governed service: clear event triggers (debt conditions), standardized content rules, and traceability from notification back to financial facts. This reduced ambiguity in how debt is determined and ensured the communication process remained auditable.

## Outcome and Impact
A unified notification approach and solution architecture were established and used for implementation. Accounts receivable decreased threefold, and the organization reduced time spent on reconciliation and paper/email handling, producing a material economic effect.

## Lessons Learned
Receivables reduction is often achieved not by stronger collections, but by making the organization’s expectations legible and timely—so that paying becomes the default, not a negotiation.

### O2O Interaction (RTK-O2O)
- **Period:** 2017–2019
- **Role:** Solution Architect
- **Employer:** Rostelecom
- **Client:** Rostelecom
- **Industry:** Telecom
- **Domain:** Inter-operator Communication
- **Domain tags:** finance, architecture, integration, process-automation
- **Industry tags:** telecom, telecom
- **Role tags:** enterprise-architect, solution-architect

**Key Result:** A concept for interaction architecture between operators was developed. A solution was created. As an alternative, a solution for inter-operator settlement registration based on blockchain was proposed.

# Simplifying inter-operator settlement accounting under complex offsets

## Context
Rostelecom’s interactions with other operators involved complex multi-party service supply and debt offset schemes. Settlement reconciliation was slow, error-prone, and paper-heavy, consuming significant operational effort and delaying the availability of funds.

## The Decision Challenge
The decision challenge was how to simplify settlements without losing correctness: whether to continue with incremental process improvements or to introduce a more structured settlement registration and reconciliation model. Errors at this layer are expensive—financially and in partner relationships—so “speed” without control would be a false win.

## Constraints and Trade-offs
Multiple counterparties and non-trivial offset rules create edge cases that are difficult to resolve manually. Formalizing the model improves accuracy and reduces effort, but it requires agreement across internal stakeholders and partners. Exploring alternative technology (a distributed ledger POC) could increase transparency but introduces adoption and governance complexity.

## Architectural / Strategic Perspective
The work focused on making settlement events and obligations explicit: standard representations, controlled reconciliation steps, and clear responsibility boundaries. The alternative approach using distributed registration was explored as a way to reduce disputes and improve traceability, with attention to where such an approach would be justified.

## Outcome and Impact
A concept and agreed direction for inter-operator interaction architecture were established, with a documented solution ready for implementation. The expected benefits included thousands of man-hours saved per year and significant error-driven loss avoidance.

## Lessons Learned
Multi-party settlements improve when reconciliation is treated as a shared model—with explicit events, obligations, and traceability across parties—rather than as endless exception handling.

### Financial Monitoring (SKY-BARS)
- **Period:** 2008–2010
- **Role:** Business Analyst, Project Manager
- **Employer:** Rostelecom.SkyLink
- **Client:** Rostelecom.SkyLink
- **Industry:** Telecom
- **Domain:** Finance
- **Technologies:** Microsoft C#, MS SQL Server, MS SQL Analysis Services, MS SQL Reporting Services.
- **Domain tags:** finance
- **Industry tags:** telecom, retail, telecom, retail
- **Role tags:** business-analyst, project-manager

**Key Result:** Automated internal financial control system. Implemented a budgeting and control process that reduced the budget preparation cycle from 6 months to 2 and improved financial transparency.

# Internal budgeting and financial control

## Context
Rostelecom.SkyLink relied on budgeting and internal financial control processes that were slow and opaque. Budget preparation could take up to six months, which limited the organization’s ability to respond to change and reduced confidence in management reporting.

## The Decision Challenge
The central question was whether budgeting should remain a periodic administrative exercise or become a management control loop supported by consistent data and rules. Getting it wrong risked locking the company into long planning cycles, weak cost discipline, and decisions driven by incomplete or late information.

## Constraints and Trade-offs
The work had to reconcile different expectations across finance and management while keeping day-to-day operations running. Standardization improved comparability and control, but it reduced local flexibility and forced explicit choices about definitions, approval flows, and reporting granularity.

## Architectural / Strategic Perspective
The problem was framed as an end-to-end decision system: how plans are created, approved, monitored, and corrected. That required a shared information model for budget items and financial facts, clear ownership of rules, and a consistent path from operational inputs to management views. The emphasis was on making the logic auditable and repeatable rather than relying on individual expertise and manual reconciliation.

## Outcome and Impact
Budget preparation time was reduced from six months to two months. Financial transparency improved, enabling more reliable monitoring of financial flows and stronger internal control without increasing the manual reporting burden.

## Lessons Learned
This case illustrates that “automation” only matters after the organization agrees on what it wants to control and why; clarity of definitions and decision rights is what makes speed and transparency sustainable.

### 1С: Accounting + Trade & Warehouse (SKY-ACC-TRD)
- **Period:** 2008–2010
- **Role:** Business Analyst, Project Manager
- **Employer:** Rostelecom.SkyLink
- **Client:** Rostelecom.SkyLink
- **Industry:** Telecom
- **Domain:** Accounting, Retail
- **Technologies:** 1C:Accounting, 1C:Trade&Warehouse
- **Domain tags:** erp, finance
- **Industry tags:** telecom, retail, telecom, retail
- **Role tags:** business-analyst, project-manager

**Key Result:** Deployed and configured integrated accounting. Unified accounting and inventory management across all legal entities, enabling transparent reporting and integration with planning systems.

# Consolidated accounting and inventory across legal entities

## Context
Rostelecom.SkyLink operated through multiple legal entities with fragmented accounting and inventory practices. Disparate data made consolidated reporting slow and unreliable and weakened integration with planning and control functions.

## The Decision Challenge
The core decision was how far to push unification: whether to accept “local truth” in each entity and stitch reports together later, or to enforce shared definitions and workflows so that consolidation becomes routine. A poor choice would either stall adoption (if overly rigid) or preserve the same transparency problems under a new label (if overly permissive).

## Constraints and Trade-offs
Unification required aligning accounting policies and inventory rules while respecting legal-entity differences. Faster rollout favored minimal change, but long-term transparency depended on disciplined data standards and consistent operating procedures. Integration with existing planning processes added pressure to define stable interfaces and ownership.

## Architectural / Strategic Perspective
The work treated accounting and inventory as enterprise data products: a single set of definitions, controlled master data, and predictable aggregation paths to consolidated views. The emphasis was on reducing reconciliation surfaces—fewer handoffs, fewer transformations, and fewer “special cases” that only exist in spreadsheets.

## Outcome and Impact
Accounting and inventory management were unified across legal entities, enabling transparent consolidated reporting and making integration with planning systems feasible. Operational effort shifted away from manual consolidation toward routine, repeatable controls.

## Lessons Learned
For multi-entity organizations, the hardest part is not the system choice but agreeing on what “consistent data” means in practice—and being explicit about where differences are legitimate and where they are just inherited noise.
