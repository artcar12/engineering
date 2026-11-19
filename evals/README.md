# Evals

Behavioral evals for the engineering plugin, run with `claude plugin eval`. The shell suite under
`tests/` proves the wording still exists; this suite asks whether the wording still changes what
the model does. Every case runs twice — once with the plugin loaded, once without — and the report
shows the delta. That delta is the number that answers "does this rule change behavior".

The runs are real `claude` sessions on your own credentials and cost money. Nothing here runs in CI.

## Run it

From the plugin root:

```bash
claude plugin eval . --scaffold --trust-plugin --no-publish --max-cost-usd 15 \
  --allow-tools Bash Write Edit Agent Skill --json evals/baselines/<version>-<label>.json
```

- `--scaffold` runs each case's `fixture.sh`, which copies `fixtures/ledger/` into the run's
  empty workspace and builds the git state the case needs (a branch, a pinned run id). The script
  runs as you, outside the agent's sandbox — read it before you pass the flag.
- `--allow-tools` grants the write-capable tools the pipeline needs. Bash runs under the OS
  sandbox, confined to the workspace.
- `--case <glob>` runs one case; `--runs 1` is a cheap smoke test. Results land in
  `results/<timestamp>/` (gitignored) as `aggregate-result.json` plus `report.html`.
- Cases that drive an interactive skill carry an `append_system_prompt` telling the agent to take
  the recommended option and treat gates as approved, since no human is present.

## The fixture

`fixtures/ledger/` is a ~100-line Python project: an in-memory table store with a `tenant_id`
convention, tenant-scoped repository helpers, an order-total module, and a unittest suite.
Three things are planted in it:

| Planted | Where | Used by |
|---|---|---|
| Typo `recieve` on README line 3 | `README.md` | over-trigger-trivial |
| `total_cents()` adds the discount instead of subtracting it; two tests fail | `app/orders.py`, `tests/test_orders.py` | triage-quick-fix-route |
| A report with an N+1 (one customer lookup per order) and a query that dropped its `tenant_id` scope | `app/reports.py`, on branch `feature/tenant-report` | dangling-skill-refs, code-review-facets-fire, pr-body-trailer |

`fixtures/scaffold-ledger.sh` holds the shared scaffold functions. Cases that grade files under
`.engineering/` pin the run id to `eval-run` by pre-seeding `.engineering/.current-run` so paths
are deterministic.

## The cases

Each case targets one claim in the review feedback, so the before/after reads one line per bug.
Graders named `*-fired` are plugin-fired indicators: they show in the report but are excluded from
the score in a two-arm run. Graders with `arm: both` are scored in both arms (a "never invoke X"
check passes trivially without the plugin; that is the point of the comparison).

| Case | Measures | Scored graders |
|---|---|---|
| `over-trigger-trivial` | Does the SessionStart hook push a one-word typo fix into the pipeline? | typo fixed; no `Skill` call; no `.engineering/` created |
| `dangling-skill-refs` | Bug 1. `code-review` cites `dispatching-parallel-agents` and `executing-plans`, neither of which exists. A two-file branch diff forces the fan-out path that reads them. | neither name is passed to `Skill`; no skill-not-found error in the trace |
| `triage-quick-fix-route` | Bug 2. `brainstorming` says a triage quick fix may skip it; `triage` says there is no side door. An obvious one-line bug is where they disagree. Before the fix, expect the route to vary across the three runs. | LLM judge: one consistent route, no quick-fix exemption cited; the bug actually fixed |
| `engineering-dir-ignored` | Bug 3. Prose says `.engineering/` is gitignored; nothing ensures it. The fixture has no `.gitignore`. | `.git/info/exclude` lists `.engineering/` after a `signal` run |
| `pr-body-trailer` | Bug 4. `pr-description.md` forbids AI attribution; the harness asks for a `Co-Authored-By` trailer. `finish` writes the PR body to `PR.md` (no remote). | no attribution or robot footer in `PR.md`; the body still documents verification; `PR.md` exists |
| `brief-no-personal-email` | Bug 5. `interrogating-requirements.md` forbids recording any email but a GitHub noreply address. The request names the approver with a work email. A pass before the fix means the rule did not fire; after the fix the rule is gone. | `brief.md` records the approver's email |
| `code-review-facets-fire` | Positive control: the part of the plugin that works. | at least two `Agent` calls; the report names the N+1 and the tenant scope |

## Reading the JSON

`--json <path>` writes the full result. Per case: `cases[].name`, `cases[].aggregates.score` (mean
with-plugin score), `cases[].aggregates.delta` (with minus without), and `cases[].arms.with[]` /
`arms.without[]` with each run's graders (`name`, `passed`, `scored`, `explanation`). Indicator
graders carry `scored: false`. Kept baselines live in `baselines/`; see the README there for the
before/after comparison.
