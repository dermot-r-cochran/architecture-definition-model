---
layout: page
title: Overview
permalink: /overview/
---

This page is normative and defines ADM semantics.

# Overview

The Architecture Definition Model (ADM) is a structured way to describe an AI system without mixing purpose, policy, design, runtime structure, and implementation details together.

In practice, ADM helps answer questions like:

- Why does this system exist?
- What context and constraints shape it?
- What capability is being provided?
- What interfaces expose that capability?
- What units execute it?
- What components implement it?
- What technical interfaces connect it?
- What rules and decisions govern it?

ADM exists to keep architecture explicit, reviewable, and stable. It separates meaning from implementation so that a system can evolve without losing architectural clarity.

## Why ADM Uses Layers

Architectural descriptions often become confusing because different kinds of statements are mixed together. For example:

- a business goal is written beside an API contract
- a safety constraint is confused with a component
- a runtime worker is described as if it were a user-facing capability
- an implementation choice is presented as a governing principle

ADM prevents that confusion by assigning each kind of architectural statement to a defined layer.

Each layer has one purpose.
Each concept has one meaning.
Architecture stays understandable because structure is preserved.

## Canonical Layer Set

The ADM layer set is:

1. Intent
2. Context
3. Capability
4. Service Interface
5. Execution Unit
6. Component
7. Technical Interface
8. Agent
9. Constraints
10. Decisions

The vertical layers refine architecture from purpose toward implementation-facing structure.

The horizontal layers apply across the model:

- **Agent** describes agent-specific behavior and responsibilities where applicable
- **Constraints** define limits, obligations, and prohibitions
- **Decisions** record deliberate architectural choices and rationale

## How ADM Relates to C4

ADM is the authoritative model for architecture semantics, governance, and conformance.
C4 is a diagramming framework used to communicate architecture at multiple zoom levels.

C4 views should be derived from ADM and must not redefine ADM layers or meanings.
For detailed guidance, see [ADM and C4: Complementary, Not Competing]({{ site.baseurl }}/adm-and-c4/).

## Running Example: AI Support Assistant

Consider an AI support assistant used by customers to ask product and troubleshooting questions.

### Intent
Why does the system exist?

- Reduce support response time
- Improve answer consistency
- Preserve auditability and safety
- Escalate uncertain cases to a human

### Context
What environment and conditions shape the system?

- Customers ask questions through a web portal
- Answers may affect regulated product usage
- Human support staff must remain part of the process
- Responses must be logged for review

### Capability
What ability does the system provide?

- Answer product-support questions
- Retrieve relevant product guidance
- Identify uncertainty and trigger escalation

### Service Interface
How is that capability presented to consumers?

- A chat interface for customers
- An internal escalation request interface for support staff
- A feedback submission interface for answer quality review

### Execution Unit
What runtime units perform the work?

- A request handler for incoming chat messages
- A retrieval pipeline that gathers relevant documents
- A response generation worker
- An escalation evaluator

### Component
What architectural building blocks implement the system?

- Conversation manager
- Retrieval service
- Policy checker
- Answer composer
- Audit logger

### Technical Interface
What concrete technical contracts connect the system?

- HTTP endpoints
- Internal service calls
- event messages
- storage APIs
- model invocation APIs

### Agent
Where an agent is used, what role does it play?

- Interpret the user request
- decide whether enough information is available
- propose an answer
- decline or escalate when policy requires it

### Constraints
What limits govern the system?

- The system must not invent unsupported claims
- High-risk advice must be reviewed or escalated

### Decisions
What deliberate choices were made, and why?

- Uncertain cases are escalated to a human rather than answered with a hedge, because answers may affect regulated product usage (Context) and the system exists to escalate uncertain cases (Intent)
- Answers are composed only from retrieved product guidance, because unsupported claims are forbidden (Constraints) and a retrieved source can be audited
- Every exchange is logged before the answer is shown, accepting the added latency, because responses must be logged for review (Context)

Each decision references elements already placed in the layers above and defines none of its own; that is what keeps it in the Decisions layer.
