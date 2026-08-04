import tempfile
import unittest
from importlib.resources import files
from pathlib import Path

from user_machine_constitution.cli import init_workspace
from user_machine_constitution.constitution import (
    load_constitution, load_scenarios, render_markdown, validate_constitution,
)

ROOT = Path(__file__).parents[1]


class ConstitutionTests(unittest.TestCase):
    def test_synthetic_example_passes_and_renders(self):
        data, text = load_constitution(ROOT / "examples/sample-constitution.toml")
        scenarios = load_scenarios(ROOT / "examples/sample-stress-tests.json")
        self.assertEqual(validate_constitution(data, text, scenarios=scenarios), [])
        rendered = render_markdown(data)
        self.assertIn("# Constitution for Morgan and Relay", rendered)
        self.assertIn("## Autonomy", rendered)
        self.assertIn("## Failure recovery", rendered)

    def test_unfilled_template_is_rejected(self):
        data, text = load_constitution(ROOT / "templates/constitution-template.toml")
        errors = validate_constitution(data, text, allow_draft=True)
        self.assertTrue(any("unresolved draft marker" in error for error in errors))

    def test_missing_public_write_confirmation_fails(self):
        data, text = load_constitution(ROOT / "examples/sample-constitution.toml")
        data["autonomy"]["always_confirm"].remove("public_external_write")
        errors = validate_constitution(data, text)
        self.assertTrue(any("public_external_write" in error for error in errors))

    def test_missing_ambiguity_default_fails_before_rendering(self):
        data, text = load_constitution(ROOT / "examples/sample-constitution.toml")
        del data["autonomy"]["default_on_ambiguity"]
        errors = validate_constitution(data, text)
        self.assertIn("missing clause: autonomy.default_on_ambiguity", errors)

    def test_private_material_is_flagged(self):
        data, text = load_constitution(ROOT / "examples/sample-constitution.toml")
        sensitive = "pass" + "word=not-a-real-secret"
        errors = validate_constitution(data, text + "\n" + sensitive)
        self.assertTrue(any("credential" in error for error in errors))

    def test_init_creates_complete_workshop(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "constitution"
            init_workspace(destination, "Avery", "Compass")
            expected = {"constitution.toml", "discovery.md", "stress-tests.json", "RATIFICATION.md", "CHANGELOG.md"}
            self.assertEqual({path.name for path in destination.iterdir()}, expected)
            data, text = load_constitution(destination / "constitution.toml")
            scenarios = load_scenarios(destination / "stress-tests.json")
            self.assertEqual(validate_constitution(data, text, allow_draft=True, scenarios=scenarios), [])

    def test_packaged_templates_match_public_templates(self):
        packaged = files("user_machine_constitution").joinpath("templates")
        for name in (
            "constitution-template.toml", "discovery-questionnaire.md",
            "stress-tests.json", "ratification-checklist.md",
        ):
            self.assertEqual(
                packaged.joinpath(name).read_text(),
                (ROOT / "templates" / name).read_text(),
            )


if __name__ == "__main__":
    unittest.main()
