#!/usr/bin/env python3
"""
Master build script for AI Ecosystem Model (v3.0).
1. Executes Claude's relational and cybernetic validator (validate_ecosystem.py)
2. Compiles canonical master docs/index.md (generate_docs.py)
3. Validates referential integrity of inquiry pages
4. Generates multi-format visual exports (Draw.io, yEd, Kumu)
"""

import sys
import os
import subprocess
import time
import yaml
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
MODEL_FILE = PROJECT_ROOT / "model" / "ai_ecosystem.yaml"
SCHEMA_FILE = PROJECT_ROOT / "schema" / "ai_ecosystem_schema.yaml"
INQUIRIES_DIR = PROJECT_ROOT / "docs" / "inquiries"

inquiry_docs = [str(p) for p in INQUIRIES_DIR.glob("*.md")] if INQUIRIES_DIR.exists() else []

PIPELINE = [
        ("Ecosystem & Cybernetic Validation", "validate_ecosystem.py", 
         [str(MODEL_FILE), str(SCHEMA_FILE)] + (["--refs"] + inquiry_docs if inquiry_docs else [])),
        ("Standing Inquiry Regression Analysis", "analyze_ecosystem.py", [str(MODEL_FILE), "all"]),
        ("Master Documentation Portal",      "generate_docs.py", []),
        ("Viewer Data Bundle Export",         "export_viewer_data.py", []),
        ("Draw.io Multi-Page Diagram",        "export_drawio.py", []),
        ("yEd GraphML Export",                "export_yed.py", []),
        ("Kumu Dynamic JSON Export",           "export_kumu.py", []),
    ]

def validate_inquiries():
    """Verifies that all node IDs referenced in inquiry frontmatter exist in ai_ecosystem.yaml."""
    if not INQUIRIES_DIR.exists():
        return

    with open(MODEL_FILE, "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)
    valid_node_ids = {n["id"] for n in model.get("nodes", [])}

    inquiry_files = list(INQUIRIES_DIR.glob("*.md"))
    if not inquiry_files:
        return

    print(f"\n[VALIDATE] Checking {len(inquiry_files)} inquiry file(s) for referential integrity...")
    for md_file in inquiry_files:
        content = md_file.read_text(encoding="utf-8")
        if not content.startswith("---"):
            continue
        try:
            _, frontmatter_text, _ = content.split("---", 2)
            meta = yaml.safe_load(frontmatter_text)
            active_nodes = meta.get("active_nodes", [])
            for nid in active_nodes:
                if nid not in valid_node_ids:
                    print(f"  [ERROR] {md_file.name} references unknown node ID: '{nid}'")
                    sys.exit(1)
            print(f"  [OK] {md_file.name} (All {len(active_nodes)} node references valid)")
        except Exception as e:
            print(f"  [WARN] Could not parse frontmatter in {md_file.name}: {e}")

def main():
    print("=" * 60)
    print("[START] AI Ecosystem Model Build Pipeline (v3.0)")
    print("=" * 60)

    if not MODEL_FILE.exists():
        sys.exit(f"[FATAL] Model file not found at: {MODEL_FILE}")
    if not SCHEMA_FILE.exists():
        sys.exit(f"[FATAL] Schema file not found at: {SCHEMA_FILE}")

    (PROJECT_ROOT / "docs").mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "docs" / "inquiries").mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "static" / "exports").mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["PYTHONPATH"] = str(SCRIPT_DIR)

    start_time = time.time()

    # Run core scripts
    for desc, script_name, extra_args in PIPELINE:
        script_path = SCRIPT_DIR / script_name
        if not script_path.exists():
            sys.exit(f"[FATAL] Script not found: {script_path}")

        print(f"\n[BUILD] {desc} ({script_name})...")
        step_start = time.time()
        cmd = [sys.executable, str(script_path)] + extra_args
        result = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        if result.returncode != 0:
            print(f"[FAILED] {script_name} failed:")
            print(result.stdout)
            print(result.stderr)
            sys.exit(1)

        for line in result.stdout.strip().splitlines():
            print(f"  {line}")
        print(f"  [OK] Completed in {time.time() - step_start:.2f}s")

    # Verify optional claim-evidence ledgers; this does not assess semantic truth.
    if inquiry_docs:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "validate_inquiry_claims.py"),
             str(MODEL_FILE)] + inquiry_docs,
            cwd=str(PROJECT_ROOT), env=env, capture_output=True,
            text=True, encoding="utf-8", errors="replace"
        )
        print(result.stdout, end="")
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr, end="")
            sys.exit(1)

    # Run inquiry referential check
    validate_inquiries()

    print("\n" + "=" * 60)
    print(f"[SUCCESS] All artifacts generated in {time.time() - start_time:.2f}s")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()