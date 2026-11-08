#!/usr/bin/env bash
# Install independent personal copies from this checkout.
set -euo pipefail
source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
if command -v py >/dev/null 2>&1; then
    exec py -3 "$source_dir/install-aegis.py" --personal "$@"
fi
exec python3 "$source_dir/install-aegis.py" --personal "$@"
