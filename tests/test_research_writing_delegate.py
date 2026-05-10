from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "research-writing-delegate" / "scripts" / "call_delegate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("call_delegate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ResearchWritingDelegateTests(unittest.TestCase):
    def test_dry_run_defaults_to_openrouter_and_uses_structured_output(self) -> None:
        brief = {
            "task": {"type": "rewrite", "target": "paragraph", "goal": "tighten the mechanism"},
            "constraints": ["do not add citations", "do not claim empirical validation"],
        }
        with tempfile.TemporaryDirectory() as tmp:
            brief_path = Path(tmp) / "brief.json"
            brief_path.write_text(json.dumps(brief), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--brief",
                    str(brief_path),
                    "--model",
                    "test-model",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
                env={},
            )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["provider"], "openrouter")
        self.assertEqual(payload["model"], "test-model")
        self.assertEqual(payload["endpoint"], "https://openrouter.ai/api/v1/chat/completions")
        self.assertEqual(payload["request"]["response_format"]["type"], "json_schema")
        self.assertEqual(
            payload["request"]["response_format"]["json_schema"]["name"],
            "research_writing_delegate_output",
        )
        self.assertTrue(payload["request"]["provider"]["require_parameters"])
        self.assertEqual(payload["request"]["messages"][0]["role"], "system")
        self.assertIn("Task modes", payload["request"]["messages"][0]["content"])
        self.assertIn("paper owner", payload["request"]["messages"][0]["content"])
        self.assertNotIn("Authorization", result.stdout)
        self.assertNotIn("OPENROUTER_API_KEY=", result.stdout)

    def test_openai_provider_still_uses_responses_api_structured_output(self) -> None:
        brief = {"task": {"type": "rewrite", "target": "paragraph", "goal": "tighten"}}
        with tempfile.TemporaryDirectory() as tmp:
            brief_path = Path(tmp) / "brief.json"
            brief_path.write_text(json.dumps(brief), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--provider",
                    "openai",
                    "--brief",
                    str(brief_path),
                    "--model",
                    "gpt-test",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
                env={},
            )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["provider"], "openai")
        self.assertEqual(payload["endpoint"], "https://api.openai.com/v1/responses")
        self.assertEqual(payload["request"]["text"]["format"]["type"], "json_schema")
        self.assertEqual(payload["request"]["text"]["format"]["name"], "research_writing_delegate_output")

    def test_env_file_loader_preserves_existing_environment_values(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            env_path = Path(tmp) / ".env"
            env_path.write_text(
                "OPENROUTER_API_KEY=from-file\nRESEARCH_WRITING_DELEGATE_MODEL='writer-model'\n",
                encoding="utf-8",
            )
            environ = {"OPENROUTER_API_KEY": "already-set"}
            module.load_env_file(env_path, environ)

        self.assertEqual(environ["OPENROUTER_API_KEY"], "already-set")
        self.assertEqual(environ["RESEARCH_WRITING_DELEGATE_MODEL"], "writer-model")

    def test_invalid_brief_fails_before_dry_run(self) -> None:
        brief = {"task": {"type": "rewrite", "target": "paragraph"}}
        with tempfile.TemporaryDirectory() as tmp:
            brief_path = Path(tmp) / "brief.json"
            brief_path.write_text(json.dumps(brief), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--brief",
                    str(brief_path),
                    "--dry-run",
                ],
                capture_output=True,
                text=True,
                env={},
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Brief validation failed", result.stderr)
        self.assertIn("task.goal", result.stderr)

    def test_initial_brief_rejects_feedback_payloads(self) -> None:
        brief = {
            "task": {"type": "rewrite", "target": "paragraph", "goal": "tighten"},
            "feedback": {"requested_changes": ["shorter"], "user_approved": True},
        }
        with tempfile.TemporaryDirectory() as tmp:
            brief_path = Path(tmp) / "brief.json"
            brief_path.write_text(json.dumps(brief), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--brief",
                    str(brief_path),
                    "--dry-run",
                ],
                capture_output=True,
                text=True,
                env={},
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("feedback is only valid with --brief-kind revision", result.stderr)

    def test_revision_brief_requires_user_approval(self) -> None:
        brief = {
            "task": {"type": "rewrite", "target": "paragraph", "goal": "tighten"},
            "feedback": {
                "previous_draft": "Draft.",
                "codex_review": {"recommendation": "regenerate"},
                "requested_changes": ["remove overclaiming"],
                "user_approved": False,
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            brief_path = Path(tmp) / "brief.json"
            brief_path.write_text(json.dumps(brief), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--brief-kind",
                    "revision",
                    "--brief",
                    str(brief_path),
                    "--dry-run",
                ],
                capture_output=True,
                text=True,
                env={},
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("feedback.user_approved must be true", result.stderr)

    def test_review_and_revision_templates_include_required_surfaces(self) -> None:
        template_dir = REPO_ROOT / "skills" / "research-writing-delegate" / "templates"
        brief_template = json.loads((template_dir / "minimal_brief.json").read_text(encoding="utf-8"))
        review_template = (template_dir / "review.md").read_text(encoding="utf-8")
        revision_schema = json.loads((template_dir / "revision_brief.schema.json").read_text(encoding="utf-8"))

        self.assertIn("may_make", brief_template["claims"])
        self.assertIn("must_not_make", brief_template["claims"])
        self.assertIn("sources", brief_template)
        for expected in [
            "Recommendation",
            "Claim Fit",
            "Source Fit",
            "Citation Risk",
            "Style fit",
            "Overclaiming",
            "Proposed Revision Brief",
            "User Approval",
        ]:
            self.assertIn(expected, review_template)
        self.assertIn("feedback", revision_schema["required"])
        self.assertTrue(revision_schema["properties"]["feedback"]["properties"]["user_approved"]["const"])

    def test_extracts_openrouter_chat_completion_content(self) -> None:
        module = load_module()
        response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "draft": "Draft.",
                                "claims_used": [],
                                "assumptions": [],
                                "citation_needs": [],
                                "weak_points": [],
                                "revision_notes": [],
                                "risk_flags": [],
                            }
                        )
                    }
                }
            ]
        }
        self.assertIn('"draft": "Draft."', module.extract_output_text(response, "openrouter"))


if __name__ == "__main__":
    unittest.main()
