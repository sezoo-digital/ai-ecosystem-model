import sys
import json
import yaml
from pathlib import Path

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def to_title_header(snake_str):
    acronyms = {"eu": "EU", "ai": "AI", "id": "ID", "mcp": "MCP", "iam": "IAM", "api": "API", "tos": "ToS", "vsm": "VSM", "nist": "NIST", "coala": "CoALA", "rag": "RAG"}
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

    # Build Elements losslessly
    for n in model.get("nodes", []):
        domains = n.get("domains", [])
        primary_domain = domains[0].capitalize() if domains else "Entity"
        cid = n.get("cluster", "")
        cluster_name = clusters_map.get(cid, cid)
        
        element = {
            "id": n["id"],
            "label": n.get("label", n["id"]),
            "type": primary_domain,
            "description": n.get("sublabel", ""),
            "tags": domains,
            "shape": n.get("shape", "rect"),
            "Cluster": cluster_name,
            "Cluster ID": cid
        }

        # Promote all dynamic properties (VSM, NIST, CoALA, Cardinality, etc.)
        for prop_key, prop_val in n.get("properties", {}).items():
            element[to_title_header(prop_key)] = prop_val

        blueprint["elements"].append(element)

    # Build Connections losslessly
    for i, e in enumerate(model.get("edges", [])):
        connection = {
            "id": f"conn_{i}",
            "from": e["from"],
            "to": e["to"],
            "label": e.get("label", ""),
            "type": e.get("type", "flow"),
            "direction": "directed",
            "tags": e.get("domains", []),
            "description": f"Relationship type: {e.get('type', 'flow')}"
        }
        blueprint["connections"].append(connection)

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(blueprint, f, indent=2, ensure_ascii=False)

    print(f"[OK] Kumu Blueprint JSON created: {target_file.name}")
    print(f"     Elements: {len(blueprint['elements'])}, Connections: {len(blueprint['connections'])}")

if __name__ == "__main__":
    main()