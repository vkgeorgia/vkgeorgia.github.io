# Mobility — Projects by Domain

Domain tag: `mobility`  
Projects: 1

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
