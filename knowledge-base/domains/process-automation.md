# Process Automation — Projects by Domain

Domain tag: `process-automation`  
Projects: 5

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

### Agentic AI POC (TRANS-AIPOC)
- **Period:** 2025
- **Role:** Enterprise Architect
- **Employer:** Transitrix
- **Client:** Transitrix
- **Industry:** AI Consulting
- **Domain:** Workflow Automation
- **Domain tags:** architecture, process-automation
- **Industry tags:** ai-consulting, consulting
- **Role tags:** enterprise-architect

**Key Result:** Successfully demonstrated the practical applicability and value of automating the Product Development Process based on AI agents, leading to negotiations for full-scale implementation.

# AI-agent proof-of-concept for product development process automation

## Context
A client’s product development process for launching and evolving confectionery products for the European market was lengthy and unpredictable. The process involved iterative workflows across multiple functions, making it difficult to forecast timelines and manage a product portfolio effectively.

## The Decision Challenge
The decision challenge was whether AI agents could reduce cycle time and increase predictability without turning the process into a fragile automation layer. A poor POC would demonstrate “automation theater” rather than producing credible evidence that the approach can be governed and scaled.

## Constraints and Trade-offs
Product development includes complex exceptions and human judgment, limiting how much can be automated safely. Increasing automation improves speed potential but raises risks around correctness, traceability, and stakeholder trust. A POC needed to focus on decision-relevant fragments and make outcomes measurable.

## Architectural / Strategic Perspective
The work treated the process as a sequence of decision points and artifacts, identifying where agent-based support can reduce coordination cost and where human judgment must remain primary. The design emphasized traceability and analytics so the organization can observe process state and performance, not just “run bots.”

## Outcome and Impact
A working proof-of-concept demonstrated the practicality of automating selected product development activities with AI agents. The client confirmed potential cycle time reduction (up to 5×) and moved into negotiations for a full-scale implementation.

## Lessons Learned
Agent-based automation is compelling when it turns a complex process into an observable system—where work state, ownership, and decisions are trackable—rather than simply replacing people with scripts.

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
