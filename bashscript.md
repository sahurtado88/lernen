# script versionado

```
#!/bin/bash
set -e pipefail
if [ -z "$GIT_COMMIT" ]; then
    # Must be running locally, use latest
  echo "latest"
fi
if [[ "$GIT_COMMIT_MESSAGE" == *"chore"* && "$GIT_COMMIT_MESSAGE" == *"release"* && "$GIT_COMMIT_MESSAGE" =~ [0-9]+\.[0-9]+.\[0-9]+ ]]; then
  cat version.txt
else
  echo "$GIT_COMMIT"
fi    
```

# automatizar proceso de releases en github

```
#!/bin/bash
set -e pipefail

# prepare github release
GH_ENTERPRISE_API_URL= https://
GH_ENTERPROSE_GRAPHQL_URL=https
if [[ "$GIT_COMMIT_MESSAGE" == *"chore"* && "$GIT_COMMIT_MESSAGE" == *"release"* && "$GIT_COMMIT_MESSAGE" =~ [0-9]+\.[0-9]+.\[0-9]+ ]]; then
  echo "rRelease version found in commit message: $GIT_COMMIT_MESSAGE"
  echo "creating Github release"
  npx -y release-please github-release \
    --token="$(cat "${BUILD_SECRET_PATH}/github_token")" \
    --repo-url="$GIT_URL" \
    --api-url="$GH_ENTERPRISE_AI_URL" \
    --graphql-url="$GH_ENTERPRISE_GRAPHQL_URL" "$@" \
    --target-branch="$GIT_BRANCH"
fi

```

