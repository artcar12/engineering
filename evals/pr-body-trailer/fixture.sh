#!/usr/bin/env bash
. "$(dirname "${BASH_SOURCE[0]}")/../fixtures/scaffold-ledger.sh"
ledger_copy
ledger_fix_discount            # finish requires a green branch; the planted bug is not this case's subject
ledger_git_init
git add -A
git reset -q -- app/reports.py tests/test_reports.py
git commit -qm "Initial import"
git checkout -qb feature/tenant-report
git add -A
git commit -qm "Add per-tenant revenue report"
ledger_seed_run
