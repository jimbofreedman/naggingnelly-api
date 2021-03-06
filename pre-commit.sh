#!/usr/bin/env bash
# pre-commit.sh
set -e

STASH_NAME="pre-commit-$(date +%s)"
git stash save -q --keep-index $STASH_NAME


# Check for syntax errors in requirements files
pip install -r requirements/test.txt

# Ensure pretty code
flake8 --count --statistics

# Test prospective commit
coverage run manage.py test
coverage report

STASHES=$(git stash list)
if [[ $STASHES == "$STASH_NAME" ]]; then
  git stash pop -q
fi
