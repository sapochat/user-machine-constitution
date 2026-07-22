from __future__ import annotations

import argparse
import json
from importlib.resources import files
from pathlib import Path

from .constitution import load_constitution, load_scenarios, render_markdown, validate_constitution


def safe_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def init_workspace(destination: Path, human: str, agent: str, title: str | None = None) -> Path:
    if destination.exists():
        raise FileExistsError(destination)
    destination.mkdir(parents=True)
    template_root = files("user_machine_constitution").joinpath("templates")
    template = template_root.joinpath("constitution-template.toml").read_text()
    values = {
        "title": safe_value(title or f"Working Constitution for {human} and {agent}"),
        "human": safe_value(human),
        "agent": safe_value(agent),
    }
    for key, value in values.items():
        template = template.replace("{" + key + "}", value)
    (destination / "constitution.toml").write_text(template)
    (destination / "discovery.md").write_text(template_root.joinpath("discovery-questionnaire.md").read_text())
    (destination / "stress-tests.json").write_text(template_root.joinpath("stress-tests.json").read_text())
    (destination / "RATIFICATION.md").write_text(template_root.joinpath("ratification-checklist.md").read_text())
    (destination / "CHANGELOG.md").write_text("# Constitution changelog\n\n## Unreleased\n\n- Initial workshop draft.\n")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(prog="user-machine-constitution")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create a neutral constitution workshop")
    init.add_argument("destination", type=Path)
    init.add_argument("--human", required=True)
    init.add_argument("--agent", required=True)
    init.add_argument("--title")

    check = sub.add_parser("check", help="validate structure, boundaries, privacy, and stress coverage")
    check.add_argument("constitution", type=Path)
    check.add_argument("--scenarios", type=Path)
    check.add_argument("--allow-draft", action="store_true")

    render = sub.add_parser("render", help="render constitution TOML as Markdown")
    render.add_argument("constitution", type=Path)
    render.add_argument("output", type=Path)

    args = parser.parse_args()
    if args.command == "init":
        print(init_workspace(args.destination, args.human, args.agent, args.title))
        return 0

    data, text = load_constitution(args.constitution)
    if args.command == "render":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render_markdown(data))
        print(args.output)
        return 0

    scenarios = load_scenarios(args.scenarios) if args.scenarios else None
    errors = validate_constitution(data, text, allow_draft=args.allow_draft, scenarios=scenarios)
    for error in errors:
        print(f"ERROR: {error}")
    print("RESULT: PASS" if not errors else "RESULT: FAIL")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
