#!/bin/sh

source .env

uv run \
  --directory /Users/ouzhencong/Codes/assistants/longport-stock-server \
  main.py \
  --app-key $LONGPORT_APP_KEY \
  --app-secret $LONGPORT_APP_SECRET \
  --access-token $LONGPORT_ACCESS_TOKEN \
  --region "cn" \
  --enable-overnight true