# Integration — Projects by Domain

Domain tag: `integration`  
Projects: 2

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
