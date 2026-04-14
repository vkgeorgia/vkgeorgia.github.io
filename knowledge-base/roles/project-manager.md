# Project Manager — Projects by Role

Role tag: `project-manager`  
Projects: 11

### Data Lab (RTK-DL)
- **Period:** 2017–2019
- **Role:** Business Architect
- **Employer:** Rostelecom
- **Client:** Rostelecom
- **Industry:** Telecom
- **Domain:** Data Analytics, Digital Marketing
- **Technologies:** Hadoop, Data Lake
- **Domain tags:** adtech-dataplatforms, analytics, marketing-automation
- **Industry tags:** telecom, telecom
- **Role tags:** business-analyst, enterprise-architect, project-manager, business-architect

**Key Result:** A new subdivision was created to handle data for the marketing department. The data includes consumer behavior. Tools for behavior analysis, segmentation, omnichannel communication, and a recommendation system were created.

# Establishing a marketing data analytics subdivision

## Context
Rostelecom needed to use large-scale behavioral data (visited sites, interests, web activity) to strengthen marketing outcomes: more precise targeting, timely churn response, and new data-driven products. The gap was not only technical—there was no dedicated operating model for turning this data into repeatable business capability.

## The Decision Challenge
The decision was whether to treat behavioral data as a byproduct of telecom services or as a strategic asset that justifies a dedicated organization, tools, and governance. Creating a new subdivision is costly and politically sensitive; failing to do so risks leaving valuable data unused and limiting the company’s marketing competitiveness.

## Constraints and Trade-offs
The subdivision needed a clear mandate and measurable outcomes, otherwise it would become an “analytics lab” without business pull. Using previously ignored data required agreement on ownership and quality expectations. Building a broad platform too early risked wasted effort; focusing too narrowly risked missing future product opportunities.

## Architectural / Strategic Perspective
The work framed the subdivision as a capability portfolio: behavior analysis, segmentation, omnichannel activation, and recommendations as connected decision loops. The emphasis was on defining responsibilities, interfaces to data suppliers/consumers, and metrics that let leadership assess whether the function is producing business value.

## Outcome and Impact
A new subdivision was created with analysts, project managers, and technical specialists, enabling systematic use of previously untapped behavioral data. The capability became a foundation for multiple data-driven products, including targeted advertising and recommendation-driven initiatives.

## Lessons Learned
Data organizations succeed when they are designed as product functions—with clear outcomes and decision rights—rather than as a collection of tools and experiments.

### Fleet Management (GAM-CAR5)
- **Period:** 2015–2017
- **Role:** Solution Architect, PM
- **Employer:** Gamma
- **Client:** CAR5
- **Industry:** Transport
- **Domain:** Fleet Management, AWS, Cloud
- **Technologies:** PHP, Web, 1C, AWS Cloud
- **Domain tags:** mobility
- **Industry tags:** transport, consulting, it-services
- **Role tags:** solution-architect, project-manager

**Key Result:** Delivered an integrated carsharing management system from scratch, including infrastructure migration to AWS Cloud, significantly improving transparency and system reliability.

# Carsharing service launch with cloud-based fleet operations

## Context
CAR5 planned a carsharing launch from zero, requiring an operational backbone for fleet availability, customer interaction, and integration with in-car devices and external service providers. The viability of the business depended on reliability and the ability to scale with growth in users and vehicles.

## The Decision Challenge
The central decision was how to design for reliability and scalability before real-world load patterns were known. A minimal build risked rework and fragility under growth; a heavy upfront design risked overinvestment and slow time-to-market.

## Constraints and Trade-offs
The solution needed dependable signals from vehicles and predictable behavior across multiple external dependencies. Operational transparency mattered as much as features: the business needed to understand what the fleet was doing and why. Moving to a cloud environment improved resilience but introduced new operational disciplines and cost controls.

## Architectural / Strategic Perspective
The work treated the platform as a coordination system: clear domain boundaries (customer actions, fleet state, payments, device telemetry), explicit integration contracts, and an operating model that anticipates partial failures. The architecture emphasized observability and fault containment so incidents stay localized and operational decisions remain possible during disruptions.

## Outcome and Impact
A carsharing service went live with web and mobile channels and an integrated fleet management backbone. Cloud-based infrastructure increased reliability and improved operational transparency, creating a scalable base for growth.

## Lessons Learned
Early-stage platforms succeed when reliability is designed as a business capability—so that the organization can keep making decisions even when parts of the ecosystem misbehave.

### Omnichannel Communications (GAM-VTB)
- **Period:** 2015–2018
- **Role:** Business Analyst, Project Manager
- **Employer:** Gamma
- **Client:** VTB Pension Fund
- **Industry:** Finance
- **Domain:** Digital Marketing
- **Technologies:** Web, PHP
- **Domain tags:** omni-channel
- **Industry tags:** finance, consulting, it-services
- **Role tags:** business-analyst, project-manager

**Key Result:** The system successfully sent hundreds of thousands of messages per week, reduced message preparation time by 10 times, and enabled event-based mailings to be completed in one day, significantly enhancing communication efficiency and quality.

# Omnichannel client notifications under compliance and volume constraints

## Context
VTB Pension Fund needed to communicate with clients reliably and at scale. Communication processes were fragmented: no unified recipient lists, limited segmentation, and inconsistent scenarios, which made timely and accurate notifications difficult.

## The Decision Challenge
The decision was whether to keep operating as a set of ad-hoc mailings or to establish a managed communication capability across channels. The cost of getting it wrong was both operational (missed or late messages at scale) and reputational, especially when clients depend on timely information about their accounts.

## Constraints and Trade-offs
Multiple channels introduced compliance, deliverability, and consistency constraints. Higher automation improved speed but required strict governance around templates, approvals, and segmentation rules to prevent errors. The organization needed a process that remained understandable to business owners, not only to IT.

## Architectural / Strategic Perspective
The work approached communication as a governed pipeline: audience definition, scenario design, message templating, approvals, and controlled execution across channels. The goal was predictable behavior—traceable rules, repeatable campaigns, and clear ownership—so volume could increase without increasing failure rates.

## Outcome and Impact
The system supported hundreds of thousands of messages per week. Message preparation time decreased tenfold, and event-based mailings that previously took up to two weeks were completed in one day, improving communication quality and reducing process confusion.

## Lessons Learned
At scale, “messaging” is not content production; it is a decision system where governance, segmentation rules, and operational discipline determine whether automation is safe.

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

### Medical Information System (MIAS) (FMBA-MIAS)
- **Period:** 2012–2015
- **Role:** Project Manager, Business Analyst
- **Employer:** FMBA
- **Client:** The Federal Medical-Biological Agency (FMBA)
- **Industry:** Healthcare
- **Domain:** Workflow Automation
- **Technologies:** Mongo DB, Ruby, Rabbit MQ
- **Domain tags:** analytics, patient-examination-system
- **Industry tags:** healthcare, consulting, it-services
- **Role tags:** solution-architect, project-manager

**Key Result:** Delivered a medical analytics system for FMBA to forecast athletes' performance and support training plans based on health assessments.

# Medical analytics for athlete health assessment and planning

## Context
The Federal Medical-Biological Agency needed a more systematic way to collect and use medical data related to athletes’ health assessments. Without a consolidated analytical view, forecasting performance trends and adjusting training plans relied too heavily on fragmented information and individual interpretation.

## The Decision Challenge
The decision was how to turn medical assessments into actionable planning input without overstating certainty. A system that only stores data does not change outcomes; a system that claims predictive power without disciplined assumptions creates false confidence. The challenge was to support informed judgment under medical and performance constraints.

## Constraints and Trade-offs
Medical data sources and assessment methods vary, and adoption depends on usability for clinicians and coaches. The solution needed to support analytical insights while maintaining traceability back to assessments. Speed and breadth of data coverage had to be balanced against consistent interpretation and reporting.

## Architectural / Strategic Perspective
The work emphasized an information architecture where assessments, indicators, and planning outputs are explicitly related. Analytical components were treated as decision support: transparent inputs, clear outputs, and repeatable reporting rather than opaque “predictions”. Integration of sources was approached as an operating discipline—consistent capture and curation before analytics.

## Outcome and Impact
FMBA gained a medical information and analytical system that supports forecasting and provides structured input into training planning based on health assessments. The organization’s ability to work with athlete medical data became more consistent and repeatable.

## Lessons Learned
In health-related analytics, the most important outcome is not a forecast—it is a shared, traceable basis for decisions that remain accountable to the underlying assessments.

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
