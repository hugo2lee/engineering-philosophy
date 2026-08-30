#!/usr/bin/env python3
"""Repository-specific validation for the engineering-philosophy Skill Suite.

The Agent Skills reference validator checks the public SKILL.md contract.  This
validator checks the repository contract around publication, routing, lifecycle
evals, knowledge records, provenance, and release evidence.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml
from jsonschema import Draft202012Validator, ValidationError


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LANGUAGES = {"zh", "en", "mixed"}
SKILL_STATUSES = {"active", "candidate", "deprecated", "archived"}
SCOPES = {"project", "organization", "global"}
OLD_SKILL_NAMES = {"spec-driven-development", "planning-and-task-breakdown"}
REQUIRED_KLC_CATEGORIES = {
    "artifact-classification",
    "generated-artifact",
    "existing-owner",
    "candidate-gate",
    "provenance",
    "redaction",
    "scope",
    "conflict",
    "retirement",
    "registry",
    "write-boundary",
    "architecture-routing",
    "domain-routing",
    "eval-gate",
    "global-promotion",
    "compiler-ci",
    "duplicate-prevention",
    "frontmatter-spec",
}


class RepositoryValidator:
    def __init__(self, root: Path):
        self.root = root
        self.errors: list[str] = []
        self.eval_ids: dict[str, str] = {}
        self.discovered: list[str] = []
        self.active: list[str] = []
        self.registry_by_name: dict[str, dict] = {}
        self.version = ""

    def error(self, message: str) -> None:
        self.errors.append(message)

    def load_yaml(self, path: Path):
        try:
            return yaml.safe_load(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            self.error(f"missing YAML file: {path.relative_to(self.root)}")
        except yaml.YAMLError as exc:
            self.error(f"{path.relative_to(self.root)}: invalid YAML: {exc}")
        except OSError as exc:
            self.error(f"{path.relative_to(self.root)}: cannot read: {exc}")
        return None

    def frontmatter(self, path: Path) -> dict:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            self.error(f"{path.relative_to(self.root)}: cannot read: {exc}")
            return {}
        if len(lines) < 3 or lines[0].strip() != "---":
            self.error(f"{path.relative_to(self.root)}: missing YAML frontmatter")
            return {}
        try:
            end = lines.index("---", 1)
        except ValueError:
            self.error(f"{path.relative_to(self.root)}: frontmatter is not closed")
            return {}
        try:
            value = yaml.safe_load("\n".join(lines[1:end])) or {}
        except yaml.YAMLError as exc:
            self.error(f"{path.relative_to(self.root)}: invalid frontmatter: {exc}")
            return {}
        if not isinstance(value, dict):
            self.error(f"{path.relative_to(self.root)}: frontmatter must be a mapping")
            return {}
        return value

    def check_links(self, directory: Path) -> None:
        link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
        for markdown in directory.rglob("*.md"):
            try:
                text = markdown.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                self.error(f"{markdown.relative_to(self.root)}: cannot read: {exc}")
                continue
            for raw_target in link_pattern.findall(text):
                target = raw_target.strip().split("#", 1)[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                target_path = (markdown.parent / unquote(target)).resolve()
                if not target_path.exists():
                    self.error(
                        f"{markdown.relative_to(self.root)}: broken reference link {raw_target}"
                    )

    def validate_skill_list(self, values, case_id: str, field: str) -> None:
        if not isinstance(values, list) or not all(
            isinstance(value, str) for value in values
        ):
            self.error(f"{case_id}: {field} must be a list of Skill names")
            return
        unknown = [value for value in values if value not in self.registry_by_name]
        if unknown:
            self.error(f"{case_id}: {field} contains unknown Skills {unknown}")

    def register_eval_id(self, case_id: str, source: str) -> None:
        previous = self.eval_ids.get(case_id)
        if previous is not None:
            self.error(f"duplicate eval case ID {case_id}: {previous} and {source}")
        else:
            self.eval_ids[case_id] = source

    def validate_markdown_evals(self, skill: str, minimum: int) -> None:
        cases_path = self.root / "evals" / skill / "cases.md"
        expected_path = self.root / "evals" / skill / "expected.md"
        if not cases_path.exists():
            self.error(f"{skill} is missing evals/{skill}/cases.md")
            return
        if not expected_path.exists():
            self.error(f"{skill} is missing evals/{skill}/expected.md")
            return
        heading_pattern = re.compile(r"^##\s+([A-Z]+-\d+)\b", re.MULTILINE)
        cases = heading_pattern.findall(cases_path.read_text(encoding="utf-8"))
        expected = heading_pattern.findall(expected_path.read_text(encoding="utf-8"))
        if len(cases) != len(set(cases)):
            self.error(f"{skill}: duplicate case ID in cases.md")
        if len(expected) != len(set(expected)):
            self.error(f"{skill}: duplicate case ID in expected.md")
        if set(cases) != set(expected):
            self.error(f"{skill}: cases.md and expected.md IDs differ")
        for case_id in cases:
            self.register_eval_id(case_id, f"evals/{skill}/cases.md")
        if len(cases) < minimum:
            self.error(f"{skill}: expected at least {minimum} eval cases, found {len(cases)}")

    def validate_publication_registry(self) -> None:
        skills_root = self.root / "skills"
        self.discovered = sorted(
            path.parent.name for path in skills_root.glob("*/SKILL.md")
        )
        registry_path = skills_root / "registry.yaml"
        data = self.load_yaml(registry_path)
        if not isinstance(data, dict):
            return
        if data.get("schema_version") != "1":
            self.error("skills/registry.yaml must declare schema_version 1")
        entries = data.get("skills")
        if not isinstance(entries, list):
            self.error("skills/registry.yaml: skills must be a list")
            return
        for entry in entries:
            if not isinstance(entry, dict):
                self.error("skills/registry.yaml: every Skill entry must be a mapping")
                continue
            name = entry.get("name")
            if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
                self.error(f"skills/registry.yaml: invalid Skill name {name!r}")
                continue
            if name in self.registry_by_name:
                self.error(f"skills/registry.yaml: duplicate Skill name {name}")
                continue
            status = entry.get("status")
            if status not in SKILL_STATUSES:
                self.error(f"skills/registry.yaml: invalid status for {name}: {status!r}")
            if entry.get("scope") not in SCOPES:
                self.error(f"skills/registry.yaml: invalid scope for {name}: {entry.get('scope')!r}")
            if str(entry.get("version")) != self.version:
                self.error(f"skills/registry.yaml: {name} version must be {self.version}")
            if not isinstance(entry.get("allow_implicit_invocation"), bool):
                self.error(f"skills/registry.yaml: {name} allow_implicit_invocation must be boolean")
            if not isinstance(entry.get("minimum_eval_cases"), int) or entry["minimum_eval_cases"] < 5:
                self.error(f"skills/registry.yaml: {name} minimum_eval_cases must be an integer >= 5")
            self.registry_by_name[name] = entry
        self.active = sorted(
            name for name, entry in self.registry_by_name.items() if entry.get("status") == "active"
        )
        if self.discovered != self.active:
            self.error(
                "discovered Skill set does not equal active registry Skill set: "
                f"discovered={self.discovered!r}, active={self.active!r}"
            )
        if not self.active:
            self.error("skills/registry.yaml must publish at least one active Skill")

    def validate_skills(self) -> None:
        for skill in self.active:
            skill_dir = self.root / "skills" / skill
            skill_md = skill_dir / "SKILL.md"
            metadata_path = skill_dir / "agents" / "openai.yaml"
            if not skill_dir.is_dir():
                self.error(f"missing Skill directory: {skill}")
                continue
            if not skill_md.exists():
                self.error(f"{skill} is missing SKILL.md")
            if not metadata_path.exists():
                self.error(f"{skill} is missing agents/openai.yaml")
            eval_dir = self.root / "evals" / skill
            if not eval_dir.is_dir():
                self.error(f"{skill} is missing evals/{skill}")
            if skill_md.exists():
                properties = self.frontmatter(skill_md)
                if properties.get("name") != skill:
                    self.error(f"{skill}: frontmatter name does not match directory")
                description = properties.get("description")
                if not isinstance(description, str) or not description.strip():
                    self.error(f"{skill}: description is empty")
                elif len(description) > 1024:
                    self.error(f"{skill}: description exceeds 1024 characters")
                metadata = properties.get("metadata")
                if not isinstance(metadata, dict) or str(metadata.get("version")) != self.version:
                    self.error(f"{skill}: metadata.version must be {self.version}")
                text = skill_md.read_text(encoding="utf-8")
                if "[TODO:" in text:
                    self.error(f"{skill}: contains an unfinished TODO")
                self.check_links(skill_dir)
            if metadata_path.exists():
                metadata = self.load_yaml(metadata_path)
                if not isinstance(metadata, dict):
                    continue
                interface = metadata.get("interface", {})
                policy = metadata.get("policy", {})
                if not isinstance(interface, dict):
                    self.error(f"{skill}: agents/openai.yaml interface must be a mapping")
                else:
                    for field in ("display_name", "short_description", "default_prompt"):
                        if not isinstance(interface.get(field), str) or not interface[field].strip():
                            self.error(f"{skill}: metadata interface.{field} is missing")
                    short_description = interface.get("short_description", "")
                    if not 25 <= len(short_description) <= 64:
                        self.error(f"{skill}: short_description must be 25-64 characters")
                    if f"${skill}" not in interface.get("default_prompt", ""):
                        self.error(f"{skill}: default_prompt must mention ${skill}")
                expected_policy = self.registry_by_name.get(skill, {}).get("allow_implicit_invocation")
                if not isinstance(policy, dict) or policy.get("allow_implicit_invocation") is not expected_policy:
                    self.error(f"{skill}: allow_implicit_invocation must match skills/registry.yaml")
            minimum = self.registry_by_name.get(skill, {}).get("minimum_eval_cases", 5)
            self.validate_markdown_evals(skill, minimum)

    def validate_specialist_evals(self) -> None:
        requirements = {
            "requirement-engineering": ("REQ-", "# Requirement Engineering Cases", "Spec-Driven Development"),
            "change-planning": ("CHG-", "# Change Planning Cases", "Planning and Task Breakdown"),
        }
        for skill, (prefix, title, forbidden_title) in requirements.items():
            cases_path = self.root / "evals" / skill / "cases.md"
            expected_path = self.root / "evals" / skill / "expected.md"
            if not cases_path.exists() or not expected_path.exists():
                continue
            cases_text = cases_path.read_text(encoding="utf-8")
            expected_text = expected_path.read_text(encoding="utf-8")
            if not cases_text.splitlines() or cases_text.splitlines()[0].strip() != title:
                self.error(f"{skill}: cases.md must use semantic title {title!r}")
            expected_title = f"# {skill.replace('-', ' ').title()} Expected Outcomes"
            if not expected_text.splitlines() or expected_text.splitlines()[0].strip() != expected_title:
                self.error(f"{skill}: expected.md has the wrong semantic title")
            if forbidden_title in cases_text or forbidden_title in expected_text:
                self.error(f"{skill}: stale migrated eval title remains: {forbidden_title}")
            ids = re.findall(r"^##\s+([A-Z]+-\d+)\b", cases_text, re.MULTILINE)
            if any(not case_id.startswith(prefix) for case_id in ids):
                self.error(f"{skill}: eval IDs must use {prefix} prefix")
            if len(ids) < 8:
                self.error(f"{skill}: semantic specialist evals require at least 8 cases")

    def validate_structured_eval_file(
        self,
        path: Path,
        source_name: str,
        id_pattern: str | None,
        minimum: int,
        required_categories: set[str] | None = None,
    ) -> list[dict]:
        data = self.load_yaml(path)
        if not isinstance(data, list):
            self.error(f"{source_name}: top level must be a list")
            return []
        required = {
            "id", "category", "language", "prompt", "context", "expected_primary",
            "allowed_secondary", "expected_decisions", "forbidden", "acceptance",
        }
        seen: set[str] = set()
        categories: set[str] = set()
        for case in data:
            if not isinstance(case, dict):
                self.error(f"{source_name}: every case must be a mapping")
                continue
            case_id = case.get("id", "<unknown>")
            missing = required - set(case)
            if missing:
                self.error(f"{source_name} case {case_id}: missing {sorted(missing)}")
                continue
            if case_id in seen:
                self.error(f"{source_name}: duplicate case ID {case_id}")
            seen.add(case_id)
            self.register_eval_id(case_id, source_name)
            if id_pattern and (not isinstance(case_id, str) or not re.fullmatch(id_pattern, case_id)):
                self.error(f"{source_name} case {case_id}: ID has invalid format")
            category = case.get("category")
            if not isinstance(category, str) or not category.strip():
                self.error(f"{source_name} case {case_id}: category must be non-empty")
            else:
                categories.add(category)
            if case.get("language") not in LANGUAGES:
                self.error(f"{source_name} case {case_id}: language must be zh, en, or mixed")
            for field in ("prompt", "context", "acceptance"):
                if not isinstance(case.get(field), str) or not case[field].strip():
                    self.error(f"{source_name} case {case_id}: {field} must be non-empty")
            primary = case.get("expected_primary")
            if not isinstance(primary, str) or primary not in self.registry_by_name:
                self.error(f"{source_name} case {case_id}: expected_primary must be one Skill name")
            self.validate_skill_list(case.get("allowed_secondary"), case_id, "allowed_secondary")
            self.validate_skill_list(case.get("forbidden"), case_id, "forbidden")
            if primary in (case.get("forbidden") or []):
                self.error(f"{source_name} case {case_id}: expected primary is also forbidden")
            decisions = case.get("expected_decisions")
            if not isinstance(decisions, list) or not decisions or not all(
                isinstance(value, str) and value.strip() for value in decisions
            ):
                self.error(f"{source_name} case {case_id}: expected_decisions must be non-empty strings")
        if len(data) < minimum:
            self.error(f"{source_name}: expected at least {minimum} cases, found {len(data)}")
        if required_categories:
            missing_categories = required_categories - categories
            if missing_categories:
                self.error(f"{source_name}: missing required categories {sorted(missing_categories)}")
        return data

    def validate_routing(self) -> None:
        path = self.root / "evals" / "routing" / "cases.yaml"
        cases = self.load_yaml(path)
        if not isinstance(cases, list):
            self.error("evals/routing/cases.yaml: top level must be a list")
            return
        required = {"id", "language", "prompt", "expected_primary", "allowed_secondary", "forbidden"}
        seen: set[str] = set()
        counts = {language: 0 for language in LANGUAGES}
        by_id: dict[str, dict] = {}
        for case in cases:
            if not isinstance(case, dict):
                self.error("routing: every case must be a mapping")
                continue
            case_id = case.get("id", "<unknown>")
            missing = required - set(case)
            if missing:
                self.error(f"routing case {case_id}: missing {sorted(missing)}")
                continue
            if case_id in seen:
                self.error(f"routing: duplicate case ID {case_id}")
            seen.add(case_id)
            self.register_eval_id(case_id, "evals/routing/cases.yaml")
            by_id[case_id] = case
            language = case["language"]
            if language not in LANGUAGES:
                self.error(f"routing case {case_id}: invalid language")
            else:
                counts[language] += 1
            if not isinstance(case["prompt"], str) or not case["prompt"].strip():
                self.error(f"routing case {case_id}: prompt must be non-empty")
            self.validate_skill_list(case["expected_primary"], case_id, "expected_primary")
            self.validate_skill_list(case["allowed_secondary"], case_id, "allowed_secondary")
            self.validate_skill_list(case["forbidden"], case_id, "forbidden")
            if any(value in case["forbidden"] for value in case["expected_primary"]):
                self.error(f"routing case {case_id}: expected primary is also forbidden")
            prompt = case["prompt"]
            has_cjk = bool(re.search(r"[\u3400-\u9fff]", prompt))
            has_latin = bool(re.search(r"[A-Za-z]", prompt))
            if language == "zh" and not has_cjk:
                self.error(f"routing case {case_id}: zh case has no CJK text")
            if language == "en" and has_cjk:
                self.error(f"routing case {case_id}: en case contains CJK text")
            if language == "mixed" and not (has_cjk and has_latin):
                self.error(f"routing case {case_id}: mixed case needs CJK and Latin text")
        if len(cases) < 30:
            self.error(f"routing: expected at least 30 cases, found {len(cases)}")
        for language, minimum in (("zh", 12), ("en", 12), ("mixed", 6)):
            if counts[language] < minimum:
                self.error(f"routing: expected at least {minimum} {language} cases, found {counts[language]}")
        negative_requirements = {
            "ROUTE-ZH-001": "ddd-lite",
            "ROUTE-EN-013": "ddd-lite",
            "ROUTE-ZH-003": "architecture-boundaries",
            "ROUTE-EN-015": "architecture-boundaries",
            "ROUTE-ZH-004": "change-planning",
            "ROUTE-EN-017": "requirement-engineering",
            "ROUTE-ZH-005": "incremental-implementation",
            "ROUTE-ZH-006": "change-planning",
            "ROUTE-EN-018": "change-planning",
            "ROUTE-ZH-007": "code-review-and-quality",
            "ROUTE-EN-019": "code-review-and-quality",
            "ROUTE-EN-020": "systematic-debugging",
            "ROUTE-ZH-009": "ci-cd-and-automation",
            "ROUTE-EN-022": "git-workflow-and-versioning",
        }
        for case_id, skill in negative_requirements.items():
            if case_id not in by_id:
                self.error(f"routing: required negative case is missing: {case_id}")
            elif skill not in by_id[case_id].get("forbidden", []):
                self.error(f"routing case {case_id}: must forbid {skill}")

    def validate_knowledge_schemas(self) -> None:
        schemas_dir = self.root / "schemas"
        schema_paths = {
            "knowledge registry": schemas_dir / "knowledge-registry.schema.yaml",
            "generated Skill record": schemas_dir / "generated-skill-record.schema.yaml",
        }
        schemas: dict[str, dict] = {}
        for label, path in schema_paths.items():
            data = self.load_yaml(path)
            if not isinstance(data, dict):
                continue
            try:
                Draft202012Validator.check_schema(data)
            except Exception as exc:  # jsonschema exposes several schema errors
                self.error(f"{path.relative_to(self.root)}: invalid Draft 2020-12 schema: {exc}")
            else:
                schemas[label] = data

        registry_schema = schemas.get("knowledge registry")
        registry_fixture = self.root / "tests/fixtures/knowledge-compilation/valid-knowledge-registry.yaml"
        if registry_schema:
            artifact_schema = registry_schema.get("$defs", {}).get("artifact", {})
            artifact_properties = artifact_schema.get("properties", {})
            artifact_required = set(artifact_schema.get("required", []))
            if not isinstance(artifact_properties, dict):
                self.error("knowledge-registry schema artifact properties must be an object")
            else:
                if "ownership" in artifact_properties:
                    self.error("knowledge-registry schema must not duplicate owner/scope in ownership")
                for field in ("owner", "scope"):
                    if field not in artifact_properties or field not in artifact_required:
                        self.error(f"knowledge-registry schema must require top-level {field}")

        if registry_schema:
            instance = self.load_yaml(registry_fixture)
            if instance is not None:
                self.assert_valid(registry_schema, instance, registry_fixture)
        record_schema = schemas.get("generated Skill record")
        if record_schema:
            record_properties = record_schema.get("properties", {})
            if not isinstance(record_properties, dict) or "ownership" not in record_properties:
                self.error("generated Skill record schema must retain structured ownership")
        record_fixture = self.root / "tests/fixtures/knowledge-compilation/valid-generated-skill-record.yaml"
        if record_schema:
            instance = self.load_yaml(record_fixture)
            if instance is not None:
                self.assert_valid(record_schema, instance, record_fixture)
            invalid_path = self.root / "tests/fixtures/knowledge-compilation/invalid-generated-global-without-promotion.yaml"
            invalid = self.load_yaml(invalid_path)
            if invalid is not None:
                try:
                    Draft202012Validator(record_schema).validate(invalid)
                except ValidationError:
                    pass
                else:
                    self.error(f"{invalid_path.relative_to(self.root)} unexpectedly passes global promotion gate")

        fixture_skill = self.root / "tests/fixtures/knowledge-compilation/generated-skill"
        fixture_md = fixture_skill / "SKILL.md"
        fixture_record = fixture_skill / "knowledge.yaml"
        if not fixture_md.exists() or not fixture_record.exists():
            self.error("generated Skill fixture must contain SKILL.md and knowledge.yaml")
        else:
            properties = self.frontmatter(fixture_md)
            metadata = properties.get("metadata")
            if not isinstance(metadata, dict) or metadata.get("knowledge_record") != "knowledge.yaml":
                self.error("generated Skill fixture must link metadata.knowledge_record to knowledge.yaml")
            for key in ("provenance", "generation", "lifecycle", "ownership"):
                if key in properties:
                    self.error(f"generated Skill fixture must not put {key} in SKILL.md frontmatter")
            record = self.load_yaml(fixture_record)
            if isinstance(record, dict) and ("name" in record or "description" in record):
                self.error("generated Skill sidecar must not redefine name or description")

    def assert_valid(self, schema: dict, instance, path: Path) -> None:
        try:
            Draft202012Validator(schema).validate(instance)
        except ValidationError as exc:
            self.error(f"{path.relative_to(self.root)} failed JSON Schema validation: {exc.message}")

    def validate_docs_and_version(self) -> None:
        version_path = self.root / "VERSION"
        if not version_path.exists():
            self.error("missing root VERSION file")
        else:
            self.version = version_path.read_text(encoding="utf-8").strip()
            if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", self.version):
                self.error(f"VERSION must contain a plain MAJOR.MINOR.PATCH value: {self.version}")
        readme = self.root / "README.md"
        readme_text = readme.read_text(encoding="utf-8") if readme.exists() else ""
        if f"v{self.version}" not in readme_text:
            self.error(f"README.md must declare version v{self.version}")
        if "hugo2lee/engineering-philosophy" not in readme_text:
            self.error("README.md must document the public repository identity")
        changelog = self.root / "CHANGELOG.md"
        changelog_text = changelog.read_text(encoding="utf-8") if changelog.exists() else ""
        if f"## v{self.version} -" not in changelog_text:
            self.error(f"CHANGELOG.md must contain the v{self.version} heading")
        historical_marker = "Added the C++ boundary realization reference under `architecture-boundaries` without creating a C++ top-level Skill."
        if historical_marker not in changelog_text:
            self.error("CHANGELOG.md must preserve the released v0.2.0 C++ reference entry")
        lifecycle_documents = (
            (readme, "Release Behavior Baseline", "Change Review / Gate 3"),
            (self.root / "skills/engineering-philosophy/SKILL.md", "Release Behavior Baseline", "Change Review / Gate 3"),
            (self.root / "skills/engineering-philosophy/references/feature-change-lifecycle.md", "Release Behavior Baseline", "Change Review / Gate 3"),
        )
        order = (
            "User Request", "Requirement Clarification", "Requirement Reconciliation",
            "User Decision Gate", "Approved Requirement Contract", "Repository Analysis",
            "Business Change / Impact Analysis", "Architecture Pressure Analysis",
            "Conditional architecture-boundaries / ddd-lite routing", "Implementation Plan",
            "Incremental Implementation", "TDD / Focused Verification", "Release Behavior Baseline",
            "Change Review / Gate 3", "CI / Artifact / Release Verification / Gate 4",
            "Version / Tag / Release",
        )
        for document, baseline_marker, review_marker in lifecycle_documents:
            if not document.exists():
                self.error(f"missing lifecycle document: {document.relative_to(self.root)}")
                continue
            text = document.read_text(encoding="utf-8")
            if text.find(baseline_marker) < 0 or text.find(baseline_marker) > text.find(review_marker):
                self.error(f"{document.relative_to(self.root)} must establish baseline before Gate 3")
            positions = [text.find(marker) for marker in order]
            if any(position < 0 for position in positions):
                missing = [marker for marker, position in zip(order, positions) if position < 0]
                self.error(f"{document.relative_to(self.root)} is missing lifecycle markers {missing}")
            elif positions != sorted(positions):
                self.error(f"{document.relative_to(self.root)} lifecycle markers are out of order")
        review_skill = self.root / "skills/code-review-and-quality/SKILL.md"
        if not review_skill.exists() or "applicable Release Behavior Baselines" not in review_skill.read_text(encoding="utf-8"):
            self.error("code-review-and-quality must require applicable Release Behavior Baselines")
        record_template = self.root / "skills/engineering-philosophy/references/feature-change-record.md"
        if not record_template.exists() or "## Change Review / Gate 3" not in record_template.read_text(encoding="utf-8"):
            self.error("Feature Change Record must include a Change Review / Gate 3 section")
        tag_ref = os.environ.get("GITHUB_REF", "")
        tag_name = os.environ.get("GITHUB_REF_NAME", "")
        if tag_ref.startswith("refs/tags/") and tag_name != f"v{self.version}":
            self.error(f"GitHub tag context must be v{self.version}, found {tag_name or tag_ref}")

    def validate_lifecycle_evals(self) -> None:
        lifecycle_path = self.root / "evals/lifecycle/cases.yaml"
        self.validate_structured_eval_file(
            lifecycle_path,
            "evals/lifecycle/cases.yaml",
            None,
            30,
            {
                "requirement-clarification", "requirement-reconciliation", "repository-analysis",
                "architecture-pressure", "change-planning", "behavior-implementation",
                "service-behavior-baseline", "persistence-baseline", "outbound-baseline",
                "inbound-baseline", "regression-debugging", "review-traceability", "release-readiness",
            },
        )

    def validate_knowledge_lifecycle(self) -> None:
        path = self.root / "evals/knowledge-lifecycle/cases.yaml"
        cases = self.validate_structured_eval_file(
            path,
            "evals/knowledge-lifecycle/cases.yaml",
            r"KLC-[0-9]{3}",
            31,
            REQUIRED_KLC_CATEGORIES,
        )
        by_id = {case.get("id"): case for case in cases if isinstance(case, dict)}
        case = by_id.get("KLC-031")
        if case is None:
            self.error("knowledge lifecycle must contain KLC-031 frontmatter-spec")
        else:
            if case.get("category") != "frontmatter-spec":
                self.error("KLC-031 must use the frontmatter-spec category")
            if case.get("expected_primary") != "knowledge-compilation":
                self.error("KLC-031 must route primarily to knowledge-compilation")
            combined = " ".join(case.get("expected_decisions", []))
            if "sidecar" not in combined.lower() or "frontmatter" not in combined.lower():
                self.error("KLC-031 must require standard frontmatter and a sidecar record")

    def validate_stale_names_and_scope(self) -> None:
        allowed_stale = {
            self.root / "README.md", self.root / "CHANGELOG.md",
            self.root / "docs/migrations/v0.3.0-skill-renames.md",
            self.root / "scripts/smoke-test-npx.sh",
            self.root / "scripts/validate_repository.py",
        }
        for path in self.root.rglob("*"):
            if not path.is_file() or ".git" in path.parts or path in allowed_stale:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for old_name in OLD_SKILL_NAMES:
                if old_name in text:
                    self.error(f"{path.relative_to(self.root)} contains stale active Skill name {old_name}")

        knowledge_root = self.root / "skills/knowledge-compilation"
        scoped_files = list(knowledge_root.rglob("*")) + list((self.root / "schemas").rglob("*")) + [self.root / "skills/registry.yaml"]
        forbidden_scope_facts = ("farm-manage", "internal/", "xpack", "delivery-sync", "production MQTT")
        for path in scoped_files:
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8").lower()
            except (OSError, UnicodeDecodeError):
                continue
            for marker in forbidden_scope_facts:
                if marker.lower() in text:
                    self.error(f"{path.relative_to(self.root)} contains project-specific scope marker {marker!r}")

    def validate_protocol_contracts(self) -> None:
        candidate = self.root / "skills/knowledge-compilation/references/skill-candidate-and-promotion.md"
        candidate_text = candidate.read_text(encoding="utf-8") if candidate.exists() else ""
        for marker in ("lifecycle state, not necessarily a deployable Skill directory", "automatically discovers every", "SKILL.md", "outside the active path"):
            if marker not in candidate_text:
                self.error(f"skill-candidate-and-promotion.md is missing candidate isolation rule: {marker}")
        contract = self.root / "skills/knowledge-compilation/references/generated-knowledge-contract.md"
        contract_text = contract.read_text(encoding="utf-8") if contract.exists() else ""
        for marker in ("standard frontmatter", "sidecar", "knowledge.yaml", "must not redefine"):
            if marker.lower() not in contract_text.lower():
                self.error(f"generated-knowledge-contract.md is missing sidecar rule: {marker}")
        deploy_text = (self.root / "scripts/deploy.sh").read_text(encoding="utf-8")
        smoke_text = (self.root / "scripts/smoke-test-npx.sh").read_text(encoding="utf-8")
        if re.search(r"SKILLS=\(\s*[^)]", deploy_text):
            self.error("scripts/deploy.sh must not hard-code a Skill list")
        if "skill-set.py" not in deploy_text or "--mode published" not in deploy_text:
            self.error("scripts/deploy.sh must use the shared published Skill-set helper")
        if "skill-set.py" not in smoke_text or "--mode published" not in smoke_text:
            self.error("scripts/smoke-test-npx.sh must use the shared published Skill-set helper")
        workflow = self.root / ".github/workflows/validate.yml"
        workflow_text = workflow.read_text(encoding="utf-8") if workflow.exists() else ""
        for marker in ("PyYAML>=6,<7", "jsonschema>=4,<5", "skills-ref==0.1.1"):
            if marker not in workflow_text:
                self.error(f"CI workflow is missing validation dependency {marker}")
        checklist = self.root / "docs/release-checklist.md"
        checklist_text = checklist.read_text(encoding="utf-8") if checklist.exists() else ""
        if "git tag -a v0.3.0" in checklist_text:
            self.error("release checklist contains a stale v0.3.0 tag command")
        for marker in ("v0.1.0", "v0.2.0", "v0.2.1", "v0.3.0"):
            if marker not in checklist_text:
                self.error(f"release checklist must preserve immutable history marker {marker}")
        if "v0.4.0 <release-commit>" not in checklist_text:
            self.error("release checklist must use the generic v0.4.0 tag command")

    def run(self) -> int:
        self.validate_docs_and_version()
        self.validate_publication_registry()
        self.validate_skills()
        self.validate_specialist_evals()
        self.validate_routing()
        self.validate_lifecycle_evals()
        self.validate_knowledge_lifecycle()
        self.validate_knowledge_schemas()
        self.validate_stale_names_and_scope()
        self.validate_protocol_contracts()
        if self.errors:
            for error in self.errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print(f"DISCOVERED_SKILLS={','.join(self.discovered)}")
        print(f"ACTIVE_REGISTRY_SKILLS={','.join(self.active)}")
        print(f"PUBLISHED_SKILLS={','.join(self.active)}")
        print(f"VALIDATED_SKILLS={len(self.active)} VERSION={self.version}")
        print("SCHEMA_FIXTURES=valid-registry,valid-generated-record,invalid-global-rejected")
        print("KLC_CASES=31 REQUIRED_CATEGORIES=18")
        return 0


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <repository-root>", file=sys.stderr)
        return 2
    return RepositoryValidator(Path(sys.argv[1]).resolve()).run()


if __name__ == "__main__":
    raise SystemExit(main())
