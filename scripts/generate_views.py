import yaml
from pathlib import Path
from generate_docs import build_view_mermaid

def generate_view_pages():
    model_file = Path("model/ai_ecosystem.yaml")
    if not model_file.exists():
        print(f"Error: {model_file} not found.")
        return

    with open(model_file, "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    docs_path = Path("docs/ecosystem")
    docs_path.mkdir(parents=True, exist_ok=True)

    clusters_map = {c["id"]: c["label"] for c in model.get("clusters", [])}
    nodes_map = {n["id"]: n for n in model["nodes"]}

    for idx, v in enumerate(model.get("views", []), start=2):
        vid = v["id"]
        vtitle = v["title"]
        vdomains = set(v["domains"])
        vdesc = v.get("description", "Architectural projection of the ecosystem.")
        
        # Filter nodes & edges for this specific view
        active_nodes = [n for n in model["nodes"] if any(d in vdomains for d in n.get("domains", []))]
        active_node_ids = {n["id"] for n in active_nodes}
        active_edges = [
            e for e in model["edges"]
            if any(d in vdomains for d in e.get("domains", [])) 
            and e["from"] in active_node_ids 
            and e["to"] in active_node_ids
        ]

        chart = build_view_mermaid(model, v)

        md = [
            "---",
            f"title: \"{vtitle}\"",
            f"sidebar_position: {idx}",
            "---",
            "",
            f"# {vtitle}",
            "",
            f"> {vdesc}",
            "",
            "## Architecture Diagram",
            "",
            "```mermaid",
            chart,
            "```",
            "",
            "## Active Elements in this Lens",
            "",
            "| Element | Cluster | Operational Role & Properties |",
            "| :--- | :--- | :--- |"
        ]

        for n in active_nodes:
            props = "<br/>".join([f"**{k}**: {val}" for k, val in n.get("properties", {}).items()])
            cname = clusters_map.get(n.get("cluster", ""), "")
            sub = f"<br/><small>{n['sublabel']}</small>" if n.get("sublabel") else ""
            md.append(f"| **{n['label']}**{sub}<br/>`{n['id']}` | {cname} | {props} |")

        md.append("")
        md.append("## Active Relationships & Protocols")
        md.append("")
        md.append("| Source | Relationship / Protocol | Target | Type |")
        md.append("| :--- | :---: | :--- | :--- |")
        for e in active_edges:
            src = nodes_map.get(e["from"], {}).get("label", e["from"])
            dst = nodes_map.get(e["to"], {}).get("label", e["to"])
            md.append(f"| **{src}** | {e.get('label', '')} | **{dst}** | `{e.get('type', 'flow')}` |")

        page_file = docs_path / f"{vid}.md"
        page_file.write_text("\n".join(md), encoding="utf-8")
        print(f"✔ Individual lens page created: {page_file}")

if __name__ == "__main__":
    generate_view_pages()