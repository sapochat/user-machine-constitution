# User–Machine Constitution

A workshop and validation toolkit for creating a bilateral operating contract between a person and an AI agent.

This is not a published private constitution and it is not a personality prompt. It is a neutral method for deciding:

- who holds which responsibilities;
- how disagreement and uncertainty work;
- when the agent may act autonomously;
- which actions require immediate approval;
- what belongs in memory, skills, or temporary artifacts;
- how failures become amendments rather than repeated apologies;
- how the agreement is ratified, deployed, and reviewed.

`working-with-an-agent` explains the broader collaboration system. This repository produces and maintains the actual bilateral contract inside that system.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -e .

.venv/bin/user-machine-constitution init ./my-constitution \
  --human "Your name" --agent "Agent name"

.venv/bin/user-machine-constitution check \
  ./my-constitution/constitution.toml \
  --scenarios ./my-constitution/stress-tests.json \
  --allow-draft

.venv/bin/user-machine-constitution render \
  ./my-constitution/constitution.toml \
  ./my-constitution/constitution.md
```

## Workflow

1. **Discover:** answer the questionnaire independently where useful.
2. **Draft:** encode decisions in the TOML source, not only prose.
3. **Stress-test:** use concrete failure and authority scenarios.
4. **Reconcile:** resolve ambiguous or contradictory clauses.
5. **Ratify:** the human approves; the agent restates operational effects.
6. **Deploy:** place the compact contract in an always-on profile/personality layer.
7. **Observe:** record failures as evidence, not shame.
8. **Amend:** change the correct clause, update the changelog, and rerun tests.

## Included

- neutral draft generator;
- machine-readable TOML constitution;
- Markdown renderer;
- structural, privacy, approval-boundary, and stress-coverage checks;
- discovery, ratification, and amendment templates;
- synthetic example involving fictional parties;
- portable `SKILL.md` for agent-assisted constitution design.

## Important boundary

A constitution should be stored in an always-on configuration layer. The skill in this repository teaches how to create and maintain one; it should not be the only place the resulting contract lives.

## Test

```bash
.venv/bin/python -m unittest discover -s tests -v
```

## License

MIT.
