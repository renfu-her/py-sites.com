#!/usr/bin/env bash
set -euo pipefail
set -x
curl -sk https://py-sites.com/healthz -H "Host: py-sites.com" && echo
curl -sk https://shop.py-sites.com/healthz -H "Host: shop.py-sites.com" && echo
curl -sk https://web-primary.py-sites.com/healthz -H "Host: web-primary.py-sites.com" && echo
