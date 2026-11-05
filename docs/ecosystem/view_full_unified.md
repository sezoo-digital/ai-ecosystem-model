---
title: "Unified Ecosystem Model"
sidebar_position: 5
---

# Unified Ecosystem Model

> The complete property graph combining economic flows, technical loops, and governance gates.

## Architecture Diagram

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

## Active Elements in this Lens

| Element | Cluster | Operational Role & Properties |
| :--- | :--- | :--- |
| **Market Surveillance Authorities**<br/><small>EU AI Office, FTC, DPAs, Courts</small><br/>`N_REGULATOR` | 0. Jurisdictional & Regulatory Sphere | **enforcement_powers**: Fines up to 7% turnover, injunctions |
| **Conformity Body & ISO Auditor**<br/><small>Notified Bodies, ISO/IEC 42001 Certifiers</small><br/>`N_AUDITOR` | 0. Jurisdictional & Regulatory Sphere | **role**: AIMS certification & post-market monitoring |
| **AI Risk Underwriter & Insurer**<br/><small>Cyber & Algorithmic Liability Carrier</small><br/>`N_INSURER` | 0. Jurisdictional & Regulatory Sphere | **underwriting_gate**: Requires verifiable audit trail & human oversight |
| **Training Supply Chain**<br/><small>Data Curators, Annotators, Compute Clusters</small><br/>`N_TRAIN` | 1. Upstream Foundation & Model Lab | **cost_type**: Fixed / Heavy R&D CapEx<br/>**ip_risk**: Copyright / Scraping litigation |
| **Frontier GPAI Lab**<br/><small>Weights & Wholesale Inference APIs</small><br/>`N_FRONTIER` | 1. Upstream Foundation & Model Lab | **eu_ai_act_role**: Provider_GPAI<br/>**pricing_model**: Per-Token Usage<br/>**liability_posture**: Disclaimed via ToS ('AS-IS') |
| **Platform Absorption Zone**<br/><small>Native Tools, Prompt Cache, Hosted Agent State</small><br/>`N_ABSORBED` | 1. Upstream Foundation & Model Lab | **market_effect**: Feature commoditization of wrapper ISVs |
| **Specialized AI Application**<br/><small>Vertical Solutions (Legal, Medical, Finance, Ops)</small><br/>`N_ISV_PRODUCT` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | **eu_ai_act_role**: Provider_System<br/>**pricing_model**: SaaS Seat / Value Outcome |
| **Agent Governance Harness**<br/><small>Deterministic Policy Engine & Guardrails</small><br/>`N_HARNESS` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | **iso_42001_role**: AIMS Technical Control Implementation<br/>**duty_of_care**: Caps blast radius, halts unsafe prompts/actions |
| **Sovereign Audit Ledger**<br/><small>Tamper-Evident WORM State & Forensic Store</small><br/>`N_AUDIT_STORE` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | **compliance**: Art. 12 Mandatory Logging / Rebuttal of Fault<br/>**sovereignty**: Client / Enterprise Owned |
| **Observability & Evals Engine**<br/><small>Continuous Evaluation, Traces & Cost Telemetry</small><br/>`N_OBSERVE` | 2. Specialized Product & Harness Domain (ISV / Custom Runtime) | **capabilities**: LLM-as-a-judge, OTEL tracing, token cost tracking |
| **Enterprise Deployer**<br/><small>Legal Principal & Economic Sponsor</small><br/>`N_ENTERPRISE` | 3. Enterprise Deployer & Principal Domain | **eu_ai_act_role**: Deployer<br/>**liability_posture**: Holds Vicarious & Strict Liability |
| **Enterprise Identity & Auth (IdP)**<br/><small>OAuth, OIDC, Workload IAM & Ephemeral Tokens</small><br/>`N_IDP` | 3. Enterprise Deployer & Principal Domain | **security_role**: Issues scoped actor delegations to agents |
| **Human Task Delegator & Overseer**<br/><small>End User / Mandatory HITL Supervisor</small><br/>`N_HUMAN_USER` | 3. Enterprise Deployer & Principal Domain | **control_mode**: Prompting, Art. 14 Human Oversight, Override |
| **Protocol Gateway (MCP Host)**<br/><small>Standardized Tool Broker & Context Provider</small><br/>`N_MCP_HOST` | 4. Target Execution Environment & Blast Radius | **protocol_standard**: Model Context Protocol (MCP)<br/>**isolation**: Dynamic capability & permission negotiation |
| **Target Systems & Operational APIs**<br/><small>Databases, Production ERP, Financial Rails</small><br/>`N_TARGET_SYS` | 4. Target Execution Environment & Blast Radius | **risk_zone**: Direct Causation Blast Radius |
| **Impacted Third Party**<br/><small>Consumers, Employees, Citizens</small><br/>`N_AFFECTED_PARTY` | 4. Target Execution Environment & Blast Radius | **eu_ai_act_role**: Affected_Subject<br/>**legal_standing**: Private right of action, tort claimant |

## Active Relationships & Protocols

| Source | Relationship / Protocol | Target | Type |
| :--- | :---: | :--- | :--- |
| **Enterprise Deployer** | $$$ SaaS Subscription / Outcome Fee | **Specialized AI Application** | `money` |
| **Specialized AI Application** | $$ Token Consumption Cost | **Frontier GPAI Lab** | `money` |
| **Frontier GPAI Lab** | $ Compute & Data CapEx | **Training Supply Chain** | `money` |
| **Platform Absorption Zone** | Platform Commoditization Pressure | **Specialized AI Application** | `tension` |
| **AI Risk Underwriter & Insurer** | $ Policy Premiums & Underwriting | **Enterprise Deployer** | `money` |
| **Observability & Evals Engine** | Real-time Cost & Token Telemetry | **Enterprise Deployer** | `flow` |
| **Market Surveillance Authorities** | Statutory Compliance & Fines (Art. 71) | **Enterprise Deployer** | `authority` |
| **Market Surveillance Authorities** | GPAI Codes of Practice & Transparency (Art. 53) | **Frontier GPAI Lab** | `authority` |
| **Conformity Body & ISO Auditor** | Conformity Audits (ISO 42001 / High Risk) | **Enterprise Deployer** | `authority` |
| **Frontier GPAI Lab** | Disclaims Liability (ToS 'AS-IS') | **Enterprise Deployer** | `disclaim` |
| **Enterprise Deployer** | Vicarious Liability for Agent Harm (Respondeat Superior) | **Impacted Third Party** | `tension` |
| **Impacted Third Party** | Complaints & Redress Demands | **Market Surveillance Authorities** | `flow` |
| **Enterprise Deployer** | Delegates Authority & Safety Boundaries | **Agent Governance Harness** | `authority` |
| **Human Task Delegator & Overseer** | Art. 14 Human Oversight & Stop Button | **Agent Governance Harness** | `authority` |
| **Agent Governance Harness** | Cryptographic Tamper-Proof Audit Trail | **Sovereign Audit Ledger** | `governance_control` |
| **Sovereign Audit Ledger** | Forensic Evidence for Compliance Verification | **Conformity Body & ISO Auditor** | `flow` |
| **Agent Governance Harness** | Enforces Least-Privilege Scopes | **Protocol Gateway (MCP Host)** | `governance_control` |
| **Target Systems & Operational APIs** | Direct Impact & Real-World Blast Radius | **Impacted Third Party** | `tension` |
| **Human Task Delegator & Overseer** | Prompt Intent & Working Context | **Specialized AI Application** | `flow` |
| **Enterprise Identity & Auth (IdP)** | Issues Scoped Delegation Token | **Agent Governance Harness** | `protocol` |
| **Specialized AI Application** | Initiates Autonomous Loop | **Agent Governance Harness** | `flow` |
| **Agent Governance Harness** | Inference API (Tokens & Directives) | **Frontier GPAI Lab** | `protocol` |
| **Agent Governance Harness** | Context Retrieval (RAG) & Checkpointing | **Sovereign Audit Ledger** | `flow` |
| **Agent Governance Harness** | Traces & LLM Evaluation Metrics | **Observability & Evals Engine** | `flow` |
| **Agent Governance Harness** | JSON-RPC / MCP Tool Discovery & Invocations | **Protocol Gateway (MCP Host)** | `protocol` |
| **Protocol Gateway (MCP Host)** | Authenticated Read/Write Operations | **Target Systems & Operational APIs** | `flow` |