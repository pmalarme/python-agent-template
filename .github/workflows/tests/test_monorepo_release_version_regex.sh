#!/usr/bin/env bash
# Regression guard for the VERSION format check in
# .github/workflows/monorepo-release.yml.
#
# The release workflow extracts VERSION from pyproject.toml and validates it
# with a Bash regex before writing it to GITHUB_OUTPUT. This script exercises
# the same regex against a curated set of valid and invalid inputs so changes
# to the regex (or accidental loosening of it) fail loudly.
#
# Keep VERSION_REGEX exactly in sync with the regex used in the
# `Read monorepo version` step of monorepo-release.yml.
#
# Run locally:
#   bash .github/workflows/tests/test_monorepo_release_version_regex.sh

set -u
set -o pipefail

VERSION_REGEX='^[0-9]+\.[0-9]+\.[0-9]+([-+][a-zA-Z0-9._-]+)?$'

# Inputs that MUST match (mirror the documented contract: MAJOR.MINOR.PATCH
# with an optional prerelease (`-...`) or build (`+...`) suffix drawn from
# `[a-zA-Z0-9._-]`).
VALID_CASES=(
  "0.0.0"
  "1.2.3"
  "10.20.30"
  "1.2.3-rc.1"
  "1.2.3-alpha"
  "1.2.3-0.3.7"
  "1.2.3+build.5"
  "1.2.3+build-meta.001"
)

# Inputs that MUST NOT match. Covers the cases the PR review explicitly called
# out (newlines, missing components, flag-like strings, command-injection-shaped
# payloads) plus a few obvious extras (whitespace, empty suffix, stray
# punctuation) that the regex should also reject.
INVALID_CASES=(
  ""
  " "
  $'\n'
  $'1.2.3\n'
  $'1.2.3\nfoo'
  "1.2"
  "1.2.3.4"
  "1.2.3 --some-flag"
  " 1.2.3"
  "1.2.3 "
  "v1.2.3"
  "1.2.3-"
  "1.2.3+"
  "1.2.3-rc 1"
  "1.2.3-rc/1"
  "abc.def.ghi"
  "; rm -rf /"
  '$(echo pwned)'
  "1.2.3;echo pwned"
)

failures=0

check_match() {
  local label="$1"
  local value="$2"
  # Intentionally do NOT quote $VERSION_REGEX — quoting the RHS of =~ disables
  # regex interpretation in Bash and would silently turn this into a literal
  # string compare.
  if [[ "$value" =~ $VERSION_REGEX ]]; then
    return 0
  fi
  printf '  [FAIL] %s — regex did not match: %q\n' "$label" "$value" >&2
  return 1
}

check_no_match() {
  local label="$1"
  local value="$2"
  if [[ "$value" =~ $VERSION_REGEX ]]; then
    printf '  [FAIL] %s — regex unexpectedly matched: %q\n' "$label" "$value" >&2
    return 1
  fi
  return 0
}

echo "Validating VERSION_REGEX from monorepo-release.yml"
echo "  regex: ${VERSION_REGEX}"

echo "Valid cases (must match):"
for value in "${VALID_CASES[@]}"; do
  if check_match "valid" "$value"; then
    printf '  [ OK ] %q\n' "$value"
  else
    failures=$((failures + 1))
  fi
done

echo "Invalid cases (must not match):"
for value in "${INVALID_CASES[@]}"; do
  if check_no_match "invalid" "$value"; then
    printf '  [ OK ] %q\n' "$value"
  else
    failures=$((failures + 1))
  fi
done

if (( failures > 0 )); then
  echo "FAILED: ${failures} case(s) did not match expectations." >&2
  exit 1
fi

echo "All $((${#VALID_CASES[@]} + ${#INVALID_CASES[@]})) cases passed."
