from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_repository import RepositoryValidator  # noqa: E402


def write_registry(root: Path, names: list[str]) -> None:
    skills_root = root / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    entries = []
    for name in names:
        skill_dir = skills_root / name
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: " + name + "\n---\n", encoding="utf-8")
        entries.append(
            {
                "name": name,
                "status": "active",
                "version": "0.4.0",
                "scope": "global",
                "allow_implicit_invocation": True,
                "minimum_eval_cases": 5,
            }
        )
    (skills_root / "registry.yaml").write_text(
        yaml.safe_dump({"schema_version": "1", "skills": entries}, sort_keys=False),
        encoding="utf-8",
    )


class RegistryDrivenSkillCountTest(unittest.TestCase):
    def test_matching_thirteen_skill_set_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            names = [f"skill-{index:02d}" for index in range(13)]
            write_registry(root, names)
            validator = RepositoryValidator(root)
            validator.version = "0.4.0"

            validator.validate_publication_registry()

            self.assertEqual([], validator.errors)
            self.assertEqual(sorted(names), validator.active)
            self.assertEqual(sorted(names), validator.discovered)

    def test_empty_active_set_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "skills"
            skills_root.mkdir(parents=True)
            (skills_root / "registry.yaml").write_text(
                yaml.safe_dump({"schema_version": "1", "skills": []}, sort_keys=False),
                encoding="utf-8",
            )
            validator = RepositoryValidator(root)
            validator.version = "0.4.0"

            validator.validate_publication_registry()

            self.assertIn(
                "skills/registry.yaml must publish at least one active Skill",
                validator.errors,
            )


if __name__ == "__main__":
    unittest.main()
