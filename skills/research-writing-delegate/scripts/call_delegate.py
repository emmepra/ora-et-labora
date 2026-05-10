#!/usr/bin/env python3
"""Call an external model for bounded academic prose drafting."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_PROVIDER = "openrouter"
DEFAULT_OPENROUTER_MODEL = "openai/gpt-5.2"
DEFAULT_OPENAI_MODEL = "gpt-5.5"
SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SYSTEM_PROMPT_PATH = SKILL_DIR / "prompts" / "delegate_system.md"
ALLOWED_TASK_TYPES = {
    "draft_paragraph",
    "rewrite",
    "tighten",
    "bridge",
    "abstract",
    "critique",
    "related_work",
    "theory",
    "literature_review",
    "limits",
}

DELEGATE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "draft",
        "claims_used",
        "assumptions",
        "citation_needs",
        "weak_points",
        "revision_notes",
        "risk_flags",
    ],
    "properties": {
        "draft": {"type": "string"},
        "claims_used": {"type": "array", "items": {"type": "string"}},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "citation_needs": {"type": "array", "items": {"type": "string"}},
        "weak_points": {"type": "array", "items": {"type": "string"}},
        "revision_notes": {"type": "array", "items": {"type": "string"}},
        "risk_flags": {"type": "array", "items": {"type": "string"}},
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--provider",
        choices=["openrouter", "openai"],
        default=os.environ.get("RESEARCH_WRITING_DELEGATE_PROVIDER", DEFAULT_PROVIDER),
    )
    parser.add_argument("--brief-kind", choices=["initial", "revision"], default="initial")
    parser.add_argument("--brief", required=True, help="Path to brief JSON, or '-' for stdin.")
    parser.add_argument("--out", type=Path, help="Write artifact JSON to this path.")
    parser.add_argument("--model", default=os.environ.get("RESEARCH_WRITING_DELEGATE_MODEL"))
    parser.add_argument("--system-prompt", type=Path, default=DEFAULT_SYSTEM_PROMPT_PATH)
    parser.add_argument("--env-file", type=Path, help="Optional local untracked .env file.")
    parser.add_argument("--max-output-tokens", type=int, default=1800)
    parser.add_argument("--temperature", type=float, default=0.4)
    parser.add_argument("--openrouter-site-url", default=os.environ.get("OPENROUTER_SITE_URL"))
    parser.add_argument("--openrouter-app-name", default=os.environ.get("OPENROUTER_APP_NAME"))
    parser.add_argument("--dry-run", action="store_true", help="Print sanitized request payload without calling the API.")
    return parser.parse_args()


def load_env_file(path: Path, environ: dict[str, str] | None = None) -> None:
    target = os.environ if environ is None else environ
    if not path.exists():
        raise SystemExit(f"Env file does not exist: {path}")
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in target:
            target[key] = value


def load_brief(path_value: str) -> dict[str, Any]:
    if path_value == "-":
        text = sys.stdin.read()
    else:
        text = Path(path_value).read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Brief must be JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("Brief must be a JSON object.")
    return data


def load_system_prompt(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"System prompt file does not exist: {path}")
    prompt = path.read_text(encoding="utf-8").strip()
    if not prompt:
        raise SystemExit(f"System prompt file is empty: {path}")
    return prompt


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_string_list(value: Any, path: str, errors: list[str], *, allow_empty: bool = True) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be an array of strings.")
        return
    if not allow_empty and not value:
        errors.append(f"{path} must contain at least one string.")
        return
    for index, item in enumerate(value):
        if not _is_non_empty_string(item):
            errors.append(f"{path}[{index}] must be a non-empty string.")


def _validate_optional_text_fields(
    data: dict[str, Any],
    fields: tuple[str, ...],
    prefix: str,
    errors: list[str],
) -> None:
    for field in fields:
        if field in data and not isinstance(data[field], str):
            errors.append(f"{prefix}.{field} must be a string.")


def validate_brief(brief: dict[str, Any], brief_kind: str) -> None:
    errors: list[str] = []

    task = brief.get("task")
    if not isinstance(task, dict):
        errors.append("task must be an object.")
    else:
        task_type = task.get("type")
        if not _is_non_empty_string(task_type):
            errors.append("task.type must be a non-empty string.")
        elif task_type not in ALLOWED_TASK_TYPES:
            errors.append(f"task.type must be one of: {', '.join(sorted(ALLOWED_TASK_TYPES))}.")
        for field in ("target", "goal"):
            if not _is_non_empty_string(task.get(field)):
                errors.append(f"task.{field} must be a non-empty string.")
        if "length" in task and not isinstance(task["length"], str):
            errors.append("task.length must be a string when present.")

    context = brief.get("context")
    if context is not None:
        if not isinstance(context, dict):
            errors.append("context must be an object when present.")
        else:
            _validate_optional_text_fields(context, ("before", "current", "after"), "context", errors)
            if "outline" in context:
                _validate_string_list(context["outline"], "context.outline", errors)

    claims = brief.get("claims")
    if claims is not None:
        if not isinstance(claims, dict):
            errors.append("claims must be an object when present.")
        else:
            for field in ("may_make", "must_not_make"):
                if field in claims:
                    _validate_string_list(claims[field], f"claims.{field}", errors)

    sources = brief.get("sources")
    if sources is not None:
        if not isinstance(sources, list):
            errors.append("sources must be an array when present.")
        else:
            for index, source in enumerate(sources):
                if not isinstance(source, dict):
                    errors.append(f"sources[{index}] must be an object.")
                    continue
                for field in ("citation_key", "excerpt", "usable_for"):
                    if not _is_non_empty_string(source.get(field)):
                        errors.append(f"sources[{index}].{field} must be a non-empty string.")

    style = brief.get("style")
    if style is not None and not isinstance(style, dict):
        errors.append("style must be an object when present.")

    feedback = brief.get("feedback")
    if brief_kind == "initial":
        if feedback is not None:
            errors.append("feedback is only valid with --brief-kind revision.")
    else:
        if not isinstance(feedback, dict):
            errors.append("feedback must be an object for revision briefs.")
        else:
            if not _is_non_empty_string(feedback.get("previous_draft")):
                errors.append("feedback.previous_draft must be a non-empty string.")
            codex_review = feedback.get("codex_review")
            if not isinstance(codex_review, dict):
                errors.append("feedback.codex_review must be an object.")
            elif not _is_non_empty_string(codex_review.get("recommendation")):
                errors.append("feedback.codex_review.recommendation must be a non-empty string.")
            _validate_string_list(
                feedback.get("requested_changes"),
                "feedback.requested_changes",
                errors,
                allow_empty=False,
            )
            if feedback.get("user_approved") is not True:
                errors.append("feedback.user_approved must be true before regeneration.")

    if errors:
        raise SystemExit("Brief validation failed:\n- " + "\n- ".join(errors))


def resolve_model(provider: str, model: str | None) -> str:
    if model:
        return model
    if provider == "openrouter":
        return DEFAULT_OPENROUTER_MODEL
    return DEFAULT_OPENAI_MODEL


def build_request(
    brief: dict[str, Any],
    provider: str,
    model: str,
    system_prompt: str,
    max_output_tokens: int,
    temperature: float,
) -> dict[str, Any]:
    user_content = "Draft from this writing brief. Return JSON only.\n\n" + json.dumps(
        brief,
        ensure_ascii=False,
        indent=2,
    )
    if provider == "openrouter":
        return {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "research_writing_delegate_output",
                    "strict": True,
                    "schema": DELEGATE_SCHEMA,
                },
            },
            "provider": {"require_parameters": True},
            "max_tokens": max_output_tokens,
            "temperature": temperature,
        }

    return {
        "model": model,
        "input": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "research_writing_delegate_output",
                "strict": True,
                "schema": DELEGATE_SCHEMA,
            }
        },
        "max_output_tokens": max_output_tokens,
        "temperature": temperature,
    }


def endpoint_for_provider(provider: str) -> str:
    if provider == "openrouter":
        return OPENROUTER_CHAT_URL
    return OPENAI_RESPONSES_URL


def auth_hint(provider: str) -> str:
    if provider == "openrouter":
        return "redacted; sourced from RESEARCH_WRITING_DELEGATE_API_KEY or OPENROUTER_API_KEY"
    return "redacted; sourced from RESEARCH_WRITING_DELEGATE_API_KEY or OPENAI_API_KEY"


def api_key_for_provider(provider: str) -> str | None:
    override = os.environ.get("RESEARCH_WRITING_DELEGATE_API_KEY")
    if override:
        return override
    if provider == "openrouter":
        return os.environ.get("OPENROUTER_API_KEY")
    return os.environ.get("OPENAI_API_KEY")


def redact_request(request_payload: dict[str, Any], provider: str, endpoint: str) -> dict[str, Any]:
    return {
        "provider": provider,
        "model": request_payload["model"],
        "endpoint": endpoint,
        "request": request_payload,
        "auth": auth_hint(provider),
    }


def extract_output_text(api_response: dict[str, Any], provider: str) -> str:
    if provider == "openrouter":
        choices = api_response.get("choices", [])
        if not choices:
            raise SystemExit("Could not find choices in OpenRouter response.")
        message = choices[0].get("message", {})
        if message.get("refusal"):
            raise SystemExit(f"Model refusal: {message.get('refusal')}")
        content = message.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = [item.get("text", "") for item in content if item.get("type") == "text"]
            if parts:
                return "\n".join(parts)
        raise SystemExit("Could not find message content in OpenRouter response.")

    if isinstance(api_response.get("output_text"), str):
        return api_response["output_text"]

    parts: list[str] = []
    for output in api_response.get("output", []):
        for item in output.get("content", []):
            if item.get("type") in {"output_text", "text"} and isinstance(item.get("text"), str):
                parts.append(item["text"])
            if item.get("type") == "refusal":
                raise SystemExit(f"Model refusal: {item.get('refusal')}")
    if not parts:
        raise SystemExit("Could not find output text in API response.")
    return "\n".join(parts)


def call_api(
    request_payload: dict[str, Any],
    provider: str,
    endpoint: str,
    api_key: str,
    openrouter_site_url: str | None = None,
    openrouter_app_name: str | None = None,
) -> dict[str, Any]:
    body = json.dumps(request_payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if provider == "openrouter":
        if openrouter_site_url:
            headers["HTTP-Referer"] = openrouter_site_url
        if openrouter_app_name:
            headers["X-OpenRouter-Title"] = openrouter_app_name
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"{provider} API error {exc.code}: {detail}") from exc


def build_artifact(
    brief: dict[str, Any],
    request_payload: dict[str, Any],
    api_response: dict[str, Any],
    provider: str,
    endpoint: str,
) -> dict[str, Any]:
    output_text = extract_output_text(api_response, provider)
    try:
        parsed_output = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Delegate response was not valid JSON: {exc}\n{output_text}") from exc
    return {
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "provider": provider,
        "endpoint": endpoint,
        "model": request_payload["model"],
        "brief": brief,
        "delegate_output": parsed_output,
        "api_response_id": api_response.get("id"),
        "usage": api_response.get("usage"),
    }


def main() -> int:
    args = parse_args()
    if args.env_file:
        load_env_file(args.env_file)

    provider = args.provider.lower()
    brief = load_brief(args.brief)
    validate_brief(brief, args.brief_kind)
    model = resolve_model(provider, args.model)
    endpoint = endpoint_for_provider(provider)
    system_prompt = load_system_prompt(args.system_prompt)
    request_payload = build_request(brief, provider, model, system_prompt, args.max_output_tokens, args.temperature)

    if args.dry_run:
        print(json.dumps(redact_request(request_payload, provider, endpoint), indent=2, ensure_ascii=False))
        return 0

    api_key = api_key_for_provider(provider)
    if not api_key:
        raise SystemExit(
            f"Missing API key for {provider}. {auth_hint(provider)}. "
            "Set it in the environment, or pass --env-file .env for a local untracked file."
        )

    api_response = call_api(
        request_payload,
        provider,
        endpoint,
        api_key,
        args.openrouter_site_url,
        args.openrouter_app_name,
    )
    artifact = build_artifact(brief, request_payload, api_response, provider, endpoint)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        print(json.dumps(artifact, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
