"""Unit tests for data integrity and generators (python -m unittest discover -s tests)."""
import io, json, subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build, validate  # noqa: E402
from common import load_all, load_metrics  # noqa: E402


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load_all()

    def test_validate_clean(self):
        self.assertEqual(validate.errors(), [])

    def test_featured_have_both_languages(self):
        for e in self.d["entries"]:
            if e["featured"]:
                self.assertTrue(e["why"] and e["why_en"], e["id"])

    def test_every_entry_has_evidence_and_date(self):
        for e in self.d["entries"]:
            self.assertGreaterEqual(len(e["evidence"]), 3, e["id"])
            self.assertRegex(e["verified_at"], r"^\d{4}-\d{2}-\d{2}$")

    def test_no_oh_my_posh_noise(self):
        for e in self.d["entries"]:
            self.assertNotRegex((e["name"] + " " + e["evidence"]).lower(), r"oh-my-posh|openmp", e["id"])

    def test_core_entry_is_can1357(self):
        core = [e for e in self.d["entries"] if e["id"] == "oh-my-pi"][0]
        self.assertEqual(core["repo"], "can1357/oh-my-pi")
        self.assertEqual(core["omp_support"], "native")

    def test_anchor_per_entry_in_ecosystem(self):
        txt = build.ecosystem(self.d, load_metrics())
        for e in self.d["entries"]:
            self.assertIn(f'<a id="{e["id"]}"></a>', txt)

    def test_readme_blocks_counts(self):
        bl = build.blocks(self.d, load_metrics())
        self.assertEqual(bl["top3"].count("\n") + 1, 3)
        feat = sum(e["featured"] for e in self.d["entries"])
        self.assertEqual(sum(l.startswith("- **[") for l in bl["featured"].splitlines()), feat)
        self.assertNotIn("| Data |", bl["featured"])
        self.assertIn(str(len(self.d["entries"])), bl["stats"])

    def test_featured_grouped_by_task(self):
        tasks = [t[0] for t in build.TASKS]
        for e in self.d["entries"]:
            if e["featured"]:
                self.assertIn(e.get("task"), tasks, e["id"])
        for en in (False, True):
            bl = build.blocks(self.d, load_metrics(), en)
            self.assertEqual(bl["featured"].count("### "), len({e["task"] for e in self.d["entries"] if e["featured"]}))

    def test_lore_block_from_milestones(self):
        lore = [x for x in self.d["milestones"] if x.get("lore")]
        self.assertGreaterEqual(len(lore), 3)
        for en in (False, True):
            bl = build.blocks(self.d, load_metrics(), en)
            self.assertEqual(bl["lore"].count("\n") + 1, len(lore))
            for x in lore:
                self.assertIn(x["date"], bl["lore"])

    def test_readme_safety_notice_on_first_screen(self):
        for f in ("README.md", "README.en.md"):
            head = "\n".join((ROOT / f).read_text(encoding="utf-8").splitlines()[:20])
            self.assertIn("[!WARNING]", head, f)
            self.assertIn("--no-extensions", head, f)

    def test_misconceptions_cover_name_confusion(self):
        ids = {m["id"] for m in self.d["misconceptions"]}
        self.assertTrue({"not-oh-my-posh", "npm-name"} <= ids)

    def test_build_idempotent(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/build.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class ProbeSummaryTests(unittest.TestCase):
    def run_summary(self, payload, want):
        r = subprocess.run([sys.executable, str(ROOT / "examples/summarize_probe.py"), want],
                           input=json.dumps(payload), capture_output=True, text=True)
        return r.stdout

    def test_found(self):
        p = {"ready": True, "get_available_commands": {"data": {"commands": [{"name": "hello-omp"}, {"name": "x"}]}}}
        self.assertIn("hello-omp found: True", self.run_summary(p, "hello-omp"))

    def test_skill_prefix(self):
        p = {"ready": True, "get_available_commands": {"data": {"commands": [{"name": "skill:hello"}]}}}
        self.assertIn("['skill:hello']", self.run_summary(p, "hello"))

    def test_not_ready(self):
        self.assertIn("ready: None", self.run_summary({}, "x"))


if __name__ == "__main__":
    unittest.main()
