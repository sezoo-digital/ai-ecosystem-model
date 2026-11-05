---
title: AI Ecosystem Multi-Lens Architecture
sidebar_position: 1
slug: /
---

# AI Ecosystem: Multi-Lens Architecture & Governance

Select a lens below to explore the ecosystem. You can also download the raw models for visual editing in **yEd** or **draw.io**.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
<TabItem value="view_economic" label="Executive & Economic View (Value Flows & Commoditization)">

> 📥 **Export to Graphical Tools:** 
> <a href="pathname:///ai-ecosystem-model/exports/view_economic.graphml" download>Download for yEd (.graphml)</a> &nbsp;|&nbsp; 
> <a href="pathname:///ai-ecosystem-model/exports/view_economic.drawio" download>Download for draw.io (.drawio)</a>

```mermaid
flowchart TB
    subgraph cluster_supply ["1. Upstream Foundation & Model Lab"]
        N_TRAIN["<b>Training Supply Chain</b><br/><small><i>Data Curators, Annotators, Compute</i></small>"]
        N_FRONTIER["<b>Frontier Model Instance</b><br/><small><i>Weights & Wholesale Inference API</i></small>"]
        N_ABSORBED["<b>Platform Absorption Zone</b><br/><small><i>Native Tools, Prompt Cache, Hosted State</i></small>"]
    end
    subgraph cluster_product ["2. Specialized Product & Harness Domain (ISV)"]
        N_ISV_PRODUCT["<b>Specialized AI Product</b><br/><small><i>Vertical Solutions (Legal, Medical, Finance)</i></small>"]
    end
    subgraph cluster_client ["3. Enterprise & Principal Domain"]
        N_ENTERPRISE["<b>Enterprise Principal</b><br/><small><i>Budget Holder & Legal Entity</i></small>"]
    end

    N_ENTERPRISE == "$$$ High-Margin SaaS / Outcome Contract" ==> N_ISV_PRODUCT
    N_ISV_PRODUCT == "$$ Wholesale Token Consumption" ==> N_FRONTIER
    N_FRONTIER == "$ Compute & Annotation CapEx" ==> N_TRAIN
    N_ABSORBED -. "Platform Commoditization Pressure" .-> N_ISV_PRODUCT
```

</TabItem>
<TabItem value="view_governance" label="Governance, Rights & Liability View">

> 📥 **Export to Graphical Tools:** 
> <a href="pathname:///ai-ecosystem-model/exports/view_governance.graphml" download>Download for yEd (.graphml)</a> &nbsp;|&nbsp; 
> <a href="pathname:///ai-ecosystem-model/exports/view_governance.drawio" download>Download for draw.io (.drawio)</a>

```mermaid
flowchart TB
    subgraph cluster_supply ["1. Upstream Foundation & Model Lab"]
        N_FRONTIER["<b>Frontier Model Instance</b><br/><small><i>Weights & Wholesale Inference API</i></small>"]
    end
    subgraph cluster_product ["2. Specialized Product & Harness Domain (ISV)"]
        N_HARNESS["<b>Agent Governance Harness</b><br/><small><i>Rights, Duties & Deterministic Sandbox</i></small>"]
        N_MEMORY["<b>State & Persistence Layer</b><br/><small><i>Episodic Vector DBs & Audit History</i></small>"]
    end
    subgraph cluster_client ["3. Enterprise & Principal Domain"]
        N_ENTERPRISE["<b>Enterprise Principal</b><br/><small><i>Budget Holder & Legal Entity</i></small>"]
        N_HUMAN_USER["<b>Human Task Delegator</b><br/><small><i>End User / Operator</i></small>"]
    end
    subgraph cluster_environment ["4. Target Execution Environment"]
        N_MCP_HOST["<b>Protocol Gateway (MCP)</b><br/><small><i>Standardized Tool Discovery & Context</i></small>"]
        N_TARGET_SYS["<b>Target Systems & APIs</b><br/><small><i>Databases, ERPs, Cloud Infrastructure</i></small>"]
    end

    N_ENTERPRISE == "Delegates Authority & Statutory Duties" ==> N_HARNESS
    N_HUMAN_USER == "Human-in-the-Loop Oversight & Overrides" ==> N_HARNESS
    N_FRONTIER -. "Disclaims Liability (ToS Boundary)" .-> N_ENTERPRISE
    N_HARNESS -->|"Mandatory Audit Trail & State Proof"| N_MEMORY
    N_HARNESS -->|"Enforces Least Privilege & Limits"| N_MCP_HOST
    N_MCP_HOST -->|"Constrains Blast Radius"| N_TARGET_SYS
```

</TabItem>
</Tabs>

## Canonical Element Dictionary

| Element | Domains | Properties |
| :--- | :--- | :--- |
| **Training Supply Chain**<br/>`N_TRAIN` | economic, technical | **cost_type**: Fixed / R&D CapEx |
| **Frontier Model Instance**<br/>`N_FRONTIER` | economic, technical, governance | **pricing_model**: Per-Token Usage<br/>**liability_posture**: Disclaimed via ToS |
| **Platform Absorption Zone**<br/>`N_ABSORBED` | economic, technical | **market_effect**: Encroachment on ISVs |
| **Specialized AI Product**<br/>`N_ISV_PRODUCT` | economic, technical | **pricing_model**: SaaS Seat / Outcome Pricing<br/>**margin_profile**: High Gross Margin (Vulnerable) |
| **Agent Governance Harness**<br/>`N_HARNESS` | technical, governance | **enforcement**: Deterministic Policies & Budgets<br/>**audit_role**: Sovereign Audit Ledger |
| **State & Persistence Layer**<br/>`N_MEMORY` | technical, governance | **sovereignty**: Client / Enterprise Owned<br/>**compliance**: GDPR / Audit Logging |
| **Enterprise Principal**<br/>`N_ENTERPRISE` | economic, governance | **liability_posture**: Holds Vicarious Legal Liability<br/>**commercial_role**: Economic Sponsor |
| **Human Task Delegator**<br/>`N_HUMAN_USER` | technical, governance | **control_mode**: Prompting & HITL Approvals |
| **Protocol Gateway (MCP)**<br/>`N_MCP_HOST` | technical, governance | **protocol_standard**: Model Context Protocol<br/>**security**: Scope Negotiation |
| **Target Systems & APIs**<br/>`N_TARGET_SYS` | technical, governance | **risk_zone**: Blast Radius<br/>**access_control**: RBAC / Least Privilege |