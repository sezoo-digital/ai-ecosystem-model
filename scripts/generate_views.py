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

def generate_interactive_page(model, output_path):
    md = [
        "---",
        "title: Interactive Ecosystem Views",
        "sidebar_position: 1",
        "---",
        "",
        "# AI Ecosystem: Multi-Lens Model",
        "",
        "Select a lens below to view the ecosystem filtered by interest domain.",
        "",
        "import Tabs from '@theme/Tabs';",
        "import TabItem from '@theme/TabItem';",
        "",
        "<Tabs>",
    ]
    
    for v in model.get("views", []):
        chart = build_view_mermaid(model, v)
        md.append(f'<TabItem value="{v["id"]}" label="{v["title"]}">\n')
        md.append("```mermaid")
        md.append(chart)
        md.append("```\n")
        md.append("</TabItem>")
        
    md.append("</Tabs>\n")
    
    md.append("## Canonical Node Dictionary\n")
    md.append("| Node | Domains | Core Properties |")
    md.append("| :--- | :--- | :--- |")
    for n in model["nodes"]:
        props = "<br/>".join([f"**{k}**: {v}" for k, v in n.get("properties", {}).items()])
        domains = ", ".join(n.get("domains", []))
        md.append(f"| **{n['label']}**<br/>`{n['id']}` | {domains} | {props} |")
        
    Path(output_path).write_text("\n".join(md))

if __name__ == "__main__":
    with open("model/ai_ecosystem.yaml", "r") as f:
        model = yaml.safe_load(f)
    Path("docs/ecosystem").mkdir(parents=True, exist_ok=True)
    generate_interactive_page(model, "docs/ecosystem/index.md")