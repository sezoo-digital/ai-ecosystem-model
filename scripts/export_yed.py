import yaml
import html
from pathlib import Path

def main():
    with open("model/ai_ecosystem.yaml", "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    export_path = Path("static/exports")
    export_path.mkdir(parents=True, exist_ok=True)
    target_file = export_path / "ai_ecosystem.graphml"

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns"',
        '         xmlns:y="http://www.yworks.com/xml/graphml"',
        '         xmlns:yed="http://www.yworks.com/xml/yed/3">',
        '  <key for="node" id="d_graphics" yfiles.type="nodegraphics"/>',
        '  <key for="edge" id="d_edge_graphics" yfiles.type="edgegraphics"/>',
        '  <key for="node" id="d_cluster" attr.name="cluster" attr.type="string"/>',
        '  <key for="node" id="d_domains" attr.name="domains" attr.type="string"/>',
        '  <key for="node" id="d_sublabel" attr.name="sublabel" attr.type="string"/>',
        '  <key for="node" id="d_properties" attr.name="properties" attr.type="string"/>',
        '  <key for="edge" id="d_edge_domains" attr.name="domains" attr.type="string"/>',
        '  <key for="edge" id="d_edge_type" attr.name="type" attr.type="string"/>',
        '  <graph id="G" edgedefault="directed">'
    ]

    # Export All Nodes with Attributes
    for n in model["nodes"]:
        domains_str = ", ".join(n.get("domains", []))
        props_str = " | ".join([f"{k}: {v}" for k, v in n.get("properties", {}).items()])
        lbl = html.escape(n["label"])
        sub = html.escape(n.get("sublabel", ""))
        full_label = f"{lbl}\n({sub})" if sub else lbl
        
        xml.append(f'    <node id="{n["id"]}">')
        xml.append(f'      <data key="d_cluster">{html.escape(n.get("cluster", ""))}</data>')
        xml.append(f'      <data key="d_domains">{html.escape(domains_str)}</data>')
        xml.append(f'      <data key="d_sublabel">{sub}</data>')
        xml.append(f'      <data key="d_properties">{html.escape(props_str)}</data>')
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

    # Export All Edges with Attributes
    for i, e in enumerate(model["edges"]):
        elbl = html.escape(e.get("label", ""))
        domains_str = ", ".join(e.get("domains", []))
        etype = e.get("type", "flow")
        color = "#16A34A" if etype == "money" else ("#DC2626" if etype in ["tension", "disclaim"] else "#1E40AF")
        
        xml.append(f'    <edge id="e{i}" source="{e["from"]}" target="{e["to"]}">')
        xml.append(f'      <data key="d_edge_domains">{html.escape(domains_str)}</data>')
        xml.append(f'      <data key="d_edge_type">{html.escape(etype)}</data>')
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
    target_file.write_text("\n".join(xml), encoding="utf-8")
    print(f"✔ Unified yEd GraphML created: {target_file}")

if __name__ == "__main__":
    main()