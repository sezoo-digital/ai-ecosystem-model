import sys
import yaml
import csv
from pathlib import Path

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def sanitize_cell(val):
    """Formats values for Kumu compatibility."""
    if val is None:
        return ""
    if isinstance(val, list):
        # Kumu uses the pipe character '|' for multi-value tags and filters
        return " | ".join(str(v).strip() for v in val)
    return str(val).strip()

def to_title_header(snake_str):
    """Converts snake_case property keys to friendly Kumu Field Titles."""
    return snake_str.replace("_", " ").title()

def main():
    model_file = Path("model/ai_ecosystem.yaml")
    if not model_file.exists():
        print(f"Error: {model_file} not found.")
        return

    with open(model_file, "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    export_path = Path("static/exports")
    export_path.mkdir(parents=True, exist_ok=True)
    target_file = export_path / "ai_ecosystem_kumu.csv"

    clusters_map = {c["id"]: c.get("label", c["id"]) for c in model.get("clusters", [])}

    # 1. Discover all unique property keys across all nodes to generate custom columns
    node_prop_keys = set()
    for n in model.get("nodes", []):
        for k in n.get("properties", {}).keys():
            node_prop_keys.add(k)
    sorted_prop_keys = sorted(list(node_prop_keys))

    # 2. Define Kumu canonical headers
    # Core Kumu columns: ID, Label, Type, Description, Tags, From, To, Direction
    base_headers = [
        "ID",
        "Label",
        "Type",
        "Description",
        "Tags",
        "From",
        "To",
        "Direction",
        "Cluster",
        "Domains"
    ]
    
    # Custom property headers (converted to Title Case for Kumu UI)
    prop_headers = [to_title_header(k) for k in sorted_prop_keys]
    headers = base_headers + prop_headers

    rows = []

    # 3. Export Nodes (Elements)
    for n in model.get("nodes", []):
        domains = n.get("domains", [])
        primary_domain = domains[0].capitalize() if domains else "Entity"
        cluster_label = clusters_map.get(n.get("cluster", ""), n.get("cluster", ""))
        
        row = {
            "ID": n["id"],
            "Label": n.get("label", n["id"]),
            "Type": primary_domain,                      # Sets default element type in Kumu
            "Description": n.get("sublabel", ""),        # Shown in Kumu left drawer
            "Tags": sanitize_cell(domains),              # Filterable tags
            "From": "",                                  # Blank for Elements
            "To": "",                                    # Blank for Elements
            "Direction": "",
            "Cluster": cluster_label,
            "Domains": sanitize_cell(domains)
        }

        # Populate custom dynamic properties
        node_props = n.get("properties", {})
        for raw_k, title_k in zip(sorted_prop_keys, prop_headers):
            row[title_k] = sanitize_cell(node_props.get(raw_k, ""))

        rows.append(row)

    # 4. Export Edges (Connections)
    for i, e in enumerate(model.get("edges", [])):
        etype = e.get("type", "flow")
        edge_domains = e.get("domains", [])
        
        row = {
            "ID": f"conn_{i}",
            "Label": e.get("label", ""),
            "Type": etype,                               # Enables @connection["type"="..."] styling
            "Description": f"Relationship type: {etype}",
            "Tags": sanitize_cell(edge_domains),
            "From": e["from"],                           # Bound to Node ID
            "To": e["to"],                               # Bound to Node ID
            "Direction": "directed",                     # Standard arrow in Kumu
            "Cluster": "",
            "Domains": sanitize_cell(edge_domains)
        }

        # Pad connection rows for property columns
        for title_k in prop_headers:
            row[title_k] = ""

        rows.append(row)

    # 5. Write RFC 4180 compliant CSV
    with open(target_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] Kumu CSV exported successfully: {target_file}")
    print(f"  - Elements:   {len(model.get('nodes', []))}")
    print(f"  - Connections:{len(model.get('edges', []))}")
    print(f"  - Metadata Fields: {len(prop_headers)} custom attributes mapped")

if __name__ == "__main__":
    main()