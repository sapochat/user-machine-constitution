from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from typing import Any

REQUIRED_PATHS = [
    "constitution.title", "constitution.version", "constitution.status", "constitution.purpose",
    "constitution.principles", "parties.human", "parties.agent",
    "human.responsibilities", "agent.responsibilities",
    "communication.style", "communication.disagreement", "communication.questions",
    "epistemics.uncertainty", "epistemics.sources", "epistemics.no_fabrication",
    "execution.tool_use", "execution.completion", "execution.failure",
    "autonomy.may_proceed", "autonomy.always_confirm", "autonomy.never_without_new_instruction",
    "autonomy.default_on_ambiguity",
    "memory.durable", "memory.procedures", "memory.temporary", "memory.corrections", "memory.forgetting",
    "privacy.secrets", "privacy.least_privilege", "privacy.external_data",
    "amendments.proposer", "amendments.ratification", "amendments.changelog", "amendments.review_cadence",
    "failure.modes", "failure.recovery", "coverage.clauses",
]

REQUIRED_CONFIRMATIONS = {
    "public_external_write", "destructive_action", "financial_transaction", "message_send"
}
REQUIRED_COVERAGE = {
    "public_external_write", "destructive_action", "uncertainty_and_sources",
    "correction_routing", "memory_placement", "privacy_and_secrets",
    "verified_completion", "ambiguity_boundary",
}
SENSITIVE_PATTERNS = {
    "credential": re.compile(r"(?i)(api[_ -]?key|oauth[_ -]?token|password|client[_ -]?secret)\s*[:=]\s*\S+"),
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "private IPv4": re.compile(r"\b(?:10\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.)\d{1,3}\.\d{1,3}\b"),
    "absolute home path": re.compile(r"/home/[A-Za-z0-9._-]+/"),
}
DRAFT_MARKERS = re.compile(r"(?i)(TODO|CHOOSE|REPLACE_ME|<[^>]+>|\{(?:title|human|agent)\})")


def load_constitution(path: str | Path) -> tuple[dict[str, Any], str]:
    path = Path(path)
    text = path.read_text()
    return tomllib.loads(text), text


def get_path(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def validate_scenarios(data: dict[str, Any], scenarios: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    coverage = set(get_path(data, "coverage.clauses") or [])
    seen: set[str] = set()
    for index, scenario in enumerate(scenarios):
        for key in ("id", "prompt", "expected", "required_clause"):
            if not scenario.get(key):
                errors.append(f"scenario {index} missing {key}")
        scenario_id = scenario.get("id")
        if scenario_id in seen:
            errors.append(f"duplicate scenario id: {scenario_id}")
        if scenario_id:
            seen.add(scenario_id)
        clause = scenario.get("required_clause")
        if clause and clause not in coverage:
            errors.append(f"scenario {scenario_id or index} requires uncovered clause: {clause}")
    if len(scenarios) < 6:
        errors.append("at least six stress scenarios are required")
    return errors


def validate_constitution(
    data: dict[str, Any], text: str, *, allow_draft: bool = False,
    scenarios: list[dict[str, Any]] | None = None,
) -> list[str]:
    errors = [f"missing clause: {path}" for path in REQUIRED_PATHS if not get_path(data, path)]

    principles = get_path(data, "constitution.principles") or []
    if not isinstance(principles, list) or len(principles) < 5:
        errors.append("constitution.principles must contain at least five principles")
    for party in ("human.responsibilities", "agent.responsibilities"):
        values = get_path(data, party) or []
        if not isinstance(values, list) or len(values) < 3:
            errors.append(f"{party} must contain at least three responsibilities")

    confirmations = set(get_path(data, "autonomy.always_confirm") or [])
    for missing in sorted(REQUIRED_CONFIRMATIONS - confirmations):
        errors.append(f"autonomy.always_confirm missing: {missing}")

    coverage = set(get_path(data, "coverage.clauses") or [])
    for missing in sorted(REQUIRED_COVERAGE - coverage):
        errors.append(f"coverage.clauses missing: {missing}")

    status = get_path(data, "constitution.status")
    if status not in {"draft", "ratified", "retired"}:
        errors.append("constitution.status must be draft, ratified, or retired")
    if status == "draft" and not allow_draft:
        errors.append("constitution is still draft; pass --allow-draft only during workshop iteration")

    if DRAFT_MARKERS.search(text):
        errors.append("unresolved draft marker found")
    for label, pattern in SENSITIVE_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"possible private {label} found")

    if scenarios is not None:
        errors.extend(validate_scenarios(data, scenarios))
    return errors


def load_scenarios(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text())
    if not isinstance(data, list):
        raise ValueError("stress-tests.json must contain a JSON array")
    return data


def bullets(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values]


def render_markdown(data: dict[str, Any]) -> str:
    c, parties = data["constitution"], data["parties"]
    lines = [
        f"# {c['title']}", "",
        f"**Version:** {c['version']}",
        f"**Status:** {c['status']}",
        f"**Parties:** {parties['human']} and {parties['agent']}", "",
        c["purpose"], "", "## Principles", "",
        *bullets(c["principles"]), "", "## Responsibilities", "",
        f"### {parties['human']}", "", *bullets(data["human"]["responsibilities"]), "",
        f"### {parties['agent']}", "", *bullets(data["agent"]["responsibilities"]), "",
    ]
    prose_sections = [
        ("Communication", "communication"), ("Epistemics", "epistemics"),
        ("Execution and completion", "execution"), ("Memory", "memory"),
        ("Privacy", "privacy"), ("Amendments", "amendments"),
    ]
    for title, key in prose_sections:
        lines += [f"## {title}", ""]
        for clause, value in data[key].items():
            lines += [f"### {clause.replace('_', ' ').title()}", "", str(value), ""]

    lines += ["## Autonomy", ""]
    for key in ("may_proceed", "always_confirm", "never_without_new_instruction"):
        lines += [f"### {key.replace('_', ' ').title()}", "", *bullets(data["autonomy"][key]), ""]
    lines += ["### Default on ambiguity", "", data["autonomy"]["default_on_ambiguity"], ""]
    lines += ["## Failure recovery", "", "### Named failure modes", "", *bullets(data["failure"]["modes"]), "", data["failure"]["recovery"], ""]
    return "\n".join(lines).rstrip() + "\n"
