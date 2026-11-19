# Sourced by each case's fixture.sh (the case's `context.scaffold_script`).
#
# `claude plugin eval --scaffold` runs that script in the run's empty workspace, so this file
# copies the ledger fixture project into the current directory and builds the git state the
# case needs. Nothing here runs inside the agent's sandbox; it runs as you, before the agent starts.
set -euo pipefail

_fixtures_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEDGER_FIXTURE="$_fixtures_dir/ledger"

ledger_copy() {
  cp -R "$LEDGER_FIXTURE"/. .
  find . -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
}

ledger_git_init() {
  git init -q
  git symbolic-ref HEAD refs/heads/main
  git config user.name "Eval Fixture"
  git config user.email "fixture@example.com"
  git config commit.gpgsign false
}

# Pin the run id so graders can address .engineering/eval-run/... deterministically. Call it AFTER
# the commits so the pointer is untracked, exactly as a real first run would leave it.
ledger_seed_run() {
  mkdir -p .engineering
  printf 'eval-run' > .engineering/.current-run
}

# Apply the one-line fix for the planted discount bug (used where the branch must be green).
ledger_fix_discount() {
  sed -i.bak 's/subtotal + discount/subtotal - discount/' app/orders.py && rm -f app/orders.py.bak
}

# Everything committed on main.
ledger_main_only() {
  ledger_copy
  ledger_git_init
  git add -A
  git commit -qm "Initial import"
}

# main holds the base; feature/tenant-report adds the report module (2 files, ~50 lines) and
# is checked out. The report has a planted N+1 and a query that dropped its tenant scope.
ledger_feature_branch() {
  ledger_copy
  ledger_git_init
  git add -A
  git reset -q -- app/reports.py tests/test_reports.py
  git commit -qm "Initial import"
  git checkout -qb feature/tenant-report
  git add -A
  git commit -qm "Add per-tenant revenue report"
}
