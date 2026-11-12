#!/usr/bin/env python3
"""
Generates the canonical docs/index.md page.
1. Reads editorial introduction from templates/model_introduction.md
2. Dynamically generates & appends:
   - Export download callouts
   - Architectural visual key (Mermaid & table)
   - Complete unified Mermaid ecosystem diagram
   - Canonical element data dictionary
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

def format_node_shape(node_id, label, sublabel, shape):
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
    etype = e.get("type", "flow")
    label = e.get("label", "").replace('"', "'")
    if etype in ["money", "authority"]: return f'== "{label}" ==>'
    elif etype in ["tension", "disclaim", "governance_control"]: return f'-. "{label}" .->'
    return f'-->|"{label}"|'

def get_node_class(node):
    domains = node.get("domains", [])
    if "governance" in domains: return "gov"
    if "economic" in domains: return "econ"
    if "technical" in domains: return "tech"
    return "default"

def build_visual_key_mermaid(styles_def):
    shapes = styles_def.get("shapes", {})
    if not shapes: return ""
    lines = [
        "flowchart LR",
        "    classDef gov fill:#FFF1F0,stroke:#F5222D,stroke-width:2px;",
        "    classDef econ fill:#F6FFED,stroke:#52C41A,stroke-width:2px;",
        "    classDef tech fill:#E6F7FF,stroke:#1890FF,stroke-width:2px;",
        "    classDef default fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px;",
        "",
        '    subgraph LegendShapes ["Architectural Node Archetypes"]'
    ]
    sample_classes = {
        "hexagon": "gov", "circle": "gov", "subproc": "tech",
        "cylinder": "tech", "stadium": "tech", "rounded": "tech", "rect": "econ"
    }
    for shape_name, info in shapes.items():
        node_id = f"K_{shape_name.upper()}"
        lbl = info.get("label", shape_name)
        rendered = format_node_shape(node_id, lbl, f"shape: {shape_name}", shape_name)
        cls = sample_classes.get(shape_name, "default")
        lines.append(f"        {rendered}:::{cls}")
    lines.append("    end")
    return "\n".join(lines)

def build_notation_table(styles_def):
    shapes = styles_def.get("shapes", {})
    edge_types = styles_def.get("edge_types", {})
    md = []
    if shapes:
        md.append("### Node Archetypes (Shapes)\n")
        md.append("| Shape | Archetype / Meaning | Description |")
        md.append("| :---: | :--- | :--- |")
        for s_name, s_info in shapes.items():
            md.append(f"| `{s_name}` | **{s_info.get('label', '')}** | {s_info.get('description', '')} |")
    if edge_types:
        md.append("\n### Relationship & Edge Types\n")
        md.append("| Line Style | Relationship Type | Semantic Meaning |")
        md.append("| :---: | :--- | :--- |")
        for e_type, e_info in edge_types.items():
            md.append(f"| `{e_info.get('syntax', '')}` | **{e_info.get('label', '')}** (`{e_type}`) | {e_info.get('description', '')} |")
    md.append("\n### Domain Boundary Colors\n")
    md.append("| Color | Domain | Scope |")
    md.append("| :---: | :--- | :--- |")
    md.append("| 🔴 **Red / Pink** | `governance` | Statutory duties, liability allocation, compliance controls, human oversight. |")
    md.append("| 🟢 **Green** | `economic` | SaaS contracts, token consumption costs, GPU CapEx, underwriting fees. |")
    md.append("| 🔵 **Blue** | `technical` | API execution protocols, JSON-RPC (MCP), state persistence, telemetry. |")
    return "\n".join(md)

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
            shape_code = format_node_shape(n["id"], n["label"], n.get("sublabel", ""), n.get("shape", "rect"))
            lines.append(f'        {shape_code}:::{get_node_class(n)}')
        lines.append("    end\n")
        
    for e in model["edges"]:
        lines.append(f'    {e["from"]} {edge_to_mermaid(e)} {e["to"]}')
        
    return "\n".join(lines)

def main():
    if not MODEL_FILE.exists():
        sys.exit(f"[ERROR] Model file not found at: {MODEL_FILE}")

    with open(MODEL_FILE, "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    # 1. Read Intro Markdown Content
    if INTRO_TEMPLATE.exists():
        intro_content = INTRO_TEMPLATE.read_text(encoding="utf-8").strip()
    else:
        # Fallback if the file does not exist yet
        intro_content = (
            "# Canonical AI Ecosystem Model\n\n"
            "A logical property graph integrating cognitive agent state (CoALA), "
            "cybernetic control (Beer's VSM), macro-economics, and regulatory liability."
        )

    # 2. Build Dynamic Elements
    styles_def = model.get("styles") or {}
    key_chart = build_visual_key_mermaid(styles_def)
    key_tables = build_notation_table(styles_def)
    full_mermaid = build_full_unified_mermaid(model)

    # 3. Assemble Final Document
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
    ]

    if key_chart:
        md.extend([
            "```mermaid",
            key_chart,
            "```",
            ""
        ])

    md.extend([
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
        "| Element | Cluster | Domains | Properties |",
        "| :--- | :--- | :--- | :--- |",
    ])

    clusters_map = {c["id"]: c["label"] for c in model.get("clusters", [])}
    for n in model["nodes"]:
        props = "<br/>".join([f"**{k}**: {v}" for k, v in n.get("properties", {}).items()])
        domains = ", ".join(n.get("domains", []))
        cluster_name = clusters_map.get(n.get("cluster", ""), n.get("cluster", ""))
        sub = f"<br/><small>{n['sublabel']}</small>" if n.get("sublabel") else ""
        md.append(f"| **{n['label']}**{sub}<br/>`{n['id']}` | {cluster_name} | {domains} | {props} |")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(md), encoding="utf-8")
    print(f"[OK] Master documentation generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()