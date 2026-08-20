from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

LINTER_PATH = Path(__file__).parents[1] / "tools" / "template_lint.py"
SPEC = importlib.util.spec_from_file_location("template_lint", LINTER_PATH)
assert SPEC is not None and SPEC.loader is not None
template_lint = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = template_lint
SPEC.loader.exec_module(template_lint)


def test_bundled_templates_pass_static_lint() -> None:
    root = Path(__file__).parents[1] / "package_data" / "prompt_resources"
    assert template_lint.lint_resource_root(root) == []


def test_linter_reports_missing_instruction_and_slot_contract_errors(tmp_path: Path) -> None:
    root = tmp_path / "prompt_resources"
    template_path = root / "templates" / "Task-T" / "v1" / "example" / "en-US" / "template.md"
    schema_path = root / "slots" / "Task-T" / "v1" / "example" / "en-US" / "slot.json"
    template_path.parent.mkdir(parents=True)
    schema_path.parent.mkdir(parents=True)
    template_path.write_text("## Task Type\nFault diagnosis\n\n{{unknown_slot}}\n", encoding="utf-8")
    schema_path.write_text(json.dumps({"type": "object", "properties": {"unused_slot": {"type": "string"}}}), encoding="utf-8")

    rules = {error.rule for error in template_lint.lint_resource_root(root)}

    assert {"instruction-required", "slot-undefined", "slot-unused"} <= rules
