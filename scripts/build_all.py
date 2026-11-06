#!/usr/bin/env python3
"""
Master build script for AI Ecosystem Model.
Executes documentation generators and multi-format model exporters.
Can be run safely from repo root, from inside scripts/, or via CI/CD.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Force UTF-8 encoding on Windows consoles with fallback replacement
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Determine absolute paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
MODEL_FILE = PROJECT_ROOT / "model" / "ai_ecosystem.yaml"

SCRIPTS = [
    ("Mermaid Documentation Portal", "generate_docs.py"),
    ("Individual Sidebar Views",     "generate_views.py"),
    ("Draw.io Multi-Page Diagram",   "export_drawio.py"),
    ("yEd GraphML Export",           "export_yed.py"),
    ("Kumu Dynamic JSON Export",      "export_kumu.py"),
]

def print_banner(msg):
    print("\n" + "=" * 60)
    print(msg)
    print("=" * 60)

def main():
    print_banner("[START] Starting AI Ecosystem Model Build Pipeline")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Scripts Dir:  {SCRIPT_DIR}")
    print(f"Model Source: {MODEL_FILE}")

    # 1. Pre-flight check: Ensure the model exists before doing anything
    if not MODEL_FILE.exists():
        print(f"\n[FATAL] Model file not found at: {MODEL_FILE}")
        print("Please check that 'model/ai_ecosystem.yaml' exists in your project root.")
        sys.exit(1)

    # 2. Ensure output target directories exist
    (PROJECT_ROOT / "docs" / "ecosystem").mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "static" / "exports").mkdir(parents=True, exist_ok=True)

    # 3. Prepare environment: Force child processes to use UTF-8 and find sibling scripts
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["PYTHONPATH"] = str(SCRIPT_DIR) + (os.pathsep + env.get("PYTHONPATH", "") if env.get("PYTHONPATH") else "")

    total_start = time.time()

    # 4. Run each step
    for desc, script_name in SCRIPTS:
        script_path = SCRIPT_DIR / script_name
        
        if not script_path.exists():
            print(f"\n[FATAL] Script not found: {script_path}")
            sys.exit(1)

        print(f"\n[BUILD] {desc} ({script_name})...")
        step_start = time.time()

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(PROJECT_ROOT),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        # Check for non-zero exit code OR explicit error output
        if result.returncode != 0 or "Traceback" in result.stderr:
            print(f"[FAILED] {script_name} encountered an error:")
            if result.stdout.strip():
                print("\n--- STDOUT ---")
                print(result.stdout.strip())
            if result.stderr.strip():
                print("\n--- STDERR ---")
                print(result.stderr.strip())
            sys.exit(1)

        # Print success output
        for line in result.stdout.strip().splitlines():
            print(f"  {line}")
        print(f"  [OK] Completed in {time.time() - step_start:.2f}s")

    print_banner(f"[SUCCESS] All artifacts generated in {time.time() - total_start:.2f}s")
    print(f"   - Web Docs: {PROJECT_ROOT / 'docs' / 'ecosystem'}")
    print(f"   - Exports:  {PROJECT_ROOT / 'static' / 'exports'}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()