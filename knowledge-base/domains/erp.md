# ERP — Projects by Domain

Domain tag: `erp`  
Projects: 6

### Single Profile Concept (EPM-SPC)
- **Period:** 2022
- **Role:** Enterprise Architect
- **Employer:** EPAM
- **Client:** EPAM
- **Industry:** IT Services
- **Domain:** Data Management
- **Domain tags:** erp
- **Industry tags:** it-services, it-services
- **Role tags:** enterprise-architect

**Key Result:** A single profile concept was created and used as a foundation for four new projects, leading to significant time savings, process unification, and improved company image.

# Unified contact profile concept for enterprise-wide consistency

## Context
EPAM maintained multiple systems that stored information about employees and other contact types (students, interns, community members). Fragmentation created discrepancies, confusion in processes, and barriers to unification and consistent management.

## The Decision Challenge
The decision was whether to keep “profiles” as system-specific representations or establish a shared enterprise concept that can be reused across processes and systems. A weak concept would add another layer of inconsistency; an overly rigid one would block real-world use cases and slow adoption.

## Constraints and Trade-offs
Different contact types have different lifecycles and sensitivity levels, which complicates a single model. Unification improves consistency and reduces rework, but it requires explicit transformation rules and agreement on what is core versus what remains contextual. The concept also needed to be usable as a foundation for subsequent initiatives.

## Architectural / Strategic Perspective
The work defined a shared information architecture for contact profiles and clarified process-level responsibilities for creating, updating, and consuming profiles. The emphasis was on explicit data flows and transformation rules so downstream systems can integrate without re-deriving identity and profile semantics.

## Outcome and Impact
A unified profile concept was established and became the foundation for multiple follow-up initiatives (including centralized permission management and profile storage), reducing duplication and supporting more consistent processes and data management across the organization.

## Lessons Learned
A “single profile” is only valuable when it is a contract: a shared definition that reduces argument and rework every time a new system or process needs identity data.

### Human Resource Management System (HRMS) (EPM-HRMS)
- **Period:** 2021–2022
- **Role:** Lead Business Analyst, Enterprise Architect
- **Employer:** EPAM
- **Client:** EPAM
- **Industry:** IT Services
- **Domain:** HR, Data Management, Workflow Management
- **Technologies:** Java
- **Domain tags:** erp, hr-tech
- **Industry tags:** it-services, it-services
- **Role tags:** business-analyst, enterprise-architect

**Key Result:** Requirements were gathered and technical specifications for an HR system were prepared, which led to improved efficiency, significant time savings, and compliance with data privacy regulations.

# People profile management under global compliance and organizational change

## Context
EPAM experienced large-scale organizational change driven by remote work and relocations. People data existed across fragmented and outdated systems, and the scope extended beyond employees to external contacts, students, and community members. Operating across 58 countries also raised significant data privacy obligations.

## The Decision Challenge
The decision was how to redesign people profile management so that it supports evolving organizational structures while remaining compliant and operable globally. A narrow HR-only approach would fail to address broader contact use cases; an overly broad approach risked unclear ownership and uncontrolled data growth.

## Constraints and Trade-offs
Compliance requirements varied by country, and legacy data was inconsistent. Migration and transformation could not be treated as a one-time event because source systems and data formats continued to change. Strong governance improves privacy posture but can slow operational responsiveness if responsibilities and rules are not clearly defined.

## Architectural / Strategic Perspective
The work focused on defining requirements and operating rules for a profile storage capability: what constitutes a profile, how profiles change over time, how transformations are governed, and how consuming systems should interact with a single source of truth. The emphasis was on traceability and defensible compliance rather than tool-specific solutions.

## Outcome and Impact
A requirements and specification package for a new people profile management capability was established, supporting process efficiency improvements, reduction of accounting errors, and compliance alignment across countries. The work created a foundation for scalable evolution of the people data landscape.

## Lessons Learned
Global people data management is a governance problem first: without explicit rules and ownership, “data privacy compliance” becomes an endless set of exceptions rather than a stable operating model.

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

### 1С: Payroll & HR (SKY-ZUP)
- **Period:** 2008–2010
- **Role:** Business Analyst, Project Manager
- **Employer:** Rostelecom.SkyLink
- **Client:** Rostelecom.SkyLink
- **Industry:** Telecom
- **Domain:** C&B, HR
- **Technologies:** 1C:Salary and HR Management, integrated with the BARS budgeting system.
- **Domain tags:** erp, hr-tech
- **Industry tags:** telecom, retail, telecom, retail
- **Role tags:** business-analyst, project-manager

**Key Result:** Introduced a single payroll and motivation system across all branches, integrated with the budgeting system. Launched HR system for 50+ users.

# Unified payroll and HR operating model across branches

## Context
Rostelecom.SkyLink’s distributed branch network relied on non-uniform payroll and HR practices. Differences in accrual logic and incentive schemes created inconsistencies, increased manual checks, and made personnel costs difficult to plan and control.

## The Decision Challenge
The decision was whether to prioritize local autonomy or enterprise consistency in payroll and HR accounting. Fragmentation reduced comparability and increased error risk; strict standardization risked friction where incentive schemes and operational realities differed by branch.

## Constraints and Trade-offs
A unified approach needed to support existing compensation logic while making the rules explicit and auditable. Integration with budgeting meant that HR data could no longer be treated as “back office”; it became an input into financial decisions. Adoption required keeping the experience workable for a broad user base (50+ users) without building exceptions into the core logic.

## Architectural / Strategic Perspective
The work focused on defining stable “rules of record” for payroll, incentives, and personnel events, and on connecting those rules to financial planning. The emphasis was on reducing ambiguity through common definitions, consistent approval paths, and predictable outputs for budgeting and reporting.

## Outcome and Impact
A single payroll and motivation system was put in place across branches and connected to the budgeting system, improving transparency of personnel costs and reducing discrepancies in accruals. An HR system went into use for 50+ users, stabilizing day-to-day HR operations.

## Lessons Learned
When payroll becomes a planning input, consistency is a governance decision—not an IT feature. The “system” succeeds only when the organization is willing to make its compensation logic explicit.

### ERP Implementation (Microsoft Dynamics AX) (SKY-DAX)
- **Period:** 2008–2010
- **Role:** Solution Architect, Project Manager, MS Dynamics Administrator
- **Employer:** Rostelecom.SkyLink
- **Client:** Rostelecom.SkyLink
- **Industry:** Telecom
- **Domain:** ERP
- **Technologies:** MS Dynamics AX + Integration + HelpDesk
- **Domain tags:** erp, integration
- **Industry tags:** telecom, retail, telecom, retail
- **Role tags:** enterprise-architect, solution-architect, project-manager, dynamics-administrator

**Key Result:** The company gained transparency and timely access to operational data through a unified ERP system. ERP Integrated with Billing and launched a Helpdesk. Standardised landscape and organised transparent reporting, increasing business manageability during the company's pre-sale phase.

# ERP standardization for operational transparency in a pre-sale period

## Context
Rostelecom.SkyLink entered a pre-sale phase where manageability and transparency mattered as much as operational performance. Fragmented operational data and non-standard reporting slowed decision-making and made it harder to demonstrate control over the business.

## The Decision Challenge
The key decision was whether to invest in standardization and a unified operational backbone under time pressure. A conservative path (minor fixes around legacy tools) preserved short-term comfort but risked leaving the organization with the same opacity at the worst moment. A more ambitious path improved transparency but required coordinated change and disciplined scope control.

## Constraints and Trade-offs
The work had to stabilize reporting and data access without disrupting ongoing operations. Integration with billing and support processes increased complexity: the system needed consistent boundaries between operational transactions, customer-facing billing, and user support. The pre-sale context favored predictability and auditability over customization.

## Architectural / Strategic Perspective
The approach centered on a single operational “source of truth” with clear integrations to adjacent systems. Reporting was treated as a management product: consistent definitions, traceability back to operational facts, and repeatable generation. Supportability was addressed as part of the operating model by establishing a clear path for issues and changes.

## Outcome and Impact
The organization gained timely access to operational data through a unified ERP backbone, with integration to billing and an established user support channel. Standardized reporting increased transparency and improved business manageability during the pre-sale period.

## Lessons Learned
In pre-sale environments, enterprise systems are less about features and more about trust: the ability to explain the business with consistent data, repeatable reports, and controlled change.
