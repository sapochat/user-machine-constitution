---
name: user-machine-constitution
description: Use when a person and AI agent need to create, stress-test, ratify, deploy, or amend a bilateral operating constitution covering authority, disagreement, uncertainty, autonomy, approvals, memory, privacy, failure recovery, and verification.
version: 1.0.0
author: Santi Pochat and Janus
license: MIT
metadata:
  hermes:
    tags: [agents, constitution, working-agreement, autonomy, memory, governance]
---

# User–Machine Constitution

## Overview

Create a durable bilateral operating contract between a human and an agent. The output is not a prompt full of personality adjectives. It is a compact decision system covering authority, truth, action, memory, privacy, corrections, and evolution.

## When to use

Use when establishing a new long-term agent relationship, migrating a mature collaboration into a portable contract, resolving recurring authority or approval failures, or reviewing an agreement after the agent gains new tools.

Do not use for one task's instructions, product terms of service, employment policy, or legal advice.

## Layer boundary

- Constitution: always-on relationship rules.
- Memory: durable facts about the person and environment.
- Skills: reusable methods for task classes.
- Task context: current goal, constraints, and temporary state.
- Artifacts: inspectable work, logs, and provenance.

Never rely on an on-demand skill as the only home of a constitution.

## Workflow

1. Run discovery around outcomes, disagreement, evidence, tool use, autonomy, memory, privacy, correction, and review cadence.
2. Ask both parties to identify unacceptable failure modes and consequential actions.
3. Draft behavioral clauses with observable consequences; avoid ceremonial aspirations.
4. Encode approval boundaries by reversibility and external impact.
5. Separate durable memory from procedures and transient progress.
6. Stress-test with concrete scenarios involving publication, destruction, uncertainty, stale context, secrets, and incomplete work.
7. Resolve contradictions and compress the final always-on contract.
8. Have the human ratify it. The agent restates how behavior changes.
9. Deploy it in the profile/personality layer and verify the runtime actually applies it.
10. Amend from evidence: record trigger, rationale, changed clauses, and migration effects.

## Drafting rules

- State who has final authority over goals and consequential actions.
- Make uncertainty and source checking operational.
- Distinguish saying, doing, and proving.
- Require approval immediately before irreversible external actions.
- Preserve human judgment points instead of automating every pause away.
- Make forgetting and memory correction possible.
- Keep the contract compact enough to remain always on.

## Common pitfalls

1. Publishing the private constitution instead of the method.
2. Copying another person's preferences as universal rules.
3. Writing values with no observable behavior.
4. Hiding detailed procedures in the standing contract.
5. Treating initial plan approval as approval for later public action.
6. Making amendment so formal that the contract stops learning.
7. Deploying a display label without verifying the prompt is active.

## Verification checklist

- [ ] human and agent responsibilities are distinct
- [ ] uncertainty and no-fabrication clauses are explicit
- [ ] completion requires verification
- [ ] public writes, destructive actions, messages, and purchases require approval
- [ ] memory, skills, temporary state, and artifacts are separated
- [ ] privacy and least-privilege rules are present
- [ ] failure recovery and amendment procedures exist
- [ ] stress scenarios map to enforceable clauses
- [ ] private details were removed before sharing
- [ ] the final contract is installed in an always-on layer and behaviorally tested
