# Analytics — Projects by Domain

Domain tag: `analytics`  
Projects: 9

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
