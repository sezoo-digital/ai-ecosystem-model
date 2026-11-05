import yaml
import html
from pathlib import Path

def render_diagram_page(page_id, page_name, nodes, edges):
    xml = [
        f'  <diagram id="{page_id}" name="{html.escape(page_name)}">',
        '    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">',
        '      <root>',
        '        <mxCell id="0"/>',
        '        <mxCell id="1" parent="0"/>'
    ]

    x, y = 40, 40
    for n in nodes.values():
        lbl = f"<b>{html.escape(n['label'])}</b><br/><small>{html.escape(n.get('sublabel', ''))}</small>"
        style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#1E40AF;strokeWidth=2;"
        domains_str = ", ".join(n.get("domains", []))
        props_attrs = " ".join([f'{html.escape(k)}="{html.escape(str(v))}"' for k, v in n.get("properties", {}).items()])

        # Encapsulate as draw.io <object> with custom data attributes
        xml.append(f'        <object id="{n["id"]}" label="{lbl}" domains="{html.escape(domains_str)}" cluster="{html.escape(n.get("cluster", ""))}" {props_attrs}>')
        xml.append(f'          <mxCell style="{style}" vertex="1" parent="1">')
        xml.append(f'            <mxGeometry x="{x}" y="{y}" width="200" height="70" as="geometry"/>')
        xml.append('          </mxCell>')
        xml.append('        </object>')

        y += 100
        if y > 500:
            y = 40
            x += 260

    for i, e in enumerate(edges):
        elbl = html.escape(e.get("label", ""))
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

    # Page 2+: Filtered Views from YAML
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
    print(f"✔ Unified draw.io file created with tabs: {target_file}")

if __name__ == "__main__":
    main()