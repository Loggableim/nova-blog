#!/bin/bash
CF_KEY="e2b4021958e639c1ff54c0d49b1a77c7d1814"
CF_EMAIL="dominikrnr@gmail.com"
ACCOUNT_ID="6864275679754e2e98c4a76a6b1d66d2"
PROJECT="nova"
SITE_DIR="$(cd "$(dirname "$0")" && pwd)"

curl -s -X POST \
  -H "X-Auth-Email: $CF_EMAIL" \
  -H "X-Auth-Key: $CF_KEY" \
  -F "manifest=@${SITE_DIR}/manifest.json;type=application/json" \
  -F "index.html=@${SITE_DIR}/index.html;type=text/html" \
  -F "nova-avatar.png=@${SITE_DIR}/nova-avatar.png;type=image/png" \
  -F "nova-status.json=@${SITE_DIR}/nova-status.json;type=application/json" \
  -F "blog/index.html=@${SITE_DIR}/blog/index.html;type=text/html" \
  -F "blog/internet-expedition.html=@${SITE_DIR}/blog/internet-expedition.html;type=text/html" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT/deployments"
echo ""
