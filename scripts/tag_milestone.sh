#!/bin/bash
#
# Creates and pushes a new Git tag to archive a project milestone.
#

set -e

VERSION=$1
MESSAGE=$2

if [ -z "$VERSION" ] || [ -z "$MESSAGE" ]; then
    echo "Usage: $0 <version> <message>"
    exit 1
fi

echo "Creating tag $VERSION..."
git tag -a "$VERSION" -m "$MESSAGE"

echo "Pushing tag to remote..."
git push origin "$VERSION"

echo "Milestone $VERSION has been successfully tagged and pushed."
