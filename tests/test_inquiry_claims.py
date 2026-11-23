"""Negative and boundary tests for opt-in inquiry claim ledgers."""
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_inquiry_claims import check_document

KNOWN = {"N_AGENT", "E_AGENT_TO_GATEWAY_A2T"}

def doc(frontmatter, body="<!-- claim: C-01 -->"):
    return "---\n" + frontmatter + "\n---\n" + body

BASE = """id: example
claim_evidence:
  - id: C-01
    classification: derived
    model_refs: [E_AGENT_TO_GATEWAY_A2T]
    assumptions:
      - Gateway mediates all relevant calls."""

class ClaimLedgerTests(unittest.TestCase):
    def check(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inquiry.md"
            path.write_text(content, encoding="utf-8")
            return check_document(path, KNOWN)

    def test_valid_derived(self):
        self.assertEqual([], self.check(doc(BASE)))

    def test_unannotated_legacy_inquiry(self):
        self.assertEqual([], self.check(doc("id: legacy", "Unannotated inquiry.")))

    def test_missing_anchor(self):
        self.assertTrue(any("exactly one" in x for x in self.check(doc(BASE, "No claim anchor"))))

    def test_duplicate_anchor(self):
        self.assertTrue(any("found 2" in x for x in self.check(doc(BASE, "<!-- claim: C-01 -->\n<!-- claim: C-01 -->"))))

    def test_unknown_model_id(self):
        self.assertTrue(any("unknown canonical ID" in x for x in self.check(doc(BASE.replace("E_AGENT_TO_GATEWAY_A2T", "E_NONEXISTENT")))))

    def test_missing_derived_assumption(self):
        self.assertTrue(any("requires explicit assumptions" in x for x in self.check(doc(BASE.replace("    assumptions:\n      - Gateway mediates all relevant calls.", "")))))

    def test_external_requires_url(self):
        s = BASE.replace("derived", "externally-evidenced").replace("    assumptions:\n      - Gateway mediates all relevant calls.", "")
        self.assertTrue(any("requires source URLs" in x for x in self.check(doc(s))))

    def test_unverified_requires_limitations(self):
        s = BASE.replace("derived", "unverified").replace("    assumptions:\n      - Gateway mediates all relevant calls.", "")
        self.assertTrue(any("requires limitations" in x for x in self.check(doc(s))))

    def test_undeclared_anchor(self):
        self.assertTrue(any("undeclared claim anchor" in x for x in self.check(doc(BASE, "<!-- claim: C-01 -->\n<!-- claim: C-02 -->"))))

    def test_missing_frontmatter(self):
        self.assertTrue(self.check("No YAML header"))

    def test_invalid_yaml(self):
        self.assertTrue(self.check("---\nclaim_evidence: [\n---\ntext"))

if __name__ == "__main__":
    unittest.main()
