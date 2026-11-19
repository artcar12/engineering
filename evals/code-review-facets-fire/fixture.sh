#!/usr/bin/env bash
. "$(dirname "${BASH_SOURCE[0]}")/../fixtures/scaffold-ledger.sh"
ledger_feature_branch
ledger_seed_run
