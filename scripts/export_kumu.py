#!/usr/bin/env python3
"""
Kumu Dynamic Blueprint JSON Exporter for AI Ecosystem Model.
Outputs: static/exports/ai_ecosystem_kumu.json
Formats:
  - Elements: Promotes Kind, VSM System, Recursion Level, Ashby Variety, and Jurisdiction to Kumu fields
  - Connections: Preserves relation_kind, protocol_plane, polarity, power_asymmetry, and switching_cost
"""

import sys
import json
import yaml
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def to_title_header(snake_str):
    acronyms = {
        "eu": "EU", "ai": "AI", "id": "ID", "mcp": "MCP",
        "iam": "IAM", "api": "API", "tos": "ToS", "vsm": "VSM",
        "nist": "NIST", "coala": "CoALA", "rag": "RAG", "gpai": "GPAI"
    }
    words = snake_str.split("_")
    return " ".join(acronyms.get(w.lower(), w.capitalize()) for w in words)

def main():
    model_file = PROJECT_ROOT / "model" / "ai_ecosystem.yaml"
    if not model_file.exists():
        sys.exit(f"[ERROR] Model file not found at: {model_file}")

    with open(model_file, "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    export_path = PROJECT_ROOT / "static" / "exports"
    export_path.mkdir(parents=True, exist_ok=True)
    target_file = export_path / "ai_ecosystem_kumu.json"

    clusters_map = {c["id"]: c.get("label", c["id"]) for c in model.get("clusters", [])}

    blueprint = {
        "elements": [],
        "connections": []
    }

    # Build Elements
    for n in model.get("nodes", []):
        domains = n.get("domains", [])
        primary_domain = domains[0].capitalize() if domains else "Entity"
        cid = n.get("cluster", "")
        cluster_name = clusters_map.get(cid, cid)
        
        c_min = n.get("cardinality_log10_min")
        c_max = n.get("cardinality_log10_max")
        c_unit = n.get("cardinality_unit", "")
        variety_str = f"10^{c_min:g}–10^{c_max:g} {c_unit}" if c_min is not None and c_max is not None else ""

        element = {
            "id": n["id"],
            "label": n.get("label", n["id"]),
            "type": primary_domain,
            "description": n.get("sublabel", ""),
            "tags": domains,
            "Kind": n.get("kind", "EconomicEntity"),
            "VSM System": n.get("vsm_system", ""),
            "VSM Recursion Level": n.get("vsm_recursion_level", ""),
            "Jurisdiction": n.get("jurisdiction", "Global"),
            "Ashby Variety": variety_str,
            "EU AI Act Role": n.get("eu_ai_act_role") or "Not Specified",
            "NIST Function": n.get("nist_function") or "Not Specified",
            "Cluster": cluster_name,
            "Cluster ID": cid
        }

        # Promote dynamic properties (e.g. compute_profile, capex_cycle, etc.)
        for prop_key, prop_val in n.get("properties", {}).items():
            element[to_title_header(prop_key)] = prop_val

        blueprint["elements"].append(element)

    # Build Connections
    for i, e in enumerate(model.get("edges", [])):
        rkind = e.get("relation_kind", "data_flow")
        pplane = e.get("protocol_plane", "NONE")
        polarity = e.get("polarity", "neutral")

        connection = {
            "id": e.get("id", f"conn_{i}"),
            "from": e["from"],
            "to": e["to"],
            "label": e.get("label", ""),
            "type": rkind,
            "direction": "directed",
            "tags": e.get("domains", []),
            "Protocol Plane": pplane,
            "Polarity": polarity,
            "description": f"Kind: {rkind} | Protocol: {pplane} | Polarity: {polarity}"
        }

        if "power_asymmetry" in e:
            connection["Power Asymmetry"] = e["power_asymmetry"]
        if "switching_cost" in e:
            connection["Switching Cost"] = e["switching_cost"]

        blueprint["connections"].append(connection)

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(blueprint, f, indent=2, ensure_ascii=False)

    print(f"[OK] Kumu Blueprint JSON created: {target_file.name}")
    print(f"     Elements: {len(blueprint['elements'])}, Connections: {len(blueprint['connections'])}")

if __name__ == "__main__":
    main()