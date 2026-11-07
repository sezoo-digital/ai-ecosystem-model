import sys
import yaml
import html
from pathlib import Path

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_drawio_style(shape, domains):
    if "governance" in domains:
        fill, stroke = "#FFF1F0", "#F5222D"
    elif "economic" in domains:
        fill, stroke = "#F6FFED", "#52C41A"
    elif "technical" in domains:
        fill, stroke = "#E6F7FF", "#1890FF"
    else:
        fill, stroke = "#F8FAFC", "#64748B"

    if shape == "cylinder":
        base = "shape=cylinder;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;"
    elif shape == "hexagon":
        base = "shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;"
    elif shape == "circle":
        base = "ellipse;whiteSpace=wrap;html=1;"
    elif shape == "stadium":
        base = "rounded=1;whiteSpace=wrap;html=1;arcSize=50;"
    elif shape == "subproc":
        base = "shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;"
    elif shape == "rounded":
        base = "rounded=1;whiteSpace=wrap;html=1;arcSize=15;"
    else:
        base = "rounded=0;whiteSpace=wrap;html=1;"

    return f"{base}fillColor={fill};strokeColor={stroke};strokeWidth=2;fontColor=#0F172A;"

def get_edge_style(etype):
    if etype == "money":
        return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#16A34A;strokeWidth=3;html=1;"
    elif etype == "authority":
        return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#722ED1;strokeWidth=3;html=1;"
    elif etype in ["tension", "disclaim"]:
        return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#DC2626;strokeWidth=2;dashed=1;html=1;"
    elif etype == "governance_control":
        return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#E11D48;strokeWidth=2;dashed=1;html=1;"
    elif etype == "protocol":
        return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#2563EB;strokeWidth=2;html=1;"
    return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#64748B;strokeWidth=1.5;html=1;"

def render_diagram_page(page_id, page_name, clusters, nodes, edges):
    xml = [
        f'  <diagram id="{page_id}" name="{html.escape(page_name, quote=True)}">',
        '    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169">',
        '      <root>',
        '        <mxCell id="0"/>',
        '        <mxCell id="1" parent="0"/>'
    ]

    # Group nodes by cluster
    nodes_by_cluster = {}
    for n in nodes.values():
        cid = n.get("cluster", "cluster_default")
        nodes_by_cluster.setdefault(cid, []).append(n)

    cluster_map = {c["id"]: c.get("label", c["id"]) for c in clusters}

    # Render Visual Cluster Containers (Swimlanes)
    cluster_x = 40
    for cid, cnodes in nodes_by_cluster.items():
        clabel = html.escape(cluster_map.get(cid, cid), quote=True)
        container_width = 280
        container_height = 80 + (len(cnodes) * 110)

        # Container Swimlane cell
        container_style = "swimlane;startSize=30;rounded=1;arcSize=8;fillColor=#F8FAFC;strokeColor=#CBD5E1;strokeWidth=1.5;fontStyle=1;fontSize=12;fontColor=#334155;"
        xml.append(f'        <mxCell id="{page_id}_{cid}" value="{clabel}" style="{container_style}" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="{cluster_x}" y="40" width="{container_width}" height="{container_height}" as="geometry"/>')
        xml.append('        </mxCell>')

        # Render Nodes as children of this cluster container
        node_y = 50
        for n in cnodes:
            raw_label = f"<b>{n['label']}</b>"
            if n.get("sublabel"):
                raw_label += f"<br/><small>{n['sublabel']}</small>"

            lbl_escaped = html.escape(raw_label, quote=True)
            style = get_drawio_style(n.get("shape", "rect"), n.get("domains", []))
            domains_str = html.escape(", ".join(n.get("domains", [])), quote=True)
            cluster_str = html.escape(cid, quote=True)
            
            # Lossless property extraction
            props_attrs = " ".join([
                f'{html.escape(k, quote=True)}="{html.escape(str(v), quote=True)}"' 
                for k, v in n.get("properties", {}).items()
            ])

            xml.append(f'        <object id="{n["id"]}" label="{lbl_escaped}" domains="{domains_str}" cluster="{cluster_str}" shape="{n.get("shape", "rect")}" {props_attrs}>')
            xml.append(f'          <mxCell style="{style}" vertex="1" parent="{page_id}_{cid}">')
            xml.append(f'            <mxGeometry x="30" y="{node_y}" width="220" height="70" as="geometry"/>')
            xml.append('          </mxCell>')
            xml.append('        </object>')
            node_y += 105

        cluster_x += 320

    # Render Edges
    for i, e in enumerate(edges):
        elbl = html.escape(e.get("label", ""), quote=True)
        style = get_edge_style(e.get("type", "flow"))
        xml.append(f'        <mxCell id="{page_id}_edge_{i}" value="{elbl}" style="{style}" edge="1" source="{e["from"]}" target="{e["to"]}" parent="1">')
        xml.append('          <mxGeometry relative="1" as="geometry"/>')
        xml.append('        </mxCell>')

    xml.append('      </root>')
    xml.append('    </mxGraphModel>')
    xml.append('  </diagram>')
    return "\n".join(xml)

def main():
    model_file = PROJECT_ROOT / "model" / "ai_ecosystem.yaml"
    if not model_file.exists():
        sys.exit(f"[ERROR] Model file not found at: {model_file}")

    with open(model_file, "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    export_path = PROJECT_ROOT / "static" / "exports"
    export_path.mkdir(parents=True, exist_ok=True)
    target_file = export_path / "ai_ecosystem.drawio"

    clusters = model.get("clusters", [])
    xml = ['<mxfile host="app.diagrams.net">']

    # Page 1: Master Model
    all_nodes = {n["id"]: n for n in model["nodes"]}
    xml.append(render_diagram_page("master_view", "1. Master Model (All Elements)", clusters, all_nodes, model["edges"]))

    # View Pages
    for v in model.get("views", []):
        view_domains = set(v["domains"])
        filtered_nodes = {n["id"]: n for n in model["nodes"] if any(d in view_domains for d in n.get("domains", []))}
        filtered_edges = [
            e for e in model["edges"]
            if any(d in view_domains for d in e.get("domains", [])) 
            and e["from"] in filtered_nodes 
            and e["to"] in filtered_nodes
        ]
        xml.append(render_diagram_page(v["id"], v["title"], clusters, filtered_nodes, filtered_edges))

    xml.append('</mxfile>')
    target_file.write_text("\n".join(xml), encoding="utf-8")
    print(f"[OK] Draw.io file created with cluster containers: {target_file.name}")

if __name__ == "__main__":
    main()