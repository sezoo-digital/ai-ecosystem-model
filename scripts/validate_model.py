import sys
import yaml
from pathlib import Path
from linkml.validator import validate

# Force UTF-8 console output on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_FILE = PROJECT_ROOT / "schema" / "ai_ecosystem_schema.yaml"
MODEL_FILE = PROJECT_ROOT / "model" / "ai_ecosystem.yaml"

def main():
    if not SCHEMA_FILE.exists():
        sys.exit(f"[ERROR] Schema not found at: {SCHEMA_FILE}")
    if not MODEL_FILE.exists():
        sys.exit(f"[ERROR] Model file not found at: {MODEL_FILE}")

    print(f"[VALIDATE] Validating {MODEL_FILE.name} against {SCHEMA_FILE.name}...")
    
    # 1. Load the actual model data into a Python dictionary
    with open(MODEL_FILE, "r", encoding="utf-8") as f:
        instance_data = yaml.safe_load(f)

    # 2. Pass the parsed data object to LinkML
    report = validate(
        instance=instance_data,
        schema=str(SCHEMA_FILE),
        target_class="EcosystemModel"
    )

    if not report.results:
        print("[OK] Schema validation successful: Model conforms to LinkML metamodel.")
        sys.exit(0)
    else:
        print(f"\n[FAILED] Found {len(report.results)} schema violation(s):")
        for res in report.results:
            print(f"  - [{res.severity}] {res.message} (Path: {res.instance})")
        sys.exit(1)

if __name__ == "__main__":
    main()