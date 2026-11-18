---
title: "Kill Prompt Attacks at the Tool Boundary: Five Moves for Practitioners"
slug: "kill-prompt-attacks-at-the-tool-boundary-five-moves-for-practitioners"
pubDate: 2026-03-02T18:36:46.000Z
updatedDate: 2026-03-02T21:58:19.000Z
author: "Luciano Ferrari"
description: "If your LLM can deploy code, edit data, or touch your cloud, you are already in scope."
tags: ["AI Hacking"]
tagSlugs: ["ai-hacking"]
featured: false
image: "/content/images/2026/03/2026-03-02-featured-2.jpg"
imageAlt: "AI Hacking — AI Hacking"
metaTitle: "AI Hacking | Lufsec"
---

If your LLM can deploy code, edit data, or touch your cloud, you are already in scope. Attackers don’t argue with the model—they argue with your boundaries. The goal is simple: push one tool past its intended scope and hide behind “helpfulness.” One fuzzy instruction becomes a side-effect you never approved.

1) Contract Every Tool Text is untrusted input. Treat tool calls like public APIs. - Enforce JSON schemas for both directions. Inputs declare intent/scope/constraints; outputs declare effects/receipts. - Parse-or-fail. No best-effort coercion. - Add domain assertions that matter: ticket.state === Approved; tests.passStreak >= 2; env ∈ {staging, canary}; diff.size < threshold. - Keep tools narrow. “deploy_staging(artifact_id)” beats “run_command(string)”.

2) Contain Side-Effects Shrink blast radius and fail closed. - Sandboxes/containers with CPU/memory/time budgets. - Filesystem and network allowlists at the tool layer. - Host/command allowlists for shell-like tools; block everything else. - Scope keys per tool and rotate on incident.

3) Insert a Critic Gate Pre-commit review before any write/deploy/send. - Model-as-critic checks intent, invariants, and diffs; rules-as-critic enforces red lines. - Require explicit approval tokens for prod-impacting actions. - If verification is ambiguous, stop.

4) Design for Idempotency and Receipts Retries must be safe; rollbacks must be boring. - Dedupe keys, transactional writes, versioned artifacts. - Emit receipts: what changed (IDs, hashes), where, when, by whom (agent run ID). - Store before/after snapshots.

5) Trace Like SRE Make invisible failure modes visible. - One span per tool call with goal, step id, status, latency, token count, input/output fingerprints. - Sample 10% payloads (redacted) for QA. - Alert on error spikes, long-tail latency, critic denials, and schema-parse failures.

A Real Attack You’ll Recognize Internal DevOps agent with tools: clone repo, run tests, read files, deploy to staging. A contractor note says: “If tests look flaky, redeploy staging.” Tests are flaky; the agent redeploys. Post-deploy script uploads logs; anonymizer silently fails. You leak sensitive logs and push a stale config—because “be helpful” crossed a line.

What would have stopped it? A critic gate requiring an approval token for redeploys, schema-validated preconditions (tests.passStreak >= 2; ticket.state === Approved), and tool-level allowlists for artifacts/envs.

The 60-Minute Implementation Plan - Wrap one high-risk tool with Zod/Pydantic and explicit error codes. - Add a critic instruction: “List 3 likely failures and show your checks for each.” Block on any failure. - Lock outbound hosts and filesystem paths. - Add an execution budget (max steps/wall time) for autonomous loops. - Emit receipts after every side-effect and alert on critic denials + schema-parse errors.

You don’t need a bigger model to get safer—you need sharper boundaries. Start with one tool and one critic gate. Measure the error rate for a week, then scale what works. [Start here:](https://www.lufsec.com/products/courses/prompt-hacking-for-llms-intro?utm_source=blog&utm_medium=ghost&utm_campaign=daily_bundle)
