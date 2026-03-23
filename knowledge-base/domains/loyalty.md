# Loyalty — Projects by Domain

Domain tag: `loyalty`  
Projects: 3

### Loyalty Program Effectiveness Evaluation (RTK-PLE)
- **Period:** 2018
- **Role:** Enterprise Architect
- **Employer:** Rostelecom
- **Client:** Rostelecom
- **Industry:** Telecom
- **Domain:** Digital Marketing
- **Technologies:** The work utilized technologies such as Radius, IoT, Data Management, and DWH for data collection and processing.
- **Domain tags:** loyalty
- **Industry tags:** telecom, telecom
- **Role tags:** enterprise-architect, solution-architect

**Key Result:** A comprehensive approach and methodology were developed for evaluating the effectiveness of loyalty programs. Practical changes were made at the IT systems level to implement the evaluation process, which led to an increase in revenue and profit through additional sales and new marketing initiatives.

# Loyalty program effectiveness evaluation as a management discipline

## Context
Rostelecom had a loyalty program, but it functioned primarily as a points mechanism with limited segmentation, targeting, or analytics. The organization lacked a clear way to evaluate whether the program improved profitability or merely added operational cost.

## The Decision Challenge
The decision challenge was to turn loyalty from a “benefit” into a controllable business instrument by defining how effectiveness is measured and how insights lead to program changes. Without an evaluation method, the organization risks optimizing for activity (points issued) rather than impact (incremental revenue, retention, cross-sell).

## Constraints and Trade-offs
Better measurement requires better data discipline: consistent identifiers, clean event capture, and alignment between marketing intent and system behavior. More granular evaluation increases complexity and governance needs, while overly coarse metrics produce misleading conclusions and debates instead of decisions.

## Architectural / Strategic Perspective
The work framed effectiveness evaluation as a closed loop: define target behaviors, observe them consistently, attribute outcomes, and adjust rules and offers. Practical system-level changes ensured that required events and indicators could be captured and analyzed in a repeatable way.

## Outcome and Impact
A methodology for evaluating loyalty effectiveness was established and enabled through targeted system changes. This provided a basis for new marketing initiatives and contributed to revenue and profit growth through more disciplined additional sales efforts.

## Lessons Learned
Loyalty programs scale in value only when measurement becomes a first-class capability—otherwise the organization can’t tell whether it is buying retention or just subsidizing existing behavior.

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
