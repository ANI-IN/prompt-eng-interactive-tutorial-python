#!/usr/bin/env bash
# Runs on every Codespace start. The course reads ANTHROPIC_API_KEY from the
# environment first; this just materializes a repo-root .env from the Codespaces
# secret as a fallback (in case the kernel process doesn't inherit env vars).
# .env is gitignored, so the key never gets committed.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -f .env ]; then
  echo ".env already present; leaving it untouched."
elif [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  umask 077
  echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" > .env
  echo "Wrote .env from the ANTHROPIC_API_KEY Codespaces secret."
else
  echo "No ANTHROPIC_API_KEY found. Add it as a Codespaces secret (Settings →"
  echo "Codespaces → Secrets) scoped to this repo, or create .env manually:"
  echo "  cp .env.example .env   # then edit it"
fi
