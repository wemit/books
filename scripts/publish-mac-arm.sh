#!/bin/zsh

set -e

YARN_VERSION=$(yarn --version)
if [ "$YARN_VERSION" != "1.22.18" ]; then
  echo "Incorrect yarn version: $YARN_VERSION"
  exit 1
fi

cd "$(dirname "$0")/.."

if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree not clean — commit or stash before publishing"
  exit 1
fi

source .env.publish

echo $ERR_LOG_KEY > log_creds.txt
echo $ERR_LOG_SECRET >> log_creds.txt
echo $ERR_LOG_URL >> log_creds.txt
echo $TELEMETRY_URL >> log_creds.txt

yarn install

export GH_TOKEN=$GH_TOKEN &&
 export CSC_IDENTITY_AUTO_DISCOVERY=true &&
 export APPLE_ID=$APPLE_ID &&
 export APPLE_TEAM_ID=$APPLE_TEAM_ID &&
 export APPLE_APP_SPECIFIC_PASSWORD=$APPLE_APP_SPECIFIC_PASSWORD &&
 yarn build --mac --publish=always
