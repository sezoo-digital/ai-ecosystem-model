import sys
import yaml
import html
from pathlib import Path

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def get_yed_shape(shape):
    if shape == "circle":
        return "ellipse"
    elif shape == "hexagon":
        return "hexagon"
    elif shape == "rect":
        return "rectangle"
    else:
        return "roundrectangle"

def get_yed_node_colors(domains):
    if "governance" in domains:
        return "#FFF1F0", "#F5222D"
    elif "economic" in domains:
        return "#F6FFED", "#52C41A"
    elif "technical" in domains:
        return "#E6F7FF", "#1890FF"
    return "#F8FAFC", "#64748B"

def get_yed_edge_style(etype):
    if etype == "money":
        return "#16A34A", "line", "3.0"
    elif etype == "authority":
        return "#722ED1", "line", "3.0"
    elif etype in ["tension", "disclaim"]:
        return "#DC2626", "dashed", "2.0"
    elif etype == "governance_control":
        return "#E11D48", "dashed", "2.0"
    elif etype == "protocol":
        return "#2563EB", "line", "2.0"
    return "#64748B", "line", "1.5"

def main():
    model_file = Path("model/ai_ecosystem.yaml")
    if not model_file.exists():
        print(f"Error: {model_file} not found.")
        return

    with open(model_file, "r", encoding="utf-8") as f:
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

    # Export Nodes
    for n in model["nodes"]:
        domains = n.get("domains", [])
        domains_str = ", ".join(domains)
        props_str = " | ".join([f"{k}: {v}" for k, v in n.get("properties", {}).items()])
        lbl = html.escape(n["label"])
        sub = html.escape(n.get("sublabel", ""))
        full_label = f"{lbl}\n({sub})" if sub else lbl
        
        fill_color, border_color = get_yed_node_colors(domains)
        yed_shape = get_yed_shape(n.get("shape", "rect"))

        xml.append(f'    <node id="{n["id"]}">')
        xml.append(f'      <data key="d_cluster">{html.escape(n.get("cluster", ""))}</data>')
        xml.append(f'      <data key="d_domains">{html.escape(domains_str)}</data>')
        xml.append(f'      <data key="d_sublabel">{sub}</data>')
        xml.append(f'      <data key="d_properties">{html.escape(props_str)}</data>')
        xml.append('      <data key="d_graphics">')
        xml.append('        <y:ShapeNode>')
        xml.append('          <y:Geometry width="230" height="75"/>')
        xml.append(f'          <y:Fill color="{fill_color}" transparent="false"/>')
        xml.append(f'          <y:BorderStyle color="{border_color}" type="line" width="2.0"/>')
        xml.append(f'          <y:NodeLabel alignment="center" autoSizePolicy="content">{full_label}</y:NodeLabel>')
        xml.append(f'          <y:Shape type="{yed_shape}"/>')
        xml.append('        </y:ShapeNode>')
        xml.append('      </data>')
        xml.append('    </node>')

    # Export Edges
    for i, e in enumerate(model["edges"]):
        elbl = html.escape(e.get("label", ""))
        domains_str = ", ".join(e.get("domains", []))
        etype = e.get("type", "flow")
        color, line_type, width = get_yed_edge_style(etype)

        xml.append(f'    <edge id="e{i}" source="{e["from"]}" target="{e["to"]}">')
        xml.append(f'      <data key="d_edge_domains">{html.escape(domains_str)}</data>')
        xml.append(f'      <data key="d_edge_type">{html.escape(etype)}</data>')
        xml.append('      <data key="d_edge_graphics">')
        xml.append('        <y:PolyLineEdge>')
        xml.append(f'          <y:LineStyle color="{color}" type="{line_type}" width="{width}"/>')
        xml.append('          <y:Arrows source="none" target="standard"/>')
        if elbl:
            xml.append(f'          <y:EdgeLabel alignment="center">{elbl}</y:EdgeLabel>')
        xml.append('        </y:PolyLineEdge>')
        xml.append('      </data>')
        xml.append('    </edge>')

    xml.append('  </graph>')
    xml.append('</graphml>')
    target_file.write_text("\n".join(xml), encoding="utf-8")
    print(f"[OK] Unified yEd GraphML created: {target_file}")

if __name__ == "__main__":
    main()