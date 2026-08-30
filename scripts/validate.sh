#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd -P)"
PYTHON_BIN="${AGENT_SKILLS_PYTHON:-$ROOT_DIR/.venv/bin/python3}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="python3"
fi
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  printf 'ERROR: Python executable not found: %s\n' "$PYTHON_BIN" >&2
  exit 1
fi
if ! "$PYTHON_BIN" -c 'import yaml, jsonschema' >/dev/null 2>&1; then
  printf 'ERROR: install PyYAML>=6,<7 and jsonschema>=4,<5 before validation.\n' >&2
  exit 1
fi

STANDARDS_VALIDATOR="${AGENT_SKILLS_STANDARDS_VALIDATOR:-}"
if [[ -z "$STANDARDS_VALIDATOR" && -x "$ROOT_DIR/.venv/bin/skills-ref" ]]; then
  STANDARDS_VALIDATOR="$ROOT_DIR/.venv/bin/skills-ref"
fi
if [[ -z "$STANDARDS_VALIDATOR" && -x "$ROOT_DIR/.venv/bin/agentskills" ]]; then
  STANDARDS_VALIDATOR="$ROOT_DIR/.venv/bin/agentskills"
fi
if [[ -z "$STANDARDS_VALIDATOR" ]] && command -v skills-ref >/dev/null 2>&1; then
  STANDARDS_VALIDATOR="$(command -v skills-ref)"
fi
if [[ -z "$STANDARDS_VALIDATOR" ]] && command -v agentskills >/dev/null 2>&1; then
  STANDARDS_VALIDATOR="$(command -v agentskills)"
fi
if [[ -z "$STANDARDS_VALIDATOR" ]]; then
  printf 'ERROR: skills-ref/agentskills is required; install the Agent Skills reference validator or set AGENT_SKILLS_STANDARDS_VALIDATOR.\n' >&2
  exit 1
fi

"$PYTHON_BIN" "$ROOT_DIR/scripts/validate_repository.py" "$ROOT_DIR"
"$PYTHON_BIN" -m unittest discover -s "$ROOT_DIR/tests" -p 'test_*.py'

published_output="$("$PYTHON_BIN" "$ROOT_DIR/scripts/skill-set.py" --mode published)"
SKILLS=()
while IFS= read -r skill; do
  [[ -n "$skill" ]] && SKILLS+=("$skill")
done <<< "$published_output"

for skill in "${SKILLS[@]}"; do
  "$STANDARDS_VALIDATOR" validate "$ROOT_DIR/skills/$skill"
done

FIXTURE_SKILL_DIR="$ROOT_DIR/tests/fixtures/knowledge-compilation/generated-skill"
"$STANDARDS_VALIDATOR" validate "$FIXTURE_SKILL_DIR"

QUICK_VALIDATOR="${AGENT_SKILLS_QUICK_VALIDATOR:-${AGENT_SKILLS_VALIDATOR:-}}"
DEFAULT_QUICK_VALIDATOR="${HOME:?HOME must be set}/.codex/skills/.system/skill-creator/scripts/quick_validate.py"
if [[ -z "$QUICK_VALIDATOR" && -f "$DEFAULT_QUICK_VALIDATOR" ]]; then
  QUICK_VALIDATOR="$DEFAULT_QUICK_VALIDATOR"
fi
if [[ -n "$QUICK_VALIDATOR" && -f "$QUICK_VALIDATOR" ]]; then
  for skill in "${SKILLS[@]}"; do
    "$PYTHON_BIN" "$QUICK_VALIDATOR" "$ROOT_DIR/skills/$skill"
  done
else
  printf 'WARN: supplemental skill-creator validator not found; skills-ref remains the standards validator.\n' >&2
fi

if ! git -C "$ROOT_DIR" diff --check; then
  printf 'ERROR: git diff --check failed.\n' >&2
  exit 1
fi

printf 'Agent Skills standards validation passed for %d published Skills.\n' "${#SKILLS[@]}"
