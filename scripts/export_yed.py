import yaml
import html
from pathlib import Path

def export_view_to_graphml(model, view_def, output_file):
    view_domains = set(view_def["domains"])
    active_nodes = {n["id"]: n for n in model["nodes"] if any(d in view_domains for d in n["domains"])}
    active_edges = [
        e for e in model["edges"] 
        if any(d in view_domains for d in e["domains"]) and e["from"] in active_nodes and e["to"] in active_nodes
    ]

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns"',
        '         xmlns:y="http://www.yworks.com/xml/graphml"',
        '         xmlns:yed="http://www.yworks.com/xml/yed/3">',
        '  <key for="node" id="d_graphics" yfiles.type="nodegraphics"/>',
        '  <key for="edge" id="d_edge_graphics" yfiles.type="edgegraphics"/>',
        '  <key for="node" id="d_sublabel" attr.name="sublabel" attr.type="string"/>',
        '  <key for="node" id="d_props" attr.name="properties" attr.type="string"/>',
        '  <graph id="G" edgedefault="directed">'
    ]

    for n in active_nodes.values():
        props_str = " | ".join([f"{k}: {v}" for k, v in n.get("properties", {}).items()])
        lbl = html.escape(n["label"])
        sub = html.escape(n.get("sublabel", ""))
        full_label = f"{lbl}\n({sub})" if sub else lbl
        
        xml.append(f'    <node id="{n["id"]}">')
        xml.append(f'      <data key="d_sublabel">{sub}</data>')
        xml.append(f'      <data key="d_props">{html.escape(props_str)}</data>')
        xml.append('      <data key="d_graphics">')
        xml.append('        <y:ShapeNode>')
        xml.append('          <y:Geometry width="220" height="70"/>')
        xml.append('          <y:Fill color="#F8FAFC" transparent="false"/>')
        xml.append('          <y:BorderStyle color="#1E40AF" type="line" width="2.0"/>')
        xml.append(f'          <y:NodeLabel alignment="center" autoSizePolicy="content">{full_label}</y:NodeLabel>')
        xml.append('          <y:Shape type="roundrectangle"/>')
        xml.append('        </y:ShapeNode>')
        xml.append('      </data>')
        xml.append('    </node>')

    for i, e in enumerate(active_edges):
        elbl = html.escape(e.get("label", ""))
        color = "#16A34A" if e.get("type") == "money" else "#1E40AF"
        xml.append(f'    <edge id="e{i}" source="{e["from"]}" target="{e["to"]}">')
        xml.append('      <data key="d_edge_graphics">')
        xml.append('        <y:PolyLineEdge>')
        xml.append(f'          <y:LineStyle color="{color}" type="line" width="2.0"/>')
        xml.append('          <y:Arrows source="none" target="standard"/>')
        if elbl:
            xml.append(f'          <y:EdgeLabel alignment="center">{elbl}</y:EdgeLabel>')
        xml.append('        </y:PolyLineEdge>')
        xml.append('      </data>')
        xml.append('    </edge>')

    xml.append('  </graph>')
    xml.append('</graphml>')
    Path(output_file).write_text("\n".join(xml), encoding="utf-8")

def main():
    with open("model/ai_ecosystem.yaml", "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    export_path = Path("static/exports")
    export_path.mkdir(parents=True, exist_ok=True)

    for v in model.get("views", []):
        target = export_path / f"{v['id']}.graphml"
        export_view_to_graphml(model, v, target)
        print(f"✔ yEd export: {target}")

if __name__ == "__main__":
    main()