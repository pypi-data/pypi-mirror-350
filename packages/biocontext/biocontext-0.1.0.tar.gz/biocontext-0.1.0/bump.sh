#!/bin/bash
set -e
uv version --bump "$1"
uv lock
version=$(uv version --short)
git commit -am "Bump version to v$version"
git tag "v$version"
