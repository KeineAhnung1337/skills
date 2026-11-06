"""Exercise path rendering, specialist boundaries, and config replacement safeguards."""

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))

from install import render, write_config
from verify_setup import permission, validate


class TeamInstallationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="opencode-team-tests-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "skills with spaces"
        self.approved = json.loads((PACKAGE / "skills.json").read_text(encoding="utf-8"))
        for relative in self.approved.values():
            folder = self.root / relative
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "SKILL.md").write_text("Synthetic skill fixture.\n", encoding="utf-8")

    def test_rendered_config_routes_skills_and_preserves_worker_boundaries(self):
        config = render(self.root)
        validate(config)
        self.assertNotIn("{env:OPENCODE_SKILLS_DIR}", json.dumps(config))
        self.assertEqual(
            config["providers"]["bosys"]["settings"]["apiKey"],
            "{env:LLM_API_KEY_BOSYS}",
        )
        for name, agent in config["agents"].items():
            for skill_id, relative in self.approved.items():
                folder = (self.root / relative).as_posix()
                self.assertEqual(permission(config, agent, "skill", skill_id), "allow")
                self.assertEqual(permission(config, agent, "external_directory", folder + "/*"), "allow")
                self.assertEqual(permission(config, agent, "read", folder + "/references/index.md"), "allow")
                self.assertEqual(permission(config, agent, "edit", folder + "/references/index.md"), "deny")
            self.assertEqual(permission(config, agent, "skill", "unapproved-fixture"), "deny")
            if agent["mode"] == "subagent":
                self.assertEqual(permission(config, agent, "external_directory", "/unrelated/private/*"), "deny")
                self.assertEqual(permission(config, agent, "subagent", "explorer"), "deny")
            if name in ("explorer", "debugger", "reviewer", "security-reviewer"):
                self.assertEqual(permission(config, agent, "shell", "git status"), "deny")

    def test_missing_skill_entry_point_is_rejected_before_installation(self):
        (self.root / "qftest" / "SKILL.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing skill entry"):
            render(self.root)

    def test_new_config_is_written_with_target_paths(self):
        destination = self.base / "target config" / "opencode.jsonc"
        config = render(self.root)
        target, backup = write_config(config, destination)
        self.assertEqual(target, destination)
        self.assertIsNone(backup)
        self.assertEqual(json.loads(target.read_text(encoding="utf-8")), config)

    def test_existing_config_is_preserved_without_explicit_replacement(self):
        destination = self.base / "opencode.jsonc"
        original = '// User settings\n{"custom": "preserve me"}\n'
        destination.write_text(original, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "already exists"):
            write_config(render(self.root), destination)
        self.assertEqual(destination.read_text(encoding="utf-8"), original)
        self.assertEqual(list(self.base.glob("*.bak-*")), [])

    def test_replacement_preserves_exact_previous_bytes_in_backup(self):
        destination = self.base / "opencode.jsonc"
        original = b'// Original JSONC with comments\r\n{"custom": 3,}\r\n'
        destination.write_bytes(original)
        config = render(self.root)
        target, backup = write_config(config, destination, replace_existing=True)
        self.assertEqual(backup.read_bytes(), original)
        self.assertEqual(json.loads(target.read_text(encoding="utf-8")), config)

    def test_failed_atomic_replacement_leaves_existing_config_intact(self):
        destination = self.base / "opencode.jsonc"
        original = b'{"custom": "keep"}\n'
        destination.write_bytes(original)
        with patch("install.os.replace", side_effect=PermissionError("synthetic failure")):
            with self.assertRaises(PermissionError):
                write_config(render(self.root), destination, replace_existing=True)
        self.assertEqual(destination.read_bytes(), original)
        self.assertEqual(list(self.base.glob(".opencode-team-*")), [])
        self.assertEqual(len(list(self.base.glob("*.bak-*"))), 1)

    def test_alternate_json_config_is_not_silently_shadowed(self):
        alternate = self.base / "opencode.json"
        alternate.write_text("{}", encoding="utf-8")
        destination = self.base / "opencode.jsonc"
        with self.assertRaisesRegex(ValueError, "Alternate config"):
            write_config(render(self.root), destination)
        self.assertFalse(destination.exists())
        self.assertEqual(alternate.read_text(encoding="utf-8"), "{}")

    def test_portable_source_template_cannot_be_overwritten(self):
        with self.assertRaisesRegex(ValueError, "portable source"):
            write_config(render(self.root), PACKAGE / "opencode.jsonc", replace_existing=True)

    def test_symlinked_config_destination_is_not_replaced(self):
        original = self.base / "existing.jsonc"
        original.write_text("{}", encoding="utf-8")
        link = self.base / "opencode.jsonc"
        try:
            link.symlink_to(original)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation is unavailable on this host.")
        with self.assertRaisesRegex(ValueError, "symlink"):
            write_config(render(self.root), link, replace_existing=True)
        self.assertTrue(link.is_symlink())
        self.assertEqual(original.read_text(encoding="utf-8"), "{}")


if __name__ == "__main__":
    unittest.main()
