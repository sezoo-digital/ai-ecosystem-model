#!/usr/bin/env python3
"""
Draw.io Multi-Page XML Exporter for AI Ecosystem Model.
Outputs: static/exports/ai_ecosystem.drawio
Maps:
  - NodeKindEnum -> Native draw.io stencil shapes (including Standards & Foresight bodies)
  - RelationKindEnum -> Semantic line styles, widths & colors (including algedonic_signal)
  - Edge attributes -> Serializes power_asymmetry, switching_cost, polarity, and protocol_plane
  - Multi-page projections -> Master Model + Economic, Governance, and Technical lenses
"""

import sys
import yaml
import html
from pathlib import Path

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

KIND_TO_SHAPE = {
    "StatutoryAuthority":   "shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;",
    "StandardsConsortium":  "rounded=1;whiteSpace=wrap;html=1;arcSize=50;",
    "ForesightInstitute":   "shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;",
    "NaturalPerson":        "ellipse;whiteSpace=wrap;html=1;",
    "DeterministicGate":    "shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;",
    "StateStore":           "shape=cylinder;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;",
    "SecurityAuthority":    "rounded=1;whiteSpace=wrap;html=1;arcSize=50;",
    "SoftwareService":      "rounded=1;whiteSpace=wrap;html=1;arcSize=15;",
    "EconomicEntity":       "rounded=0;whiteSpace=wrap;html=1;",
}

def get_drawio_style(kind, domains):
    if "governance" in domains:
        fill, stroke = "#FFF1F0", "#F5222D"
    elif "economic" in domains:
        fill, stroke = "#F6FFED", "#52C41A"
    elif "technical" in domains:
        fill, stroke = "#E6F7FF", "#1890FF"
    else:
        fill, stroke = "#F8FAFC", "#64748B"

    base_shape = KIND_TO_SHAPE.get(kind, "rounded=0;whiteSpace=wrap;html=1;")
    return f"{base_shape}fillColor={fill};strokeColor={stroke};strokeWidth=2;fontColor=#0F172A;"

def get_edge_style(relation_kind):
    if relation_kind == "algedonic_signal":
        return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#B91C1C;strokeWidth=4;html=1;"
    elif relation_kind == "commercial_flow":
        return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#16A34A;strokeWidth=3;html=1;"
    elif relation_kind == "statutory_mandate":
        return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#722ED1;strokeWidth=3;html=1;"
    elif relation_kind in ["liability_exposure", "contractual_term"]:
        return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#DC2626;strokeWidth=2;dashed=1;html=1;"
    elif relation_kind == "governance_control":
        return "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#E11D48;strokeWidth=2;dashed=1;html=1;"
    elif relation_kind == "protocol_call":
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

    nodes_by_cluster = {}
    for n in nodes.values():
        cid = n.get("cluster", "cluster_default")
        nodes_by_cluster.setdefault(cid, []).append(n)

    cluster_map = {c["id"]: c.get("label", c["id"]) for c in clusters}

    cluster_x = 40
    for cid, cnodes in nodes_by_cluster.items():
        clabel = html.escape(cluster_map.get(cid, cid), quote=True)
        container_width = 280
        container_height = 80 + (len(cnodes) * 115)

        container_style = "swimlane;startSize=30;rounded=1;arcSize=8;fillColor=#F8FAFC;strokeColor=#CBD5E1;strokeWidth=1.5;fontStyle=1;fontSize=12;fontColor=#334155;"
        xml.append(f'        <mxCell id="{page_id}_{cid}" value="{clabel}" style="{container_style}" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="{cluster_x}" y="40" width="{container_width}" height="{container_height}" as="geometry"/>')
        xml.append('        </mxCell>')

        node_y = 50
        for n in cnodes:
            raw_label = f"<b>{n['label']}</b>"
            if n.get("sublabel"):
                raw_label += f"<br/><small>{n['sublabel']}</small>"

            lbl_escaped = html.escape(raw_label, quote=True)
            kind = n.get("kind", "EconomicEntity")
            domains_list = n.get("domains", [])
            style = get_drawio_style(kind, domains_list)

            # Core formal properties as XML attributes
            attrs = {
                "kind": kind,
                "domains": ", ".join(domains_list),
                "cluster": cid,
                "vsm_system": n.get("vsm_system", ""),
                "vsm_recursion_level": n.get("vsm_recursion_level", ""),
                "jurisdiction": n.get("jurisdiction", "Global"),
                "eu_ai_act_role": n.get("eu_ai_act_role") or "",
                "nist_function": n.get("nist_function") or "",
                "cardinality_min": str(n.get("cardinality_log10_min", "")),
                "cardinality_max": str(n.get("cardinality_log10_max", "")),
                "cardinality_unit": str(n.get("cardinality_unit", "")),
            }
            # Append dynamic properties
            for k, v in n.get("properties", {}).items():
                attrs[k] = str(v)

            attrs_str = " ".join([f'{html.escape(k, quote=True)}="{html.escape(str(v), quote=True)}"' for k, v in attrs.items()])

            xml.append(f'        <object id="{n["id"]}" label="{lbl_escaped}" {attrs_str}>')
            xml.append(f'          <mxCell style="{style}" vertex="1" parent="{page_id}_{cid}">')
            xml.append(f'            <mxGeometry x="30" y="{node_y}" width="220" height="75" as="geometry"/>')
            xml.append('          </mxCell>')
            xml.append('        </object>')
            node_y += 110

        cluster_x += 320

    for e in edges:
        elbl = html.escape(e.get("label", ""), quote=True)
        rkind = e.get("relation_kind", "data_flow")
        style = get_edge_style(rkind)
        eid = html.escape(e.get("id", f"{page_id}_{e['from']}_{e['to']}"), quote=True)
        asym = html.escape(str(e.get("power_asymmetry", "")), quote=True)
        scost = html.escape(str(e.get("switching_cost", "")), quote=True)
        polarity = html.escape(str(e.get("polarity", "neutral")), quote=True)
        plane = html.escape(str(e.get("protocol_plane", "NONE")), quote=True)

        edge_attrs = f'power_asymmetry="{asym}" switching_cost="{scost}" polarity="{polarity}" protocol_plane="{plane}" relation_kind="{html.escape(rkind, quote=True)}"'

        xml.append(f'        <mxCell id="{eid}" value="{elbl}" style="{style}" edge="1" source="{e["from"]}" target="{e["to"]}" parent="1" {edge_attrs}>')
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

    # Page 1: Complete Unified Master Model
    all_nodes = {n["id"]: n for n in model["nodes"]}
    xml.append(render_diagram_page("master_view", "1. Master Model (All Elements)", clusters, all_nodes, model["edges"]))

    # Pages 2-4: Dedicated Domain Projections
    domain_views = [
        ("view_economic",   "2. Economic & Capital Flows",        "economic"),
        ("view_governance", "3. Governance & Regulatory Lens",    "governance"),
        ("view_technical",  "4. Technical & Protocol Architecture","technical"),
    ]

    for vid, vtitle, dom in domain_views:
        f_nodes = {n["id"]: n for n in model["nodes"] if dom in n.get("domains", [])}
        f_edges = [
            e for e in model["edges"]
            if dom in e.get("domains", []) and e["from"] in f_nodes and e["to"] in f_nodes
        ]
        xml.append(render_diagram_page(vid, vtitle, clusters, f_nodes, f_edges))

    xml.append('</mxfile>')
    target_file.write_text("\n".join(xml), encoding="utf-8")
    print(f"[OK] Draw.io multi-page export created: {target_file.name}")

if __name__ == "__main__":
    main()