# Business Analyst — Projects by Role

Role tag: `business-analyst`  
Projects: 24

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

### Autorisation Cockpit (DANF-ACO)
- **Period:** 2023–2024
- **Role:** Solution Architect
- **Employer:** EPAM
- **Client:** Danfoss
- **Industry:** Manufacturing
- **Domain:** AAA
- **Domain tags:** architecture
- **Industry tags:** manufacturing, consulting
- **Role tags:** business-analyst, solution-architect, product-manager

**Key Result:** A clear implementation roadmap and a capability map were developed, enabling the client to select the right vendor and launch development with a clear, cost-effective plan that met business needs.

# Authorization cockpit planning under MVP time pressure

## Context
Danfoss needed a new authorization management application for users and partners, with an MVP expected within the year. The initiative required clarity on scope, priorities, and how the solution fits the broader identity and access landscape.

## The Decision Challenge
The decision challenge was to define an MVP that is meaningful and safe: enough capability to support partner authorization needs, but not so much that it becomes a multi-year program. Vendor choice also depended on an explicit view of required capabilities and the organization’s constraints.

## Constraints and Trade-offs
Time-to-MVP limited how much could be built or standardized in the first iteration. Reuse of existing UI components reduced delivery risk but constrained design flexibility. Centralization improves governance, but it increases dependency on shared services and decision-making speed.

## Architectural / Strategic Perspective
The work focused on capability-based reasoning: what authorization decisions must be supported, what context is required, and how policy governance should work over time. A prioritized backlog and roadmap were used to make trade-offs explicit for both vendor selection and internal planning.

## Outcome and Impact
A capability map, prioritized scope, and implementation roadmap were established, supporting a cost-effective vendor selection and enabling the transition from uncertainty to a controlled build plan.

## Lessons Learned
Identity initiatives fail when MVP scope is defined by features; they succeed when MVP is defined by the minimum decision set the organization must control safely.

### Unified Profile Storage (EPM-PSR)
- **Period:** 2022
- **Role:** Lead Business Analyst
- **Employer:** EPAM
- **Client:** EPAM
- **Industry:** IT Services
- **Domain:** HR, Data Management, Workflow Management
- **Domain tags:** architecture
- **Industry tags:** it-services, it-services
- **Role tags:** business-analyst, enterprise-architect, solution-architect

**Key Result:** Client profile architecture was developed, profile storage prepared, and data migration successfully completed, accounting for dynamic system changes and format transformations, leading to active integration by consuming systems.

# Profile storage and migration to operationalize unified profiles

## Context
After establishing a unified profile concept, EPAM needed a practical implementation: centralized profile storage that consolidates data from multiple sources and provides reliable access for consuming systems. Without a shared storage capability, the concept would remain theoretical and fragmentation would persist.

## The Decision Challenge
The decision was how to implement profile storage in a way that remains stable while source systems evolve. A one-time migration would not survive dynamic changes in source formats and rules; a more robust approach required explicit operating rules and controlled transformations, increasing initial complexity.

## Constraints and Trade-offs
Source systems were changing over time, and profile data required transformation and normalization. Strong consistency improves trust but can slow onboarding of new sources; faster onboarding increases the risk of inconsistent profile semantics. The solution needed to be attractive enough that consuming systems would adopt it rather than building their own copies.

## Architectural / Strategic Perspective
The work treated profile storage as a governed data product: defined profile semantics, explicit ingestion and transformation rules, and predictable consumption patterns. Migration planning focused on integrity—verifiable mappings and controlled evolution—so the organization can keep a single profile contract even as sources change.

## Outcome and Impact
A profile storage capability and migration approach were established, enabling consuming systems to integrate around a unified profile source. The organization gained a scalable base for further expansion of profile-driven processes and access control.

## Lessons Learned
Unified profile initiatives fail when migration is treated as “moving data”; they succeed when profile semantics are treated as a living contract with controlled evolution.

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

### Enterprise Architecture (RTK-EA)
- **Period:** 2017–2019
- **Role:** Enterprise Architect
- **Employer:** Rostelecom.Restream
- **Client:** Rostelecom.Restream
- **Industry:** Telecom
- **Domain:** Enterprise Architecture, OCM
- **Domain tags:** architecture
- **Industry tags:** telecom, telecom, consulting
- **Role tags:** business-analyst, enterprise-architect

**Key Result:** Conducted EA Assessment. Delivered EA baseline and transformation roadmap.

# EA baseline and transformation roadmap for managed growth

## Context
Rostelecom.Restream was expanding and needed growth to remain manageable rather than accidental. Leadership required a clear view of the current enterprise state and a roadmap that could guide change decisions across processes, systems, and technology.

## The Decision Challenge
The central decision was how to translate a broad ambition (“grow”) into an actionable transformation sequence. Without a shared baseline and target direction, initiatives compete, dependencies become hidden, and change becomes expensive and risky to coordinate.

## Constraints and Trade-offs
The assessment had to balance completeness with usefulness: documenting everything delays decisions, but shallow documentation produces a roadmap that cannot be trusted. Stakeholder perspectives differed across organizational levels, requiring alignment on what matters most for near-term decisions versus long-term evolution.

## Architectural / Strategic Perspective
The work structured the enterprise into a baseline view and a target direction, with explicit dependencies and phased steps. The focus was on making trade-offs visible—sequencing, ownership, and implications across business architecture and enabling systems—so leadership could make informed commitments.

## Outcome and Impact
An EA baseline and transformation roadmap were established, providing management with a shared foundation for strategic and organizational decisions and a clearer path for subsequent change implementation.

## Lessons Learned
Roadmaps become valuable when they shift conversations from “what to build” to “what sequence of decisions reduces risk while keeping the organization able to move.”

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

### B2B Mailing Automation (RTK-B2B)
- **Period:** 2017–2019
- **Role:** Business Analyst
- **Employer:** Rostelecom
- **Client:** Rostelecom
- **Industry:** Telecom
- **Domain:** Data Analytics, Digital Marketing
- **Domain tags:** marketing-automation, omni-channel
- **Industry tags:** telecom, telecom
- **Role tags:** business-analyst, solution-architect

**Key Result:** Architecture for a multi-channel communication system for B2B interaction was developed. Documentation was handed over for implementation, which led to increased additional sales and customer satisfaction.

# B2B multichannel communications capability for targeted outreach

## Context
Rostelecom’s communication with client organizations lacked a consistent mechanism for segmentation and targeted outreach. Without a managed approach, outreach was either broad and noisy or slow and manual, limiting cross-sell and retention opportunities.

## The Decision Challenge
The decision was whether to treat B2B communications as campaign-by-campaign work or to establish a reusable capability with clear segmentation rules and controlled distribution. A poor decision would either increase operational burden (if overly manual) or introduce communication risk (if automated without governance).

## Constraints and Trade-offs
B2B communications require careful audience definition, approvals, and traceability to avoid damaging relationships. Scaling outreach depends on standardizing rules for recipient selection, content approval, and channel execution, but standardization can reduce flexibility for unique account situations.

## Architectural / Strategic Perspective
The solution was structured around a governed communication pipeline: how segments are defined, where recipient data is sourced, how approvals are recorded, and how distribution is run across channels. Documentation was treated as a risk-reduction mechanism—making rules explicit so implementation effort and misinterpretation risk drop.

## Outcome and Impact
An architecture and documentation package for a multichannel B2B communication system clarified how targeted mailings could be run safely. After implementation, the organization gained the ability to run segmented outreach that supported additional sales and improved customer experience.

## Lessons Learned
Communication automation only scales when the organization is willing to formalize its rules—especially approvals and recipient logic—so that speed does not come at the cost of trust.

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

### Data Management Platform (DMP) (RTK-DMP)
- **Period:** 2017–2019
- **Role:** Enterprise Architect, Solution Architect
- **Employer:** Rostelecom
- **Client:** Rostelecom
- **Industry:** Telecom
- **Domain:** Data Management, Digital Marketing
- **Technologies:** Big Data, Hadoop
- **Domain tags:** adtech-dataplatforms, analytics, marketing-automation
- **Industry tags:** telecom, telecom
- **Role tags:** business-analyst, solution-architect

**Key Result:** Architecture for a DMP was created and a business-driving implementation was proposed, which allowed the company to launch several new profitable businesses and get a foundation for building a business for years to come.

# Data management platform architecture to productize telecom data

## Context
Rostelecom generated large volumes of data through core telecom services. The organization saw the opportunity to turn that data into internal decision support and external products, but that required a coherent infrastructure and operating model beyond ad-hoc analytics.

## The Decision Challenge
The decision was whether to scale data usage through a platform approach or through isolated solutions for each use case. Isolated solutions can produce quick wins, but they accumulate duplicated onboarding work, inconsistent definitions, and growing governance risk. A platform approach requires higher upfront clarity and prioritization.

## Constraints and Trade-offs
Different consumers demand different SLAs and governance controls. A generic platform without prioritization risks becoming an expensive “warehouse of everything”; a narrow platform risks constraining future product ideas. The platform also needed to align with the operating reality of the Data Lab function.

## Architectural / Strategic Perspective
The work structured the future platform across business architecture, information concepts, and the data layer—explicitly connecting data suppliers, processing responsibilities, and consumption patterns. The emphasis was on making the roadmap practical: what must be standardized early, and what can evolve as products prove demand.

## Outcome and Impact
An architectural package for a DMP and a business-driven implementation direction were established and handed over for implementation, enabling the organization to pursue multiple data-based products and build a longer-term foundation for monetizing insights.

## Lessons Learned
The most valuable data platform outcome is not a repository; it is a repeatable way to onboard data and turn it into governed products without reinventing definitions every time.

### Proteus - Data Management System (Traffic analyser, segmentation, targeting, recommendation) (RTK-PROTEUS)
- **Period:** 2016–2018
- **Role:** Business Analyst
- **Employer:** Rostelecom.Restream
- **Client:** Rostelecom.Restream
- **Industry:** Telecom
- **Domain:** Data Analytics, Digital Marketing
- **Technologies:** Web, Cisco, Java
- **Domain tags:** adtech-dataplatforms, analytics, marketing-automation, omni-channel
- **Industry tags:** telecom, telecom
- **Role tags:** business-analyst

**Key Result:** The system was launched and as a result allowed the creation of a new business within the company, generating additional profit, and provided capabilities for targeted advertising messages and a recommendation system.

# Traffic analytics and targeting capability for new revenue streams

## Context
Rostelecom.Restream sought profit growth and considered targeted advertising on owned resources as a viable path. That direction required turning user traffic and interest signals into segments and actionable targeting decisions, not just collecting logs.

## The Decision Challenge
The decision was how to structure a capability that is commercially useful while remaining defensible: segmenting users and inferring interests can create business value, but it also amplifies risks around data quality, explainability, and operational governance. A weak foundation would produce targeting that cannot be trusted and a business model that does not scale.

## Constraints and Trade-offs
Multiple analytical steps (identity resolution, segmentation, interest graph) introduce compounding error. Increasing sophistication improves potential uplift but raises operational and reputational risk if the logic is opaque. The system needed to support both business needs (targeting and recommendations) and the organization’s ability to govern and evolve the capability.

## Architectural / Strategic Perspective
The work framed the solution as a decision pipeline: from traffic signals to identity to segment membership to targeting actions. The focus was on clear module boundaries, explicit requirements for data inputs/outputs, and traceability—so commercial decisions remain explainable even as models and rules evolve.

## Outcome and Impact
A traffic analysis and targeting system went live, enabling a new targeted advertising business line and supporting recommendation capabilities. The organization gained a scalable foundation for monetizing owned traffic through segmented communication.

## Lessons Learned
Monetization of user data is less about algorithms than about governance: when the organization can explain, control, and iterate the logic safely, revenue becomes repeatable rather than opportunistic.

### Interface layer
(information presentation system, data marts) (RTK-DASH)
- **Period:** 2016–2018
- **Role:** Business Analyst
- **Employer:** Rostelecom.Restream
- **Client:** Rostelecom.Restream
- **Industry:** Telecom
- **Domain:** Analytics
- **Technologies:** Big Data, BI, DWH
- **Domain tags:** analytics
- **Industry tags:** telecom, telecom
- **Role tags:** business-analyst

**Key Result:** Analysis and audit of the existing solution were performed, and documentation for changes to the information presentation system and data marts was prepared.

# Audit of reporting interface layer and data marts

## Context
Rostelecom.Restream depended on an interface layer and data marts to make operational and analytical data usable for business teams. The existing solution required review: misalignment with business needs, performance issues, or unclear ownership patterns can turn reporting into a bottleneck.

## The Decision Challenge
The decision was how to stabilize information access: whether to keep extending the existing layer with tactical fixes or to re-establish a coherent model of what data products exist, who owns them, and how they are consumed. A poor approach would prolong ambiguity and raise the cost of every new report or change request.

## Constraints and Trade-offs
Business units depend on reporting while the underlying data landscape continues to evolve. Increasing rigor in data marts improves quality and performance, but it also requires tighter governance and a clearer data lifecycle. The work had to produce actionable documentation that engineering teams could use, not just observations.

## Architectural / Strategic Perspective
The audit focused on system boundaries, data flows, and the mapping between business questions and data products. The goal was to reduce “unknowns”: clarify bottlenecks, document dependencies, and establish requirements for change that align business intent with technical feasibility.

## Outcome and Impact
A comprehensive analysis of the current solution and a documentation package for required changes were prepared, creating a stable basis for improving data accessibility and reducing risk in subsequent enhancements.

## Lessons Learned
Reporting platforms fail quietly: not by crashing, but by making every new decision slower. Clear data product boundaries and ownership are often the highest-leverage fix.

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

### Project 'Storage' (RTK-SDS)
- **Period:** 2016
- **Role:** Enterprise Architect, Business Analyst
- **Employer:** Rostelecom.Restream
- **Client:** Rostelecom.Restream
- **Industry:** Telecom
- **Domain:** SDS, Data Storage
- **Domain tags:** analytics, architecture
- **Industry tags:** telecom, telecom
- **Role tags:** business-analyst

**Key Result:** Customer requirements were analysed, and a balanced solution for enterprise data storage (SDS - Software Defined Storage) was proposed, which allowed the organisation to make the right choice, enhance data reliability, availability, and processing speed, and save significant funds.

# Enterprise storage option selection under mixed data needs

## Context
Rostelecom.Restream worked with growing data volumes and a mix of structured and unstructured datasets. Different departments had different views on storage and processing needs, which created fragmentation risk and made “one-size-fits-all” decisions hard to justify.

## The Decision Challenge
The decision was how to select an enterprise storage direction that balanced reliability, accessibility, and performance without overpaying or locking the organization into a mismatched approach. The risk of getting it wrong was both financial (unjustified spend) and operational (slow processing, reduced availability, inconsistent practices across teams).

## Constraints and Trade-offs
Data types had different lifecycles and access patterns, which implied different storage strategies. Centralization improves governance and efficiency, but it can reduce team autonomy if it forces a single model onto all workloads. The selection needed to remain explainable to an architectural committee and actionable for implementation.

## Architectural / Strategic Perspective
The work organized the problem around data categories and lifecycles, then translated those into requirements and constraints for storage capabilities. Options were evaluated by explicitly comparing advantages and disadvantages, focusing on controllability and fit rather than claiming a universally “best” choice.

## Outcome and Impact
Balanced storage options were presented with clear trade-offs, enabling a defensible selection. The organization improved expectations around reliability and availability and avoided unjustified costs by aligning storage choices with actual data lifecycles.

## Lessons Learned
Storage decisions are rarely about capacity; they are about making lifecycle assumptions explicit so that the organization can govern data consistently as volumes and use cases evolve.

### IoT + Big Data for the Retail Chain (GAM-X5)
- **Period:** 2015
- **Role:** Enterprise Architect
- **Employer:** Gamma
- **Client:** X5
- **Industry:** Retail
- **Domain:** IoT, Food Retail
- **Technologies:** IoT, Big Data, BI
- **Domain tags:** architecture, industrial-iot-bim
- **Industry tags:** retail, consulting, it-services
- **Role tags:** business-analyst, enterprise-architect, solution-architect

**Key Result:** The client received a chosen architectural solution and a clear roadmap, laying the foundation for significant savings.

# Monitoring and predictive maintenance concept for retail climate equipment

## Context
X5 Retail Group faced product losses and elevated electricity costs due to inconsistent temperature control in stores. Equipment failures were handled reactively, with limited ability to plan maintenance or understand systemic drivers of downtime and spoilage.

## The Decision Challenge
The decision was how to structure an investment in monitoring and predictive maintenance so that it produces measurable impact (including a 10% electricity cost reduction target) without creating a solution that stores cannot operate consistently. The risk of choosing poorly was high: either continued losses from downtime/spoilage or a costly initiative with unclear economics.

## Constraints and Trade-offs
Retail environments impose practical constraints: diverse store formats, existing equipment heterogeneity, and limited tolerance for operational disruption. Vendor selection and architecture needed to balance speed to rollout against long-term flexibility and data ownership. Predictive capabilities depend on data quality and consistent instrumentation, which are costly to standardize.

## Architectural / Strategic Perspective
The work compared credible architectural paths and made the economic logic explicit: what data is needed, where it is captured, how it is governed, and how insights become operational decisions (alerts, maintenance planning, reporting). Options were evaluated as different trade-offs between implementation complexity, controllability, and expected value.

## Outcome and Impact
Two architectural options, a vendor evaluation approach, and a phased roadmap were prepared to support a tender decision. The organization gained a clear basis for selecting a path toward reduced losses, more predictable maintenance, and measurable energy efficiency improvements.

## Lessons Learned
Predictive maintenance programs are won or lost in the operating model: if stores cannot trust and act on signals consistently, analytics never turns into savings.

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
