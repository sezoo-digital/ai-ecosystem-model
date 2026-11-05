import yaml
import html
from pathlib import Path

def export_view_to_drawio(model, view_def, output_file):
    view_domains = set(view_def["domains"])
    active_nodes = {n["id"]: n for n in model["nodes"] if any(d in view_domains for d in n["domains"])}
    active_edges = [
        e for e in model["edges"] 
        if any(d in view_domains for d in e["domains"]) and e["from"] in active_nodes and e["to"] in active_nodes
    ]

    xml = [
        '<mxfile host="app.diagrams.net">',
        f'  <diagram id="{view_def["id"]}" name="{html.escape(view_def["title"])}">',
        '    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">',
        '      <root>',
        '        <mxCell id="0"/>',
        '        <mxCell id="1" parent="0"/>'
    ]

    x, y = 40, 40
    for n in active_nodes.values():
        lbl = f"<b>{html.escape(n['label'])}</b><br/><small>{html.escape(n.get('sublabel', ''))}</small>"
        style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#1E40AF;strokeWidth=2;"
        xml.append(f'        <mxCell id="{n["id"]}" value="{lbl}" style="{style}" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="{x}" y="{y}" width="200" height="70" as="geometry"/>')
        xml.append('        </mxCell>')
        y += 100
        if y > 500:
            y = 40
            x += 260

    for i, e in enumerate(active_edges):
        elbl = html.escape(e.get("label", ""))
        color = "#16A34A" if e.get("type") == "money" else "#1E40AF"
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor={color};strokeWidth=2;html=1;"
        xml.append(f'        <mxCell id="edge_{i}" value="{elbl}" style="{style}" edge="1" source="{e["from"]}" target="{e["to"]}" parent="1">')
        xml.append('          <mxGeometry relative="1" as="geometry"/>')
        xml.append('        </mxCell>')

    xml.append('      </root>')
    xml.append('    </mxGraphModel>')
    xml.append('  </diagram>')
    xml.append('</mxfile>')
    Path(output_file).write_text("\n".join(xml), encoding="utf-8")

def main():
    with open("model/ai_ecosystem.yaml", "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    export_path = Path("static/exports")
    export_path.mkdir(parents=True, exist_ok=True)

    for v in model.get("views", []):
        target = export_path / f"{v['id']}.drawio"
        export_view_to_drawio(model, v, target)
        print(f"✔ draw.io export: {target}")

if __name__ == "__main__":
    main()