---
title: "A New Compliance Obligation Lands — What Does It Affect?"
standfirst: "If the honest answer is that a workshop is needed to find out, this is an architecture problem, not a legal one."
description: "Impact analysis as a query over an enterprise model: requirements, processes, products, data and owners as objects and relationships, so the blast radius of a new obligation is a subgraph rather than a month of workshops."
lang: en
image: /assets/og/a-new-compliance-obligation-what-does-it-affect.png
---

The EU AI Act reclassifies one of your systems as "high-risk." Which processes, what data, and which owners does this affect? If the honest answer is "a workshop is needed to find out," then this is an architectural issue, not a legal one.

When a new legal requirement emerges, the first question is always the same: "What will this affect?"

You start convening workshops, gathering everyone involved, and discussions and debates begin. Weeks, even months, pass. And the questions—"What's left uncovered?", "How long will it take to make the changes?" and "How much will it cost?"—still remain unanswered.

To organize my work correctly, I consider requirements in relation to the objects they affect. A requirement is an object. A process or product is also an object. And the fact that a requirement affects a process or product is a relationship. Each process has an owner, and this connection can also be traced. This way, you can create a traceability chain for the impact of legal requirements and standards on your products, processes, and business capabilities.

It's convenient to create such a traceability chain when you have a model of your enterprise. Essentially, impact analysis turns into a traversal of objects along the edges of the graph. In my case, the enterprise model lives as text under the Architecture-as-Code (Transitrix) methodology: law, requirement, process, product, data, and owner are objects with connections that are stored in a repository and versioned. The graph in the diagram is not a drawing, but the result of an impact query based on this model.

![The EU AI Act reclassifies a system as high-risk: the obligation is asserted on a process and a product, which in turn reach a capability, two data stores and their owners — and two of the affected objects carry no admitted control yet](/assets/articles/compliance-obligation-blast-radius.png)

Here's the example of the EU AI Act: in one run, the model shows, say, seven processes, three products, two data stores, and four owners affected by the reclassification to "high risk"—and that for two of the affected entities, no controls yet satisfy the requirement. This is the impact and the gap combined in a single pass, without a workshop.

Impact is simply a query to the model, while the blast radius is simply a subgraph you receive in response to the query. Moreover, the same query can be run on a draft law—even before it's passed—and the blast radius can be seen in advance. Thus, the enterprise architect becomes someone called in before a decision, not after an incident: they predict the consequences of a change, rather than fixing problems after the fact.

Still, it's important to remember that impact analysis using a model is more of a tool for a team of experts and a basis for discussion. A model helps conduct an impact analysis quickly, while the final decision on the impact of legal requirements on the business should rest with a human.

This is how the "Architecture-as-Code" concept helps me track the impact of legislation in my project.
