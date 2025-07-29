#!/usr/bin/env bash

# ─── Fail Fast ─────────────────────────────────────────────────────────────────
set -Eeuo pipefail
trap 'echo -e "\n❌ Error on line $LINENO. Exiting."; exit 1' ERR

# ─── Command Wrapper ───────────────────────────────────────────────────────────
check_command() {
    echo -e "\n🔹 Running: \033[1;36m$*\033[0m"
    "$@"
}

# ─── Install Dev Requirements ──────────────────────────────────────────────────
echo -e "\n\033[1;34m==> Installing development requirements...\033[0m"
check_command pip install -r requirements-dev.txt

# ─── Set Up Pre-commit Hooks ───────────────────────────────────────────────────
echo -e "\n\033[1;34m==> Installing pre-commit hooks...\033[0m"
check_command pre-commit install
check_command pre-commit install-hooks

# ─── Install Library in Editable Mode ──────────────────────────────────────────
echo -e "\n\033[1;34m==> Installing library in editable mode...\033[0m"
check_command pip install --editable . --config-settings editable_mode=strict

# ─── Done ──────────────────────────────────────────────────────────────────────
echo -e "\n\033[1;32m✅ Setup complete.\033[0m"

exit 0
