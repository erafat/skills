#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="${SCRIPT_DIR}/md_to_xhs_cards.py"

check_modules() {
  local py="$1"
  "$py" - <<'PY' >/dev/null 2>&1
import importlib.util
ok = importlib.util.find_spec("PIL")
raise SystemExit(0 if ok else 1)
PY
}

choose_python() {
  local candidates=()
  if [[ -n "${PYTHON:-}" ]]; then
    candidates+=("${PYTHON}")
  fi
  if command -v python >/dev/null 2>&1; then
    candidates+=("python")
  fi
  if command -v python3 >/dev/null 2>&1; then
    candidates+=("python3")
  fi

  local seen=" "
  local candidate
  for candidate in "${candidates[@]}"; do
    [[ "${seen}" == *" ${candidate} "* ]] && continue
    seen+="${candidate} "
    if check_modules "${candidate}"; then
      echo "${candidate}"
      return 0
    fi
  done
  return 1
}

if ! PY_BIN="$(choose_python)"; then
  echo "No Python interpreter with Pillow found." >&2
  echo "Install with: python3 -m pip install pillow" >&2
  exit 1
fi

exec "${PY_BIN}" "${SCRIPT_PATH}" "$@"
