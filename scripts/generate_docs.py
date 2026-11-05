import yaml
from pathlib import Path

def edge_to_mermaid(e):
    etype, label = e.get("type", "flow"), e.get("label", "")
    if etype == "money": return f'== "{label}" ==>'
    if etype in ["tension", "disclaim"]: return f'-. "{label}" .->'
    if etype == "authority": return f'== "{label}" ==>'
    return f'-->|"{label}"|'

def build_view_mermaid(model, view_def):
    view_domains = set(view_def["domains"])
    active_nodes = {n["id"]: n for n in model["nodes"] if any(d in view_domains for d in n["domains"])}
    active_edges = [
        e for e in model["edges"] 
        if any(d in view_domains for d in e["domains"]) and e["from"] in active_nodes and e["to"] in active_nodes
    ]
    
    lines = [f"flowchart {view_def.get('direction', 'TB')}"]
    clusters = {c["id"]: c for c in model.get("clusters", [])}
    nodes_by_cluster = {}
    for n in active_nodes.values():
        nodes_by_cluster.setdefault(n.get("cluster", "root"), []).append(n)
        
    for cid, nodes in nodes_by_cluster.items():
        if cid in clusters:
            lines.append(f'    subgraph {cid} ["{clusters[cid]["label"]}"]')
            for n in nodes:
                sub = f"<br/><small><i>{n['sublabel']}</i></small>" if n.get("sublabel") else ""
                lines.append(f'        {n["id"]}["<b>{n["label"]}</b>{sub}"]')
            lines.append("    end")
            
    lines.append("")
    for e in active_edges:
        lines.append(f'    {e["from"]} {edge_to_mermaid(e)} {e["to"]}')
        
    return "\n".join(lines)

def main():
    with open("model/ai_ecosystem.yaml", "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    docs_path = Path("docs/ecosystem")
    docs_path.mkdir(parents=True, exist_ok=True)

    md = [
        "---",
        "title: AI Ecosystem Multi-Lens Architecture",
        "sidebar_position: 1",
        "slug: /",
        "---",
        "",
        "# AI Ecosystem: Multi-Lens Architecture & Governance",
        "",
        "Select a lens below to explore the ecosystem. You can also download the raw models for visual editing in **yEd** or **draw.io**.",
        "",
        "import Tabs from '@theme/Tabs';",
        "import TabItem from '@theme/TabItem';",
        "",
        "<Tabs>",
    ]

    for v in model.get("views", []):
        vid = v["id"]
        chart = build_view_mermaid(model, v)
        md.append(f'<TabItem value="{vid}" label="{v["title"]}">\n')
        
        # FIX: Using 'pathname:///' bypasses Docusaurus page router and links directly to static assets
        md.append(f"> 📥 **Export to Graphical Tools:** ")
        md.append(f"> <a href=\"pathname:///ai-ecosystem-model/exports/{vid}.graphml\" download>Download for yEd (.graphml)</a> &nbsp;|&nbsp; ")
        md.append(f"> <a href=\"pathname:///ai-ecosystem-model/exports/{vid}.drawio\" download>Download for draw.io (.drawio)</a>\n")
        
        md.append("```mermaid")
        md.append(chart)
        md.append("```\n")
        md.append("</TabItem>")

    md.append("</Tabs>\n")

    md.append("## Canonical Element Dictionary\n")
    md.append("| Element | Domains | Properties |")
    md.append("| :--- | :--- | :--- |")
    for n in model["nodes"]:
        props = "<br/>".join([f"**{k}**: {v}" for k, v in n.get("properties", {}).items()])
        domains = ", ".join(n.get("domains", []))
        md.append(f"| **{n['label']}**<br/>`{n['id']}` | {domains} | {props} |")

    target = docs_path / "index.md"
    target.write_text("\n".join(md), encoding="utf-8")
    print(f"✔ Documentation page generated: {target}")

if __name__ == "__main__":
    main()