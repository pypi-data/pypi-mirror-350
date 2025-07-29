#!/usr/bin/env bash

set -e

GIT_ROOT=$(git rev-parse --show-toplevel)
if [ $? -ne 0 ]; then
  echo "Error: Not inside a Git repository."
  exit 1
fi

SRC_DIR="$GIT_ROOT/src/isqtools"
OUTPUT_DIR="$GIT_ROOT/docs/source/apidocs"
mkdir -p "$OUTPUT_DIR"
sphinx-apidoc -o "$OUTPUT_DIR" --module-first --no-toc --force "$SRC_DIR"
