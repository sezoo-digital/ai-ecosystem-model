import yaml
import html
from pathlib import Path

def render_diagram_page(page_id, page_name, nodes, edges):
    xml = [
        f'  <diagram id="{page_id}" name="{html.escape(page_name, quote=True)}">',
        '    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">',
        '      <root>',
        '        <mxCell id="0"/>',
        '        <mxCell id="1" parent="0"/>'
    ]

    x, y = 40, 40
    for n in nodes.values():
        # 1. Build raw HTML label
        raw_label = f"<b>{n['label']}</b>"
        if n.get("sublabel"):
            raw_label += f"<br/><small>{n['sublabel']}</small>"
            
        # 2. Escape it specifically for an XML attribute (converts < to &lt;, > to &gt;, " to &quot;)
        lbl_escaped = html.escape(raw_label, quote=True)
        
        style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#1E40AF;strokeWidth=2;"
        domains_str = html.escape(", ".join(n.get("domains", [])), quote=True)
        cluster_str = html.escape(n.get("cluster", ""), quote=True)
        
        # 3. Escape all custom properties for XML attributes
        props_attrs = " ".join([
            f'{html.escape(k, quote=True)}="{html.escape(str(v), quote=True)}"' 
            for k, v in n.get("properties", {}).items()
        ])

        # Encapsulate as draw.io <object> with valid XML attributes
        xml.append(f'        <object id="{n["id"]}" label="{lbl_escaped}" domains="{domains_str}" cluster="{cluster_str}" {props_attrs}>')
        xml.append(f'          <mxCell style="{style}" vertex="1" parent="1">')
        xml.append(f'            <mxGeometry x="{x}" y="{y}" width="220" height="70" as="geometry"/>')
        xml.append('          </mxCell>')
        xml.append('        </object>')

        y += 100
        if y > 500:
            y = 40
            x += 260

    for i, e in enumerate(edges):
        elbl = html.escape(e.get("label", ""), quote=True)
        etype = e.get("type", "flow")
        color = "#16A34A" if etype == "money" else ("#DC2626" if etype in ["tension", "disclaim"] else "#1E40AF")
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor={color};strokeWidth=2;html=1;"

        xml.append(f'        <mxCell id="{page_id}_edge_{i}" value="{elbl}" style="{style}" edge="1" source="{e["from"]}" target="{e["to"]}" parent="1">')
        xml.append('          <mxGeometry relative="1" as="geometry"/>')
        xml.append('        </mxCell>')

    xml.append('      </root>')
    xml.append('    </mxGraphModel>')
    xml.append('  </diagram>')
    return "\n".join(xml)

def main():
    with open("model/ai_ecosystem.yaml", "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    export_path = Path("static/exports")
    export_path.mkdir(parents=True, exist_ok=True)
    target_file = export_path / "ai_ecosystem.drawio"

    xml = ['<mxfile host="app.diagrams.net">']

    # Page 1: Complete Master Model
    all_nodes = {n["id"]: n for n in model["nodes"]}
    xml.append(render_diagram_page("master_view", "1. Master Model (All Elements)", all_nodes, model["edges"]))

    # Page 2+: Filtered Views defined in YAML
    for v in model.get("views", []):
        view_domains = set(v["domains"])
        filtered_nodes = {n["id"]: n for n in model["nodes"] if any(d in view_domains for d in n["domains"])}
        filtered_edges = [
            e for e in model["edges"]
            if any(d in view_domains for d in e["domains"]) and e["from"] in filtered_nodes and e["to"] in filtered_nodes
        ]
        xml.append(render_diagram_page(v["id"], v["title"], filtered_nodes, filtered_edges))

    xml.append('</mxfile>')
    target_file.write_text("\n".join(xml), encoding="utf-8")
    print(f"✔ Validated draw.io file created: {target_file}")

if __name__ == "__main__":
    main()