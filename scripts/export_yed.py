#!/usr/bin/env python3
"""
yEd GraphML Exporter for AI Ecosystem Model.
Outputs: static/exports/ai_ecosystem.graphml
Preserves:
  - yFiles group nodes for clusters
  - Ontological node kinds and custom property keys
  - Edge relation kinds, protocol planes, and polarity
"""

import sys
import yaml
import html
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_yed_shape(kind):
    if kind == "NaturalPerson": return "ellipse"
    if kind == "StatutoryAuthority": return "hexagon"
    if kind == "EconomicEntity": return "rectangle"
    return "roundrectangle"

def get_yed_node_colors(domains):
    if "governance" in domains: return "#FFF1F0", "#F5222D"
    if "economic" in domains: return "#F6FFED", "#52C41A"
    if "technical" in domains: return "#E6F7FF", "#1890FF"
    return "#F8FAFC", "#64748B"

def get_yed_edge_style(relation_kind):
    if relation_kind == "commercial_flow": return "#16A34A", "line", "3.0"
    if relation_kind == "statutory_mandate": return "#722ED1", "line", "3.0"
    if relation_kind in ["liability_exposure", "contractual_term"]: return "#DC2626", "dashed", "2.0"
    if relation_kind == "governance_control": return "#E11D48", "dashed", "2.0"
    if relation_kind == "protocol_call": return "#2563EB", "line", "2.0"
    if relation_kind == "algedonic_signal": return "#B91C1C", "line", "4.0"
    return "#64748B", "line", "1.5"

def main():
    model_file = PROJECT_ROOT / "model" / "ai_ecosystem.yaml"
    if not model_file.exists():
        sys.exit(f"[ERROR] Model file not found at: {model_file}")

    with open(model_file, "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    export_path = PROJECT_ROOT / "static" / "exports"
    export_path.mkdir(parents=True, exist_ok=True)
    target_file = export_path / "ai_ecosystem.graphml"

    # Harvest all unique custom properties
    all_prop_keys = set()
    for n in model["nodes"]:
        for k in n.get("properties", {}).keys():
            all_prop_keys.add(k)
    sorted_prop_keys = sorted(list(all_prop_keys))

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns"',
        '         xmlns:y="http://www.yworks.com/xml/graphml"',
        '         xmlns:yed="http://www.yworks.com/xml/yed/3">',
        '  <key for="node" id="d_graphics" yfiles.type="nodegraphics"/>',
        '  <key for="edge" id="d_edge_graphics" yfiles.type="edgegraphics"/>',
        '  <key for="node" id="d_cluster" attr.name="cluster" attr.type="string"/>',
        '  <key for="node" id="d_domains" attr.name="domains" attr.type="string"/>',
        '  <key for="node" id="d_kind" attr.name="kind" attr.type="string"/>',
        '  <key for="node" id="d_sublabel" attr.name="sublabel" attr.type="string"/>',
        '  <key for="node" id="d_vsm" attr.name="vsm_system" attr.type="string"/>',
        '  <key for="node" id="d_eu_role" attr.name="eu_ai_act_role" attr.type="string"/>',
        '  <key for="node" id="d_nist" attr.name="nist_function" attr.type="string"/>',
    ]

    for pk in sorted_prop_keys:
        xml.append(f'  <key for="node" id="d_prop_{pk}" attr.name="{pk}" attr.type="string"/>')

    xml.extend([
        '  <key for="edge" id="d_edge_id" attr.name="edge_id" attr.type="string"/>',
        '  <key for="edge" id="d_edge_domains" attr.name="domains" attr.type="string"/>',
        '  <key for="edge" id="d_edge_relation_kind" attr.name="relation_kind" attr.type="string"/>',
        '  <key for="edge" id="d_edge_protocol_plane" attr.name="protocol_plane" attr.type="string"/>',
        '  <key for="edge" id="d_edge_polarity" attr.name="polarity" attr.type="string"/>',
        '  <graph id="G" edgedefault="directed">'
    ])

    clusters_map = {c["id"]: c.get("label", c["id"]) for c in model.get("clusters", [])}
    nodes_by_cluster = {}
    for n in model["nodes"]:
        cid = n.get("cluster", "cluster_default")
        nodes_by_cluster.setdefault(cid, []).append(n)

    for cid, cnodes in nodes_by_cluster.items():
        clabel = html.escape(clusters_map.get(cid, cid))
        xml.append(f'    <node id="{cid}" yfiles.foldertype="group">')
        xml.append('      <data key="d_graphics">')
        xml.append('        <y:ProxyAutoBoundsNode>')
        xml.append('          <y:Realizers active="0">')
        xml.append('            <y:GroupNode>')
        xml.append('              <y:Geometry width="280" height="350"/>')
        xml.append('              <y:Fill color="#F8FAFC" transparent="false"/>')
        xml.append('              <y:BorderStyle color="#CBD5E1" type="line" width="1.5"/>')
        xml.append(f'              <y:NodeLabel alignment="right" autoSizePolicy="node_width" backgroundColor="#E2E8F0" fontSize="12" fontStyle="bold" modelName="internal" modelPosition="t">{clabel}</y:NodeLabel>')
        xml.append('              <y:Shape type="roundrectangle"/>')
        xml.append('              <y:State closed="false"/>')
        xml.append('            </y:GroupNode>')
        xml.append('          </y:Realizers>')
        xml.append('        </y:ProxyAutoBoundsNode>')
        xml.append('      </data>')
        xml.append(f'      <graph id="{cid}:" edgedefault="directed">')

        for n in cnodes:
            domains = n.get("domains", [])
            domains_str = ", ".join(domains)
            lbl = html.escape(n["label"])
            sub = html.escape(n.get("sublabel", ""))
            full_label = f"{lbl}\n({sub})" if sub else lbl
            
            kind = n.get("kind", "EconomicEntity")
            fill_color, border_color = get_yed_node_colors(domains)
            yed_shape = get_yed_shape(kind)

            xml.append(f'        <node id="{n["id"]}">')
            xml.append(f'          <data key="d_cluster">{html.escape(cid)}</data>')
            xml.append(f'          <data key="d_domains">{html.escape(domains_str)}</data>')
            xml.append(f'          <data key="d_kind">{html.escape(kind)}</data>')
            xml.append(f'          <data key="d_sublabel">{sub}</data>')
            xml.append(f'          <data key="d_vsm">{html.escape(n.get("vsm_system", ""))}</data>')
            xml.append(f'          <data key="d_eu_role">{html.escape(n.get("eu_ai_act_role", ""))}</data>')
            xml.append(f'          <data key="d_nist">{html.escape(n.get("nist_function", ""))}</data>')

            n_props = n.get("properties", {})
            for pk in sorted_prop_keys:
                if pk in n_props:
                    xml.append(f'          <data key="d_prop_{pk}">{html.escape(str(n_props[pk]))}</data>')

            xml.append('          <data key="d_graphics">')
            xml.append('            <y:ShapeNode>')
            xml.append('              <y:Geometry width="230" height="75"/>')
            xml.append(f'              <y:Fill color="{fill_color}" transparent="false"/>')
            xml.append(f'              <y:BorderStyle color="{border_color}" type="line" width="2.0"/>')
            xml.append(f'              <y:NodeLabel alignment="center" autoSizePolicy="content">{full_label}</y:NodeLabel>')
            xml.append(f'              <y:Shape type="{yed_shape}"/>')
            xml.append('            </y:ShapeNode>')
            xml.append('          </data>')
            xml.append('        </node>')

        xml.append('      </graph>')
        xml.append('    </node>')

    for i, e in enumerate(model["edges"]):
        eid = e.get("id", f"e{i}")
        elbl = html.escape(e.get("label", ""))
        domains_str = ", ".join(e.get("domains", []))
        rkind = e.get("relation_kind", "data_flow")
        pplane = e.get("protocol_plane", "NONE")
        polarity = e.get("polarity", "neutral")
        color, line_type, width = get_yed_edge_style(rkind)

        xml.append(f'    <edge id="{html.escape(eid)}" source="{e["from"]}" target="{e["to"]}">')
        xml.append(f'      <data key="d_edge_id">{html.escape(eid)}</data>')
        xml.append(f'      <data key="d_edge_domains">{html.escape(domains_str)}</data>')
        xml.append(f'      <data key="d_edge_relation_kind">{html.escape(rkind)}</data>')
        xml.append(f'      <data key="d_edge_protocol_plane">{html.escape(pplane)}</data>')
        xml.append(f'      <data key="d_edge_polarity">{html.escape(polarity)}</data>')
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
    print(f"[OK] yEd GraphML created: {target_file.name}")

if __name__ == "__main__":
    main()