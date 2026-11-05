---
title: "Engineering & Technical Runtime Perspective"
sidebar_position: 4
---

# Engineering & Technical Runtime Perspective

> The agentic execution loop: IdP delegation, inference protocols, MCP gateways, and state stores.

## Architecture Diagram

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

## Active Elements in this Lens

| Element | Cluster | Operational Role & Properties |
| :--- | :--- | :--- |
| **Training Supply Chain**<br/><small>Data Curators, Annotators, Compute Clusters</small><br/>`N_TRAIN` | 1. Upstream Foundation & Model Lab | **cost_type**: Fixed / Heavy R&D CapEx<br/>**ip_risk**: Copyright / Scraping litigation |
| **Frontier GPAI Lab**<br/><small>Weights & Wholesale Inference APIs</small><br/>`N_FRONTIER` | 1. Upstream Foundation & Model Lab | **eu_ai_act_role**: Provider_GPAI<br/>**pricing_model**: Per-Token Usage<br/>**liability_posture**: Disclaimed via ToS ('AS-IS') |
| **Platform Absorption Zone**<br/><small>Native Tools, Prompt Cache, Hosted Agent State</small><br/>`N_ABSORBED` | 1. Upstream Foundation & Model Lab | **market_effect**: Feature commoditization of wrapper ISVs |
| **Specialized AI Application**<br/><small>Vertical Solutions (Legal, Medical, Finance, Ops)</small><br/>`N_ISV_PRODUCT` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | **eu_ai_act_role**: Provider_System<br/>**pricing_model**: SaaS Seat / Value Outcome |
| **Agent Governance Harness**<br/><small>Deterministic Policy Engine & Guardrails</small><br/>`N_HARNESS` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | **iso_42001_role**: AIMS Technical Control Implementation<br/>**duty_of_care**: Caps blast radius, halts unsafe prompts/actions |
| **Sovereign Audit Ledger**<br/><small>Tamper-Evident WORM State & Forensic Store</small><br/>`N_AUDIT_STORE` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | **compliance**: Art. 12 Mandatory Logging / Rebuttal of Fault<br/>**sovereignty**: Client / Enterprise Owned |
| **Observability & Evals Engine**<br/><small>Continuous Evaluation, Traces & Cost Telemetry</small><br/>`N_OBSERVE` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | **capabilities**: LLM-as-a-judge, OTEL tracing, token cost tracking |
| **Enterprise Identity & Auth (IdP)**<br/><small>OAuth, OIDC, Workload IAM & Ephemeral Tokens</small><br/>`N_IDP` | 3. Enterprise Deployer & Principal Domain | **security_role**: Issues scoped actor delegations to agents |
| **Human Task Delegator & Overseer**<br/><small>End User / Mandatory HITL Supervisor</small><br/>`N_HUMAN_USER` | 3. Enterprise Deployer & Principal Domain | **control_mode**: Prompting, Art. 14 Human Oversight, Override |
| **Protocol Gateway (MCP Host)**<br/><small>Standardized Tool Broker & Context Provider</small><br/>`N_MCP_HOST` | 4. Target Execution Environment & Blast Radius | **protocol_standard**: Model Context Protocol (MCP)<br/>**isolation**: Dynamic capability & permission negotiation |
| **Target Systems & Operational APIs**<br/><small>Databases, Production ERP, Financial Rails</small><br/>`N_TARGET_SYS` | 4. Target Execution Environment & Blast Radius | **risk_zone**: Direct Causation Blast Radius |

## Active Relationships & Protocols

| Source | Relationship / Protocol | Target | Type |
| :--- | :---: | :--- | :--- |
| **Agent Governance Harness** | Cryptographic Tamper-Proof Audit Trail | **Sovereign Audit Ledger** | `governance_control` |
| **Agent Governance Harness** | Enforces Least-Privilege Scopes | **Protocol Gateway (MCP Host)** | `governance_control` |
| **Human Task Delegator & Overseer** | Prompt Intent & Working Context | **Specialized AI Application** | `flow` |
| **Enterprise Identity & Auth (IdP)** | Issues Scoped Delegation Token | **Agent Governance Harness** | `protocol` |
| **Specialized AI Application** | Initiates Autonomous Loop | **Agent Governance Harness** | `flow` |
| **Agent Governance Harness** | Inference API (Tokens & Directives) | **Frontier GPAI Lab** | `protocol` |
| **Agent Governance Harness** | Context Retrieval (RAG) & Checkpointing | **Sovereign Audit Ledger** | `flow` |
| **Agent Governance Harness** | Traces & LLM Evaluation Metrics | **Observability & Evals Engine** | `flow` |
| **Agent Governance Harness** | JSON-RPC / MCP Tool Discovery & Invocations | **Protocol Gateway (MCP Host)** | `protocol` |
| **Protocol Gateway (MCP Host)** | Authenticated Read/Write Operations | **Target Systems & Operational APIs** | `flow` |