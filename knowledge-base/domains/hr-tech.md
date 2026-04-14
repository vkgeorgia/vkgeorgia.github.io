# HR Tech — Projects by Domain

Domain tag: `hr-tech`  
Projects: 3

### AI-Driven Assistant for HR Service Automation (HR-BOT)
- **Period:** 2025
- **Role:** Product Manager
- **Employer:** EPAM
- **Client:** EPAM
- **Industry:** AI Consulting
- **Domain:** HR Workflow Automation
- **Technologies:** OpenAI LLM, Microsoft Semantic Kernel, C#
- **Domain tags:** ai, hr-tech, process-automation
- **Industry tags:** it-services, it-services
- **Role tags:** business-analyst, enterprise-architect, product-manager

**Key Result:** Successfully launched an AI-driven HR assistant (LLM-based) that autonomousy handles 12 HR processes, achieving an 80% deflection rate and delivering a 10x improvement in service speed.

# HR self-service assistant to reduce response time and operational load

## Context
EPAM operated at a scale of 68,000 employees and faced high volume of routine HR inquiries across 12 processes. Human-operated response times often stretched into several days, reducing employee satisfaction and limiting HR capacity for higher-value work.

## The Decision Challenge
The decision challenge was how to introduce an automated assistant that improves speed and consistency without creating new risk through incorrect guidance or poor escalation handling. A low-quality assistant would increase support load and erode trust; a conservative design would fail to reduce operational burden.

## Constraints and Trade-offs
HR processes include policy nuance and exceptions, so automation had to be bounded by a clear escalation model. Higher automation rates require a disciplined knowledge base and feedback loop; faster rollout increases the risk of inconsistent answers. Scaling from an initial user base to the full organization required stability and predictable operations.

## Architectural / Strategic Perspective
The work treated the assistant as part of the HR service operating model: knowledge-driven resolution for routine cases, controlled escalation to human experts, and measurable quality signals to guide continuous improvement. The focus was on decision safety and operational governance rather than on a “chatbot feature set.”

## Outcome and Impact
The assistant served 35,000 employees and continued expanding toward full coverage. Response times dropped from days to minutes, 80% of inquiries were resolved without human intervention, and answer accuracy reached 99%, saving thousands of man-hours per year and reducing operational load on HR.

## Lessons Learned
Service automation succeeds when the organization treats it as a governance problem—clear boundaries, measurable quality, and a reliable escalation path—rather than as a conversational interface.

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
