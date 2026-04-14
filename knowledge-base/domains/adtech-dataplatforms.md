# Adtech Dataplatforms — Projects by Domain

Domain tag: `adtech-dataplatforms`  
Projects: 4

### DWH Audit (EKHD) (RTK-EKHD)
- **Period:** 2018
- **Role:** Enterprise Architect
- **Employer:** Rostelecom
- **Client:** Rostelecom
- **Industry:** Telecom
- **Domain:** Data Analytics, Data Management
- **Domain tags:** adtech-dataplatforms, analytics, marketing-automation
- **Industry tags:** telecom, telecom
- **Role tags:** enterprise-architect

**Key Result:** A comprehensive analysis of the implementation of the Unified Corporate Data Storage System was conducted, and recommendations for its improvement were provided.

# Post-launch audit and recovery plan for corporate data storage

## Context
Rostelecom had launched a unified corporate data storage system (EKHD) and then encountered visible operational shortcomings: unclear sources, incorrect processing, disorder in storage practices, and missed SLAs. The investment was at risk of becoming a cost center rather than a decision-support foundation.

## The Decision Challenge
The decision challenge was whether to continue investing in a system that was not meeting expectations, and if so, what to change first: technology, data governance, operating processes, or all of the above. Misdiagnosis would either lead to further sunk cost or to superficial fixes that do not restore trust in data.

## Constraints and Trade-offs
The system was already in production, so remediation had to preserve continuity for business users. Improvements needed to address both technical and organizational causes, and sequencing mattered: tightening governance without fixing broken pipelines creates frustration; changing technology without clarifying ownership recreates the same disorder on a new platform.

## Architectural / Strategic Perspective
The audit linked observed problems to an explicit model of sources, flows, storage zones, and ownership responsibilities. Recommendations treated data as a lifecycle-managed asset: clear onboarding rules, controlled transformations, SLA-backed delivery processes, and governance that makes accountability visible.

## Outcome and Impact
The assessment enabled the organization to correct a costly initiative and restore value. Storage costs were reduced by 15%, report preparation time decreased by 4–5×, and the platform became a more reliable basis for management decisions and marketing operations.

## Lessons Learned
Large data platforms fail when accountability is diffuse. Recovery starts when the organization can point to specific ownership and lifecycle rules—not just to “better technology.”

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
