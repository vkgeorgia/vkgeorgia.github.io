# Finance — Projects by Industry

Industry tag: `finance`  
Projects: 4

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
