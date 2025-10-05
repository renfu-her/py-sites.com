#!/usr/bin/env bash
set -euo pipefail
root="/home/renfu/htdocs/py-sites"

for app in main shop web_primary; do
  cd "${root}/${app}"
  if [[ ! -d venv ]]; then
    python3 -m venv venv
  fi
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  deactivate
done

echo "venv + requirements 安裝完成 ✅"
