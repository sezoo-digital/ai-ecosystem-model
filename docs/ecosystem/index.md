---
title: AI Ecosystem Multi-Lens Architecture
sidebar_position: 1
slug: /
---

import useBaseUrl from '@docusaurus/useBaseUrl';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# AI Ecosystem: Multi-Lens Architecture & Governance

:::tip Download Canonical Models
Download the raw model to explore and query in external visual modeling tools:

- <a href={useBaseUrl("/exports/ai_ecosystem.graphml")} download="ai_ecosystem.graphml">**Download for yEd** (.graphml)</a>
- <a href={useBaseUrl("/exports/ai_ecosystem.drawio")} download="ai_ecosystem.drawio">**Download for draw.io** (.drawio)</a>
- <a href={useBaseUrl("/exports/ai_ecosystem_kumu.csv")} download="ai_ecosystem_kumu.csv">**Download for Kumu** (.csv)</a>
:::

<details>
<summary><strong>📖 Visual Language & Architectural Key (Click to expand)</strong></summary>

```mermaid
flowchart LR
    classDef gov fill:#FFF1F0,stroke:#F5222D,stroke-width:2px;
    classDef econ fill:#F6FFED,stroke:#52C41A,stroke-width:2px;
    classDef tech fill:#E6F7FF,stroke:#1890FF,stroke-width:2px;
    classDef default fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px;

    subgraph LegendShapes ["Architectural Node Archetypes"]
        K_HEXAGON{{"Statutory &amp; Regulatory Authority<br/><small><i>shape: hexagon</i></small>"}}:::gov
        K_CIRCLE(("Human Actor / Natural Person<br/><small><i>shape: circle</i></small>")):::gov
        K_SUBPROC[["Deterministic Gateway &amp; Policy Kernel<br/><small><i>shape: subproc</i></small>"]]:::tech
        K_CYLINDER[("Stateful Store &amp; Critical Data Asset<br/><small><i>shape: cylinder</i></small>")]:::tech
        K_STADIUM(["Identity &amp; Security Issuer<br/><small><i>shape: stadium</i></small>"]):::tech
        K_ROUNDED("Software Service &amp; Inference API<br/><small><i>shape: rounded</i></small>"):::tech
        K_RECT["Organizational &amp; Economic Entity<br/><small><i>shape: rect</i></small>"]:::econ
    end
```

### Node Archetypes (Shapes)

| Shape | Archetype / Meaning | Description |
| :---: | :--- | :--- |
| `hexagon` | **Statutory & Regulatory Authority** | External legal jurisdictions, court systems, conformity auditors (non-negotiable authority). |
| `circle` | **Human Actor / Natural Person** | Human principals, operators (HITL), or impacted third-party individuals. |
| `subproc` | **Deterministic Gateway & Policy Kernel** | Sandboxes, policy harnesses, MCP gateways where strict deterministic logic bounds AI. |
| `cylinder` | **Stateful Store & Critical Data Asset** | Append-only audit stores, vector databases, production databases, target ERPs. |
| `stadium` | **Identity & Security Issuer** | Enterprise IdP, OAuth token issuers, workload authorization brokers. |
| `rounded` | **Software Service & Inference API** | Frontier model endpoints, vertical applications, continuous eval engines. |
| `rect` | **Organizational & Economic Entity** | Commercial deployers, CapEx supply chain entities, market absorption zones. |

### Relationship & Edge Types

| Line Style | Relationship Type | Semantic Meaning |
| :---: | :--- | :--- |
| `== 'label' ==>` | **Capital / Commercial Flow** (`money`) | Financial transactions, SaaS subscriptions, compute CapEx, insurance premiums. |
| `== 'label' ==>` | **Direct Authority & Override** (`authority`) | Statutory mandates, legal agency delegation, mandatory human oversight. |
| `-. 'label' .->` | **Policy Constraint & Audit Trail** (`governance_control`) | Tamper-evident logging, scope enforcement, sandbox boundaries. |
| `-. 'label' .->` | **Liability & Market Tension** (`tension`) | Tort liability exposure, blast radius impact, platform commoditization pressure. |
| `-. 'label' .->` | **Contractual Disclaimer** (`disclaim`) | ToS liability carve-outs and 'AS-IS' warranty limitations. |
| `-->|'label'|` | **Technical Protocol** (`protocol`) | JSON-RPC tool calling, OAuth bearer flows, inference API calls. |
| `-->|'label'|` | **Data & Intent Flow** (`flow`) | Prompt context, telemetry metrics, audit evidence submissions. |

### Domain Boundary Colors

| Color | Domain | Scope |
| :---: | :--- | :--- |
| 🔴 **Red / Pink** | `governance` | Statutory duties, liability allocation, compliance controls, human oversight. |
| 🟢 **Green** | `economic` | SaaS contracts, token consumption costs, GPU CapEx, underwriting fees. |
| 🔵 **Blue** | `technical` | API execution protocols, JSON-RPC (MCP), state persistence, telemetry. |

</details>

### Interactive Lenses
Select a lens below to explore the ecosystem interactively:

<Tabs>
<TabItem value="view_economic" label="Executive & Economic Perspective">

*Capital allocation, SaaS margins, token cost exposure, and platform absorption.*

```mermaid
flowchart TB
    classDef gov fill:#FFF1F0,stroke:#F5222D,stroke-width:2px;
    classDef econ fill:#F6FFED,stroke:#52C41A,stroke-width:2px;
    classDef tech fill:#E6F7FF,stroke:#1890FF,stroke-width:2px;
    classDef default fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px;

    subgraph cluster_regulatory ["0. Jurisdictional & Regulatory Sphere"]
        N_INSURER["AI Risk Underwriter &amp; Insurer<br/><small><i>Cyber &amp; Algorithmic Liability Carrier</i></small>"]:::gov
    end

    subgraph cluster_supply ["1. Upstream Foundation & Model Lab"]
        N_TRAIN["Training Supply Chain<br/><small><i>Data Curators, Annotators, Compute Clusters</i></small>"]:::econ
        N_FRONTIER("Frontier GPAI Lab<br/><small><i>Weights &amp; Wholesale Inference APIs</i></small>"):::gov
        N_ABSORBED["Platform Absorption Zone<br/><small><i>Native Tools, Prompt Cache, Hosted Agent State</i></small>"]:::econ
    end

    subgraph cluster_product ["2. Specialized Product & Harness Domain (ISV / Custom Runtime)"]
        N_ISV_PRODUCT("Specialized AI Application<br/><small><i>Vertical Solutions (Legal, Medical, Finance, Ops)</i></small>"):::econ
        N_OBSERVE("Observability &amp; Evals Engine<br/><small><i>Continuous Evaluation, Traces &amp; Cost Telemetry</i></small>"):::gov
    end

    subgraph cluster_client ["3. Enterprise Deployer & Principal Domain"]
        N_ENTERPRISE["Enterprise Deployer<br/><small><i>Legal Principal &amp; Economic Sponsor</i></small>"]:::gov
    end

    N_ENTERPRISE == "$$$ SaaS Subscription / Outcome Fee" ==> N_ISV_PRODUCT
    N_ISV_PRODUCT == "$$ Token Consumption Cost" ==> N_FRONTIER
    N_FRONTIER == "$ Compute & Data CapEx" ==> N_TRAIN
    N_ABSORBED -. "Platform Commoditization Pressure" .-> N_ISV_PRODUCT
    N_INSURER == "$ Policy Premiums & Underwriting" ==> N_ENTERPRISE
    N_OBSERVE -->|"Real-time Cost & Token Telemetry"| N_ENTERPRISE
```

</TabItem>
<TabItem value="view_governance_liability" label="Legal, Regulatory & Liability Perspective">

*The liability disconnect: upstream ToS disclaimers vs deployer vicarious liability and regulatory enforcement.*

```mermaid
flowchart TB
    classDef gov fill:#FFF1F0,stroke:#F5222D,stroke-width:2px;
    classDef econ fill:#F6FFED,stroke:#52C41A,stroke-width:2px;
    classDef tech fill:#E6F7FF,stroke:#1890FF,stroke-width:2px;
    classDef default fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px;

    subgraph cluster_regulatory ["0. Jurisdictional & Regulatory Sphere"]
        N_REGULATOR{{"Market Surveillance Authorities<br/><small><i>EU AI Office, FTC, DPAs, Courts</i></small>"}}:::gov
        N_AUDITOR{{"Conformity Body &amp; ISO Auditor<br/><small><i>Notified Bodies, ISO/IEC 42001 Certifiers</i></small>"}}:::gov
        N_INSURER["AI Risk Underwriter &amp; Insurer<br/><small><i>Cyber &amp; Algorithmic Liability Carrier</i></small>"]:::gov
    end

    subgraph cluster_supply ["1. Upstream Foundation & Model Lab"]
        N_FRONTIER("Frontier GPAI Lab<br/><small><i>Weights &amp; Wholesale Inference APIs</i></small>"):::gov
    end

    subgraph cluster_product ["2. Specialized Product & Harness Domain (ISV / Custom Runtime)"]
        N_HARNESS[["Agent Governance Harness<br/><small><i>Deterministic Policy Engine &amp; Guardrails</i></small>"]]:::gov
        N_AUDIT_STORE[("Sovereign Audit Ledger<br/><small><i>Tamper-Evident WORM State &amp; Forensic Store</i></small>")]:::gov
        N_OBSERVE("Observability &amp; Evals Engine<br/><small><i>Continuous Evaluation, Traces &amp; Cost Telemetry</i></small>"):::gov
    end

    subgraph cluster_client ["3. Enterprise Deployer & Principal Domain"]
        N_ENTERPRISE["Enterprise Deployer<br/><small><i>Legal Principal &amp; Economic Sponsor</i></small>"]:::gov
        N_IDP(["Enterprise Identity &amp; Auth (IdP)<br/><small><i>OAuth, OIDC, Workload IAM &amp; Ephemeral Tokens</i></small>"]):::gov
        N_HUMAN_USER(("Human Task Delegator &amp; Overseer<br/><small><i>End User / Mandatory HITL Supervisor</i></small>")):::gov
    end

    subgraph cluster_environment ["4. Target Execution Environment & Blast Radius"]
        N_MCP_HOST[["Protocol Gateway (MCP Host)<br/><small><i>Standardized Tool Broker &amp; Context Provider</i></small>"]]:::gov
        N_TARGET_SYS[("Target Systems &amp; Operational APIs<br/><small><i>Databases, Production ERP, Financial Rails</i></small>")]:::gov
        N_AFFECTED_PARTY(("Impacted Third Party<br/><small><i>Consumers, Employees, Citizens</i></small>")):::gov
    end

    N_INSURER == "$ Policy Premiums & Underwriting" ==> N_ENTERPRISE
    N_REGULATOR == "Statutory Compliance & Fines (Art. 71)" ==> N_ENTERPRISE
    N_REGULATOR == "GPAI Codes of Practice & Transparency (Art. 53)" ==> N_FRONTIER
    N_AUDITOR == "Conformity Audits (ISO 42001 / High Risk)" ==> N_ENTERPRISE
    N_FRONTIER -. "Disclaims Liability (ToS 'AS-IS')" .-> N_ENTERPRISE
    N_ENTERPRISE -. "Vicarious Liability for Agent Harm (Respondeat Superior)" .-> N_AFFECTED_PARTY
    N_AFFECTED_PARTY -->|"Complaints & Redress Demands"| N_REGULATOR
    N_ENTERPRISE == "Delegates Authority & Safety Boundaries" ==> N_HARNESS
    N_HUMAN_USER == "Art. 14 Human Oversight & Stop Button" ==> N_HARNESS
    N_HARNESS -. "Cryptographic Tamper-Proof Audit Trail" .-> N_AUDIT_STORE
    N_AUDIT_STORE -->|"Forensic Evidence for Compliance Verification"| N_AUDITOR
    N_HARNESS -. "Enforces Least-Privilege Scopes" .-> N_MCP_HOST
    N_TARGET_SYS -. "Direct Impact & Real-World Blast Radius" .-> N_AFFECTED_PARTY
```

</TabItem>
<TabItem value="view_technical_runtime" label="Engineering & Technical Runtime Perspective">

*The agentic execution loop: IdP delegation, inference protocols, MCP gateways, and state stores.*

```mermaid
flowchart LR
    classDef gov fill:#FFF1F0,stroke:#F5222D,stroke-width:2px;
    classDef econ fill:#F6FFED,stroke:#52C41A,stroke-width:2px;
    classDef tech fill:#E6F7FF,stroke:#1890FF,stroke-width:2px;
    classDef default fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px;

    subgraph cluster_supply ["1. Upstream Foundation & Model Lab"]
        N_TRAIN["Training Supply Chain<br/><small><i>Data Curators, Annotators, Compute Clusters</i></small>"]:::econ
        N_FRONTIER("Frontier GPAI Lab<br/><small><i>Weights &amp; Wholesale Inference APIs</i></small>"):::gov
        N_ABSORBED["Platform Absorption Zone<br/><small><i>Native Tools, Prompt Cache, Hosted Agent State</i></small>"]:::econ
    end

    subgraph cluster_product ["2. Specialized Product & Harness Domain (ISV / Custom Runtime)"]
        N_ISV_PRODUCT("Specialized AI Application<br/><small><i>Vertical Solutions (Legal, Medical, Finance, Ops)</i></small>"):::econ
        N_HARNESS[["Agent Governance Harness<br/><small><i>Deterministic Policy Engine &amp; Guardrails</i></small>"]]:::gov
        N_AUDIT_STORE[("Sovereign Audit Ledger<br/><small><i>Tamper-Evident WORM State &amp; Forensic Store</i></small>")]:::gov
        N_OBSERVE("Observability &amp; Evals Engine<br/><small><i>Continuous Evaluation, Traces &amp; Cost Telemetry</i></small>"):::gov
    end

    subgraph cluster_client ["3. Enterprise Deployer & Principal Domain"]
        N_IDP(["Enterprise Identity &amp; Auth (IdP)<br/><small><i>OAuth, OIDC, Workload IAM &amp; Ephemeral Tokens</i></small>"]):::gov
        N_HUMAN_USER(("Human Task Delegator &amp; Overseer<br/><small><i>End User / Mandatory HITL Supervisor</i></small>")):::gov
    end

    subgraph cluster_environment ["4. Target Execution Environment & Blast Radius"]
        N_MCP_HOST[["Protocol Gateway (MCP Host)<br/><small><i>Standardized Tool Broker &amp; Context Provider</i></small>"]]:::gov
        N_TARGET_SYS[("Target Systems &amp; Operational APIs<br/><small><i>Databases, Production ERP, Financial Rails</i></small>")]:::gov
    end

    N_HARNESS -. "Cryptographic Tamper-Proof Audit Trail" .-> N_AUDIT_STORE
    N_HARNESS -. "Enforces Least-Privilege Scopes" .-> N_MCP_HOST
    N_HUMAN_USER -->|"Prompt Intent & Working Context"| N_ISV_PRODUCT
    N_IDP -->|"Issues Scoped Delegation Token"| N_HARNESS
    N_ISV_PRODUCT -->|"Initiates Autonomous Loop"| N_HARNESS
    N_HARNESS -->|"Inference API (Tokens & Directives)"| N_FRONTIER
    N_HARNESS -->|"Context Retrieval (RAG) & Checkpointing"| N_AUDIT_STORE
    N_HARNESS -->|"Traces & LLM Evaluation Metrics"| N_OBSERVE
    N_HARNESS -->|"JSON-RPC / MCP Tool Discovery & Invocations"| N_MCP_HOST
    N_MCP_HOST -->|"Authenticated Read/Write Operations"| N_TARGET_SYS
```

</TabItem>
<TabItem value="view_full_unified" label="Unified Ecosystem Model">

*The complete property graph combining economic flows, technical loops, and governance gates.*

```mermaid
flowchart TB
    classDef gov fill:#FFF1F0,stroke:#F5222D,stroke-width:2px;
    classDef econ fill:#F6FFED,stroke:#52C41A,stroke-width:2px;
    classDef tech fill:#E6F7FF,stroke:#1890FF,stroke-width:2px;
    classDef default fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px;

    subgraph cluster_regulatory ["0. Jurisdictional & Regulatory Sphere"]
        N_REGULATOR{{"Market Surveillance Authorities<br/><small><i>EU AI Office, FTC, DPAs, Courts</i></small>"}}:::gov
        N_AUDITOR{{"Conformity Body &amp; ISO Auditor<br/><small><i>Notified Bodies, ISO/IEC 42001 Certifiers</i></small>"}}:::gov
        N_INSURER["AI Risk Underwriter &amp; Insurer<br/><small><i>Cyber &amp; Algorithmic Liability Carrier</i></small>"]:::gov
    end

    subgraph cluster_supply ["1. Upstream Foundation & Model Lab"]
        N_TRAIN["Training Supply Chain<br/><small><i>Data Curators, Annotators, Compute Clusters</i></small>"]:::econ
        N_FRONTIER("Frontier GPAI Lab<br/><small><i>Weights &amp; Wholesale Inference APIs</i></small>"):::gov
        N_ABSORBED["Platform Absorption Zone<br/><small><i>Native Tools, Prompt Cache, Hosted Agent State</i></small>"]:::econ
    end

    subgraph cluster_product ["2. Specialized Product & Harness Domain (ISV / Custom Runtime)"]
        N_ISV_PRODUCT("Specialized AI Application<br/><small><i>Vertical Solutions (Legal, Medical, Finance, Ops)</i></small>"):::econ
        N_HARNESS[["Agent Governance Harness<br/><small><i>Deterministic Policy Engine &amp; Guardrails</i></small>"]]:::gov
        N_AUDIT_STORE[("Sovereign Audit Ledger<br/><small><i>Tamper-Evident WORM State &amp; Forensic Store</i></small>")]:::gov
        N_OBSERVE("Observability &amp; Evals Engine<br/><small><i>Continuous Evaluation, Traces &amp; Cost Telemetry</i></small>"):::gov
    end

    subgraph cluster_client ["3. Enterprise Deployer & Principal Domain"]
        N_ENTERPRISE["Enterprise Deployer<br/><small><i>Legal Principal &amp; Economic Sponsor</i></small>"]:::gov
        N_IDP(["Enterprise Identity &amp; Auth (IdP)<br/><small><i>OAuth, OIDC, Workload IAM &amp; Ephemeral Tokens</i></small>"]):::gov
        N_HUMAN_USER(("Human Task Delegator &amp; Overseer<br/><small><i>End User / Mandatory HITL Supervisor</i></small>")):::gov
    end

    subgraph cluster_environment ["4. Target Execution Environment & Blast Radius"]
        N_MCP_HOST[["Protocol Gateway (MCP Host)<br/><small><i>Standardized Tool Broker &amp; Context Provider</i></small>"]]:::gov
        N_TARGET_SYS[("Target Systems &amp; Operational APIs<br/><small><i>Databases, Production ERP, Financial Rails</i></small>")]:::gov
        N_AFFECTED_PARTY(("Impacted Third Party<br/><small><i>Consumers, Employees, Citizens</i></small>")):::gov
    end

    N_ENTERPRISE == "$$$ SaaS Subscription / Outcome Fee" ==> N_ISV_PRODUCT
    N_ISV_PRODUCT == "$$ Token Consumption Cost" ==> N_FRONTIER
    N_FRONTIER == "$ Compute & Data CapEx" ==> N_TRAIN
    N_ABSORBED -. "Platform Commoditization Pressure" .-> N_ISV_PRODUCT
    N_INSURER == "$ Policy Premiums & Underwriting" ==> N_ENTERPRISE
    N_OBSERVE -->|"Real-time Cost & Token Telemetry"| N_ENTERPRISE
    N_REGULATOR == "Statutory Compliance & Fines (Art. 71)" ==> N_ENTERPRISE
    N_REGULATOR == "GPAI Codes of Practice & Transparency (Art. 53)" ==> N_FRONTIER
    N_AUDITOR == "Conformity Audits (ISO 42001 / High Risk)" ==> N_ENTERPRISE
    N_FRONTIER -. "Disclaims Liability (ToS 'AS-IS')" .-> N_ENTERPRISE
    N_ENTERPRISE -. "Vicarious Liability for Agent Harm (Respondeat Superior)" .-> N_AFFECTED_PARTY
    N_AFFECTED_PARTY -->|"Complaints & Redress Demands"| N_REGULATOR
    N_ENTERPRISE == "Delegates Authority & Safety Boundaries" ==> N_HARNESS
    N_HUMAN_USER == "Art. 14 Human Oversight & Stop Button" ==> N_HARNESS
    N_HARNESS -. "Cryptographic Tamper-Proof Audit Trail" .-> N_AUDIT_STORE
    N_AUDIT_STORE -->|"Forensic Evidence for Compliance Verification"| N_AUDITOR
    N_HARNESS -. "Enforces Least-Privilege Scopes" .-> N_MCP_HOST
    N_TARGET_SYS -. "Direct Impact & Real-World Blast Radius" .-> N_AFFECTED_PARTY
    N_HUMAN_USER -->|"Prompt Intent & Working Context"| N_ISV_PRODUCT
    N_IDP -->|"Issues Scoped Delegation Token"| N_HARNESS
    N_ISV_PRODUCT -->|"Initiates Autonomous Loop"| N_HARNESS
    N_HARNESS -->|"Inference API (Tokens & Directives)"| N_FRONTIER
    N_HARNESS -->|"Context Retrieval (RAG) & Checkpointing"| N_AUDIT_STORE
    N_HARNESS -->|"Traces & LLM Evaluation Metrics"| N_OBSERVE
    N_HARNESS -->|"JSON-RPC / MCP Tool Discovery & Invocations"| N_MCP_HOST
    N_MCP_HOST -->|"Authenticated Read/Write Operations"| N_TARGET_SYS
```

</TabItem>
</Tabs>

## Canonical Element Dictionary

| Element | Cluster | Domains | Properties |
| :--- | :--- | :--- | :--- |
| **Market Surveillance Authorities**<br/><small>EU AI Office, FTC, DPAs, Courts</small><br/>`N_REGULATOR` | 0. Jurisdictional & Regulatory Sphere | governance | **enforcement_powers**: Fines up to 7% turnover, injunctions |
| **Conformity Body & ISO Auditor**<br/><small>Notified Bodies, ISO/IEC 42001 Certifiers</small><br/>`N_AUDITOR` | 0. Jurisdictional & Regulatory Sphere | governance | **role**: AIMS certification & post-market monitoring |
| **AI Risk Underwriter & Insurer**<br/><small>Cyber & Algorithmic Liability Carrier</small><br/>`N_INSURER` | 0. Jurisdictional & Regulatory Sphere | economic, governance | **underwriting_gate**: Requires verifiable audit trail & human oversight |
| **Training Supply Chain**<br/><small>Data Curators, Annotators, Compute Clusters</small><br/>`N_TRAIN` | 1. Upstream Foundation & Model Lab | economic, technical | **cost_type**: Fixed / Heavy R&D CapEx<br/>**ip_risk**: Copyright / Scraping litigation |
| **Frontier GPAI Lab**<br/><small>Weights & Wholesale Inference APIs</small><br/>`N_FRONTIER` | 1. Upstream Foundation & Model Lab | economic, technical, governance | **eu_ai_act_role**: Provider_GPAI<br/>**pricing_model**: Per-Token Usage<br/>**liability_posture**: Disclaimed via ToS ('AS-IS') |
| **Platform Absorption Zone**<br/><small>Native Tools, Prompt Cache, Hosted Agent State</small><br/>`N_ABSORBED` | 1. Upstream Foundation & Model Lab | economic, technical | **market_effect**: Feature commoditization of wrapper ISVs |
| **Specialized AI Application**<br/><small>Vertical Solutions (Legal, Medical, Finance, Ops)</small><br/>`N_ISV_PRODUCT` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | economic, technical | **eu_ai_act_role**: Provider_System<br/>**pricing_model**: SaaS Seat / Value Outcome |
| **Agent Governance Harness**<br/><small>Deterministic Policy Engine & Guardrails</small><br/>`N_HARNESS` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | technical, governance | **iso_42001_role**: AIMS Technical Control Implementation<br/>**duty_of_care**: Caps blast radius, halts unsafe prompts/actions |
| **Sovereign Audit Ledger**<br/><small>Tamper-Evident WORM State & Forensic Store</small><br/>`N_AUDIT_STORE` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | technical, governance | **compliance**: Art. 12 Mandatory Logging / Rebuttal of Fault<br/>**sovereignty**: Client / Enterprise Owned |
| **Observability & Evals Engine**<br/><small>Continuous Evaluation, Traces & Cost Telemetry</small><br/>`N_OBSERVE` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | technical, governance, economic | **capabilities**: LLM-as-a-judge, OTEL tracing, token cost tracking |
| **Enterprise Deployer**<br/><small>Legal Principal & Economic Sponsor</small><br/>`N_ENTERPRISE` | 3. Enterprise Deployer & Principal Domain | economic, governance | **eu_ai_act_role**: Deployer<br/>**liability_posture**: Holds Vicarious & Strict Liability |
| **Enterprise Identity & Auth (IdP)**<br/><small>OAuth, OIDC, Workload IAM & Ephemeral Tokens</small><br/>`N_IDP` | 3. Enterprise Deployer & Principal Domain | technical, governance | **security_role**: Issues scoped actor delegations to agents |
| **Human Task Delegator & Overseer**<br/><small>End User / Mandatory HITL Supervisor</small><br/>`N_HUMAN_USER` | 3. Enterprise Deployer & Principal Domain | technical, governance | **control_mode**: Prompting, Art. 14 Human Oversight, Override |
| **Protocol Gateway (MCP Host)**<br/><small>Standardized Tool Broker & Context Provider</small><br/>`N_MCP_HOST` | 4. Target Execution Environment & Blast Radius | technical, governance | **protocol_standard**: Model Context Protocol (MCP)<br/>**isolation**: Dynamic capability & permission negotiation |
| **Target Systems & Operational APIs**<br/><small>Databases, Production ERP, Financial Rails</small><br/>`N_TARGET_SYS` | 4. Target Execution Environment & Blast Radius | technical, governance | **risk_zone**: Direct Causation Blast Radius |
| **Impacted Third Party**<br/><small>Consumers, Employees, Citizens</small><br/>`N_AFFECTED_PARTY` | 4. Target Execution Environment & Blast Radius | governance | **eu_ai_act_role**: Affected_Subject<br/>**legal_standing**: Private right of action, tort claimant |