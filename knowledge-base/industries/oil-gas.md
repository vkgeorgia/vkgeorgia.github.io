# Oil Gas — Projects by Industry

Industry tag: `oil-gas`  
Projects: 7

### Oil & Gas Company (ADNO-TRMS)
- **Period:** 2025
- **Role:** Enterprise Architect
- **Employer:** EPAM
- **Client:** ADNOC
- **Industry:** Oil & Gas
- **Domain:** C&B, HR
- **Domain tags:** architecture, process-automation
- **Industry tags:** oil-gas, consulting
- **Role tags:** business-analyst, enterprise-architect, solution-architect, lead-business-analyst

**Key Result:** The organization received a ready-to-implement target process description and AI agent requirements, prepared for the deployment of a new AI-automated process.

# Remuneration process redesign with AI-automation readiness

## Context
A vertically integrated oil and gas company sought to overhaul remuneration planning and calculation for fixed and variable components. The existing cycle was long (around 11 weeks), error-prone, and exposed to human-factor risks, including weak transparency in bonus-related decisions.

## The Decision Challenge
The decision challenge was to redesign the process so that it becomes both faster and more controlled, while preparing it for selective automation. Automating a flawed process would amplify problems; redesigning without an automation perspective would preserve long cycle time and manual burden.

## Constraints and Trade-offs
Remuneration decisions are sensitive and politically charged, raising the cost of ambiguity and inconsistency. Achieving a projected reduction to 1–2 weeks required clear decision points, standardized inputs, and explicit rules. Increased control improves transparency but can be perceived as reduced flexibility by stakeholders.

## Architectural / Strategic Perspective
The work structured the process around capabilities and decision points, then identified fragments suitable for AI-enabled assistance and automation. Agent requirements were defined in terms of roles, inputs/outputs, and interaction logic, with emphasis on explainability and governance rather than “black box” automation.

## Outcome and Impact
An agreed target process description and AI agent requirements were prepared, positioning the organization to move toward an AI-automated process. The design established a credible path to reduce cycle time from 11 weeks to 1–2 weeks while strengthening transparency and reducing error and abuse risks.

## Lessons Learned
Automation in sensitive processes works when it is a governance choice: the organization first agrees on decision rules and accountability, and only then uses AI to compress cycle time.

### Architecture Analysis for Fuel Retail (ADNO-BCP)
- **Period:** 2024–2025
- **Role:** Enterprise Architect
- **Employer:** EPAM
- **Client:** ADNOC
- **Industry:** Oil & Gas
- **Domain:** Loyalty Program
- **Domain tags:** architecture
- **Industry tags:** oil-gas, consulting
- **Role tags:** enterprise-architect, solution-architect

**Key Result:** Проведено обследование ландшафта заказчика. Resolved loyalty issues, gave future IT landscape improvement plan

# Stabilizing fuel retail operations affected by loyalty outages

## Context
ADNOC experienced critical disruptions at petrol stations where loyalty program outages could cascade into full service shutdowns. The issue sat at the intersection of operational processes, integrations, and station hardware/software dependencies.

## The Decision Challenge
The decision challenge was how to restore stability quickly while avoiding a “patch and hope” cycle that would repeat the same incidents. The wrong approach would either prolong revenue loss (if too slow) or create temporary fixes that fail under the next load or change.

## Constraints and Trade-offs
Retail fuel operations tolerate little downtime, so remediation had to minimize operational risk. The landscape was complex, spanning loyalty, retail systems, finance, POS, and dispenser interactions. Short-term stabilization needed to coexist with a longer-term direction for resilience and simplification.

## Architectural / Strategic Perspective
The analysis focused on identifying failure points and integration bottlenecks across the end-to-end station flow, then translating findings into actionable architectural recommendations. The intent was to make dependencies explicit so that “loyalty” stops being a single point of operational failure.

## Outcome and Impact
Immediate disruptions were resolved and operational stability was restored. The organization received a forward plan for improving the IT landscape to prevent recurrence and support ongoing digital growth.

## Lessons Learned
Operational incidents in retail are often architecture problems in disguise: resilience improves when critical flows have explicit dependency management and failure containment.

### Data Lake (Presale) (RTK-LAKE)
- **Period:** 2016–2018
- **Role:** Business Analyst
- **Employer:** Rostelecom.Restream
- **Client:** Gazprom Neft
- **Industry:** Oil & Gas
- **Domain:** Data Management
- **Domain tags:** analytics
- **Industry tags:** oil-gas, telecom
- **Role tags:** business-analyst

**Key Result:** Successfully conducted a presale for a large oil and gas enterprise, including analyzing customer requirements, proposing and presenting a solution, and defending it in a competition.

# Data lake presale and solution defense for an oil & gas enterprise

## Context
Gazprom Neft needed to work with large, heterogeneous datasets across fuel supply and sales and related products. Existing approaches struggled with scale and variety, limiting the organization’s ability to extract insights and identify new profit opportunities.

## The Decision Challenge
The decision challenge was to frame a “data lake” not as a technology trend but as a coherent capability with clear business cases, costs, and implementation risks. Presale success depended on translating data ambitions into a defendable architecture and a credible delivery path under competitive scrutiny.

## Constraints and Trade-offs
Large data initiatives fail when they promise universal value without prioritization. The proposal needed to balance platform generality with concrete use cases and to set expectations around governance, data onboarding effort, and time-to-value. Competitive tender conditions raised the bar for clarity and justification.

## Architectural / Strategic Perspective
The solution was structured around sources, ingestion patterns, storage and processing responsibilities, and consumption paths for analytics. Emphasis was placed on explaining how the platform would be governed and how it would enable business units to move from data capture to repeatable insight generation.

## Outcome and Impact
Customer requirements were analyzed, a competitive solution concept and proposal were prepared and presented, and the solution was successfully defended in a tender process. The presale work established a strong basis for subsequent implementation discussions.

## Lessons Learned
In presale for data platforms, credibility comes from acknowledging constraints up front—especially governance and onboarding effort—and showing how value emerges in stages rather than all at once.

### Fuel Station Management System (GAM-ZG)
- **Period:** 2015–2019
- **Role:** Solution Architect, Project Manager
- **Employer:** Gamma
- **Client:** ZG Fuel Retail Chain
- **Industry:** Oil & Gas
- **Domain:** Loyalty Program, Retail
- **Technologies:** PHP, 1C
- **Domain tags:** retail-technologies
- **Industry tags:** retail, oil-gas, consulting, it-services
- **Role tags:** enterprise-architect, solution-architect, project-manager

**Key Result:** Implemented fuel station system with integration and migration. (Тут надо обновить чтобы была еще программа лояльности)

# Fuel station management system replacement with integration and migration

## Context
A fuel station network needed to modernize its operational backbone for station management. The existing setup limited efficiency and made integration with adjacent capabilities (accounting, loyalty, payments, reporting) harder than it should be.

## The Decision Challenge
The decision was whether to keep patching legacy processes or to move to a new management backbone while protecting operational continuity. For retail fuel operations, disruptions translate directly into lost revenue, so the migration approach mattered as much as the target state.

## Constraints and Trade-offs
Integration surfaces are extensive in station operations, and historical data is operationally relevant. A “big bang” approach reduced time spent in dual-running but increased outage risk; a phased approach lowered risk but required careful control of interfaces and data consistency during migration.

## Architectural / Strategic Perspective
The work centered on defining stable station-management capabilities and integration contracts, then planning migration so that business operations remain explainable throughout the change. Data migration was treated as an integrity problem (definitions, mappings, validation) rather than a file transfer.

## Outcome and Impact
A fuel station management system was put in place with the required integrations and completed data migration, improving transparency and manageability of station operations and reducing manual effort caused by fragmented tooling.

## Lessons Learned
In retail operations, modernization succeeds when migration is designed as a business continuity plan—with explicit risk containment and verifiable data integrity at each step.

### B2B Fuel Payment System (OILPC-KSBR)
- **Period:** 2012–2015
- **Role:** Project Manager, Business Analyst, Solution Architect
- **Employer:** OilPC
- **Client:** Gazprom Neft
- **Industry:** Oil & Gas
- **Domain:** Card Processing, Retail, Fuel Retail
- **Technologies:** Java, PHP, Oracle DB
- **Domain tags:** loyalty
- **Industry tags:** oil-gas, retail, it-services, finance
- **Role tags:** business-analyst, solution-architect, project-manager

**Key Result:** Created a platform for cashless settlement. Reduced fraud by replacing paper fuel coupons with cards. Automated cashless settlements with 70,000 legal entities; reduced reconciliation time 6x, cut fraud losses 10x; received a client commendation.

# Corporate cashless fuel payments with fraud reduction

## Context
Gazprom Neft managed cashless fuel payments for a very large base of corporate customers (70,000+ legal entities). Paper fuel coupons and manual reconciliation created operational drag and opened space for fraud, producing direct losses and slow settlement cycles.

## The Decision Challenge
The core decision was whether to keep improving controls around a paper-based model or to move the settlement mechanism onto an instrument that supports traceability and enforceable rules. A wrong choice risked continued fraud exposure and an ever-growing reconciliation effort that would not scale with the customer base.

## Constraints and Trade-offs
A change in payment instrument affected security, customer experience, and operational processes (issuance, blocking, accounting, dispute handling). Anti-fraud measures had to improve materially without turning the solution into a high-friction process for legitimate customers. Scale meant that edge cases could not be handled manually.

## Architectural / Strategic Perspective
The platform was framed as a control system: clear lifecycle management for the payment instrument, enforceable rules around transactions, and reconciliation as a repeatable process rather than an investigation. Interfaces to adjacent enterprise systems needed to preserve auditability so that operational decisions and financial outcomes stayed explainable.

## Outcome and Impact
A cashless settlement platform replaced paper coupons with cards, enabling automated settlements with 70,000+ legal entities. Reconciliation time was reduced sixfold, fraud-related losses fell tenfold, and the client formally recognized the business impact.

## Lessons Learned
Fraud reduction at scale is rarely a single “security feature”; it comes from designing the operating model so that traceability and control are built into how the business runs.

### Loyalty Program for Fuel Retail (OILPC-LOY)
- **Period:** 2012–2015
- **Role:** Business Analyst, Project Manager, Solution Architect
- **Employer:** OilPC
- **Client:** Gazprom Neft
- **Industry:** Oil & Gas
- **Domain:** Card Processing, Retail, Fuel Retail
- **Technologies:** Java, PHP, Oracle DB
- **Domain tags:** analytics, loyalty, retail-technologies
- **Industry tags:** oil-gas, retail, it-services, finance
- **Role tags:** business-analyst, solution-architect, project-manager

**Key Result:** Designed and launched a loyalty system for the fuel retail chain. Implemented a comprehensive loyalty program platform. Participants grew from 1M to 4.5M; marketing effectiveness significantly improved.

# Loyalty platform for a fuel retail network

## Context
Gazprom Neft’s fuel retail network needed loyalty to function as a business lever rather than a simple points accumulator. Without a coherent platform, personalization, measurement of campaign impact, and consistent customer experience were limited.

## The Decision Challenge
The decision was whether to keep loyalty as a lightweight marketing tool or treat it as a customer and revenue management capability with enterprise-grade data and operational discipline. Getting it wrong would either cap growth (if too simplistic) or create a costly program that cannot be operated consistently across channels (if too complex too early).

## Constraints and Trade-offs
The platform had to work across many retail locations and integrate into daily point-of-sale operations without adding friction. More personalization and analytics increased complexity and data demands, while a simpler design reduced the ability to learn and adapt. The program needed rules that could be explained to customers and staff, not only to engineers.

## Architectural / Strategic Perspective
The work treated loyalty as a system of decisions: how customers are identified, how benefits are earned and redeemed, and how campaigns are evaluated. That required consistent customer/account definitions, clear rule governance, and reliable feedback loops from transaction data to marketing decisions.

## Outcome and Impact
A comprehensive loyalty system was established for the retail chain. Participation grew from 1M to 4.5M, and marketing effectiveness improved through better segmentation and measurable campaign execution.

## Lessons Learned
Loyalty becomes valuable when it shifts from “points accounting” to a disciplined learning loop—where customer behavior, offers, and outcomes connect in a way the organization can trust.

### Fuel Retail Management System (GAM-NAMOS)
- **Period:** 2012–2015
- **Role:** System Analyst
- **Employer:** Gamma
- **Client:** Wincor Nixdorf
- **Industry:** Oil & Gas
- **Domain:** Business Analysis
- **Technologies:** Confluence
- **Domain tags:** architecture, erp, retail-technologies
- **Industry tags:** retail, oil-gas, consulting, consulting, it-services
- **Role tags:** business-analyst, solution-architect, system-analyst

**Key Result:** An architecture audit of the existing, already implemented fuel retail management system (Namos) at petrol stations was performed. Documentation for the existing software was created in accordance with local and European standards.

# Architecture audit and standards-aligned documentation for PSMS software

## Context
Wincor Nixdorf had an operational petrol station management system in the field, but the architectural knowledge and documentation were not sufficiently current or standardized. This created support and evolution risk and complicated alignment with local and European expectations for documentation quality.

## The Decision Challenge
The decision was whether to treat documentation as a compliance artifact or as a control mechanism that reduces operational and delivery risk. In mature, already-running software, gaps in architectural understanding translate into slower incident resolution, fragile integrations, and costly change.

## Constraints and Trade-offs
The work had to describe an existing reality rather than a greenfield design. Over-documentation would be expensive and quickly stale; under-documentation would fail to support compliance and change. The emphasis needed to be on system boundaries, responsibilities, integrations, and operational characteristics.

## Architectural / Strategic Perspective
The audit focused on making implicit decisions explicit: how the system is decomposed, where data moves, and where constraints and risks accumulate. Documentation was structured to support both engineering work (change planning, integration safety) and organizational needs (common vocabulary, repeatable reviews, standards alignment).

## Outcome and Impact
An architectural audit clarified the current state and risks of the PSMS software, and a complete documentation set was established in a standards-aligned form. As a result, the system became easier to support and evolve, and the organization reduced the risk associated with undocumented dependencies.

## Lessons Learned
In long-lived systems, documentation is not a narrative of work—it is a mechanism for preserving decision intent so that future change does not turn into accidental redesign.
