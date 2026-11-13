#!/usr/bin/env python3
"""
Generates the canonical docs/index.md page.
Decouples presentation styles from ontology:
- Maps NodeKindEnum to Mermaid shapes
- Maps RelationKindEnum (including algedonic_signal) to Mermaid edge styles
- Computes Ashby variety spans from log10 cardinality values
"""

import sys
import yaml
import html
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INTRO_TEMPLATE = PROJECT_ROOT / "templates" / "model_introduction.md"
MODEL_FILE = PROJECT_ROOT / "model" / "ai_ecosystem.yaml"
OUTPUT_FILE = PROJECT_ROOT / "docs" / "index.md"

KIND_TO_SHAPE = {
    "StatutoryAuthority": "hexagon",
    "NaturalPerson":      "circle",
    "DeterministicGate":  "subproc",
    "StateStore":         "cylinder",
    "SecurityAuthority":  "stadium",
    "SoftwareService":    "rounded",
    "EconomicEntity":     "rect",
}

def format_node_shape(node_id, label, sublabel, kind):
    shape = KIND_TO_SHAPE.get(kind, "rect")
    sub = f"<br/><small><i>{html.escape(sublabel)}</i></small>" if sublabel else ""
    content = f'"{html.escape(label)}{sub}"'
    
    if shape == "hexagon": return f"{node_id}{{{{{content}}}}}"
    elif shape == "cylinder": return f"{node_id}[({content})]"
    elif shape == "subproc": return f"{node_id}[[{content}]]"
    elif shape == "stadium": return f"{node_id}([{content}])"
    elif shape == "circle": return f"{node_id}(({content}))"
    elif shape == "rounded": return f"{node_id}({content})"
    return f"{node_id}[{content}]"

def edge_to_mermaid(e):
    rkind = e.get("relation_kind", "data_flow")
    label = e.get("label", "").replace('"', "'")
    if rkind == "algedonic_signal":
        return f'== "🚨 {label}" ==>'
    elif rkind in ["commercial_flow", "statutory_mandate"]:
        return f'== "{label}" ==>'
    elif rkind in ["liability_exposure", "contractual_term", "governance_control"]:
        return f'-. "{label}" .->'
    return f'-->|"{label}"|'

def get_node_class(node):
    domains = node.get("domains", [])
    if "governance" in domains: return "gov"
    if "economic" in domains: return "econ"
    if "technical" in domains: return "tech"
    return "default"

def build_visual_key_mermaid():
    lines = [
        "flowchart LR",
        "    classDef gov fill:#FFF1F0,stroke:#F5222D,stroke-width:2px;",
        "    classDef econ fill:#F6FFED,stroke:#52C41A,stroke-width:2px;",
        "    classDef tech fill:#E6F7FF,stroke:#1890FF,stroke-width:2px;",
        "    classDef default fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px;",
        "",
        '    subgraph LegendShapes ["Architectural Node Archetypes"]'
    ]
    key_samples = [
        ("K_HEX", "Statutory Authority", "StatutoryAuthority", "gov"),
        ("K_CIR", "Natural Person", "NaturalPerson", "gov"),
        ("K_SUB", "Deterministic Gate", "DeterministicGate", "tech"),
        ("K_CYL", "State Store", "StateStore", "tech"),
        ("K_STA", "Security Authority", "SecurityAuthority", "tech"),
        ("K_RND", "Software Service", "SoftwareService", "tech"),
        ("K_REC", "Economic Entity", "EconomicEntity", "econ"),
    ]
    for nid, lbl, kind, cls in key_samples:
        rendered = format_node_shape(nid, lbl, f"kind: {kind}", kind)
        lines.append(f"        {rendered}:::{cls}")
    lines.append("    end")
    return "\n".join(lines)

def build_notation_table():
    return """### Node Archetypes (Kinds)

| Kind | Semantic Meaning | Visual Shape |
| :--- | :--- | :---: |
| `StatutoryAuthority` | Non-negotiable external legal authorities, courts, market surveillance | `hexagon` |
| `NaturalPerson` | Human delegators, mandatory Art. 14 supervisors, impacted third parties | `circle` |
| `DeterministicGate` | Sandboxes, policy harnesses, capability brokers bounding non-deterministic AI | `subproc` |
| `StateStore` | WORM audit ledgers, vector databases, operational enterprise ERPs | `cylinder` |
| `SecurityAuthority` | Enterprise IdP, OAuth token issuers, workload authorization brokers | `stadium` |
| `SoftwareService` | Foundation model endpoints, vertical applications, continuous eval engines | `rounded` |
| `EconomicEntity` | Commercial deployers, CapEx supply chain entities, venture capital funds | `rect` |

### Relationship & Edge Types

| Line Style | Semantic Relation Kind | Description |
| :---: | :--- | :--- |
| `== '🚨 label' ==>` | `algedonic_signal` | **VSM Emergency Tripwire:** Direct crisis bypass from S1 operations to S5 board/policy |
| `== 'label' ==>` | `commercial_flow` | Capital transactions, SaaS fees, token costs, insurance premiums |
| `== 'label' ==>` | `statutory_mandate` | Statutory orders, compliance mandates, mandatory oversight |
| `-. 'label' .->` | `governance_control` | Policy bounds, audit trail logging, S3* independent sampling probes |
| `-. 'label' .->` | `liability_exposure` | Tort liability, blast radius causation, platform margin pressure |
| `-. 'label' .->` | `contractual_term` | Contractual liability carve-outs, ToS 'AS-IS' disclaimers |
| `-->|'label'|` | `protocol_call` | Technical protocols (A2E, MIP, A2T via MCP, A2A) |
| `-->|'label'|` | `data_flow` | Telemetry traces, prompt context (RAG), evidence logs |

### Domain Boundary Colors

| Color | Domain | Scope |
| :---: | :--- | :--- |
| 🔴 **Red / Pink** | `governance` | Statutory duties, liability allocation, compliance controls, human oversight |
| 🟢 **Green** | `economic` | SaaS contracts, token consumption costs, GPU CapEx, underwriting fees |
| 🔵 **Blue** | `technical` | API execution protocols, JSON-RPC (MCP), state persistence, telemetry |"""

def build_full_unified_mermaid(model):
    lines = [
        "flowchart TB",
        "    classDef gov fill:#FFF1F0,stroke:#F5222D,stroke-width:2px;",
        "    classDef econ fill:#F6FFED,stroke:#52C41A,stroke-width:2px;",
        "    classDef tech fill:#E6F7FF,stroke:#1890FF,stroke-width:2px;",
        "    classDef default fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px;",
        ""
    ]
    clusters = {c["id"]: c for c in model.get("clusters", [])}
    nodes_by_cluster = {}
    for n in model["nodes"]:
        nodes_by_cluster.setdefault(n.get("cluster", "root"), []).append(n)
        
    for cid, nodes in nodes_by_cluster.items():
        clabel = clusters[cid]["label"] if cid in clusters else cid
        lines.append(f'    subgraph {cid} ["{clabel}"]')
        for n in nodes:
            shape_code = format_node_shape(n["id"], n["label"], n.get("sublabel", ""), n.get("kind", "EconomicEntity"))
            lines.append(f'        {shape_code}:::{get_node_class(n)}')
        lines.append("    end\n")
        
    for e in model["edges"]:
        lines.append(f'    {e["from"]} {edge_to_mermaid(e)} {e["to"]}')
        
    return "\n".join(lines)

def format_cardinality(n):
    c_min = n.get("cardinality_log10_min")
    c_max = n.get("cardinality_log10_max")
    unit = n.get("cardinality_unit", "")
    if c_min is not None and c_max is not None:
        if c_min == c_max:
            return f"10^{c_min:g} {unit}"
        return f"10^{c_min:g}–10^{c_max:g} {unit}"
    return n.get("properties", {}).get("cardinality", "—")

def main():
    if not MODEL_FILE.exists():
        sys.exit(f"[ERROR] Model file not found at: {MODEL_FILE}")

    with open(MODEL_FILE, "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    if INTRO_TEMPLATE.exists():
        intro_content = INTRO_TEMPLATE.read_text(encoding="utf-8").strip()
    else:
        intro_content = (
            "# Canonical AI Ecosystem Model\n\n"
            "A logical property graph integrating cognitive agent state (CoALA), "
            "cybernetic control (Beer's VSM), macro-economics, and regulatory liability."
        )

    key_chart = build_visual_key_mermaid()
    key_tables = build_notation_table()
    full_mermaid = build_full_unified_mermaid(model)

    md = [
        "---",
        "title: Canonical AI Ecosystem Model",
        "sidebar_position: 1",
        "slug: /",
        "---",
        "",
        "import useBaseUrl from '@docusaurus/useBaseUrl';",
        "",
        intro_content,
        "",
        ":::tip Download Canonical Models",
        "Download the raw model to query in external visual modeling tools:",
        "",
        '- <a href={useBaseUrl("/exports/ai_ecosystem.graphml")} download="ai_ecosystem.graphml">**Download for yEd** (.graphml)</a>',
        '- <a href={useBaseUrl("/exports/ai_ecosystem.drawio")} download="ai_ecosystem.drawio">**Download for draw.io** (.drawio)</a>',
        '- <a href={useBaseUrl("/exports/ai_ecosystem_kumu.json")} download="ai_ecosystem_kumu.json">**Download for Kumu Blueprint** (.json)</a>',
        ":::",
        "",
        "<details>",
        "<summary><strong>📖 Visual Language & Architectural Key (Click to expand)</strong></summary>",
        "",
        "```mermaid",
        key_chart,
        "```",
        "",
        key_tables,
        "",
        "</details>",
        "",
        "## Unified Ecosystem Architecture",
        "",
        "```mermaid",
        full_mermaid,
        "```",
        "",
        "## Canonical Element Dictionary",
        "",
        "| Element | Cluster | Kind | VSM Tier & Recursion | Ashby Variety (Cardinality) | EU AI Act Role |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    clusters_map = {c["id"]: c["label"] for c in model.get("clusters", [])}
    for n in model["nodes"]:
        cluster_name = clusters_map.get(n.get("cluster", ""), n.get("cluster", ""))
        sub = f"<br/><small>{n['sublabel']}</small>" if n.get("sublabel") else ""
        vsm_desc = f"`{n.get('vsm_system', '')}`<br/><small>{n.get('vsm_recursion_level', '')}</small>"
        cardinality_str = format_cardinality(n)
        md.append(f"| **{n['label']}**{sub}<br/>`{n['id']}` | {cluster_name} | `{n.get('kind', '')}` | {vsm_desc} | {cardinality_str} | `{n.get('eu_ai_act_role', '')}` |")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(md), encoding="utf-8")
    print(f"[OK] Master documentation generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()