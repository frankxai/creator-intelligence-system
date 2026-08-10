#!/usr/bin/env python3
"""Validate Creator Intelligence System release truth without dependencies."""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"release contract: {message}")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads(read(path))


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


ledger = load_json("docs/releases/release-ledger.json")
changelog = read("CHANGELOG.md")
readme = read("README.md")
attestation = read("ATTESTATION.md")
notes = read(ledger["release"]["notesPath"])
audit = read("docs/releases/2026-08-10-release-foundation.md")
draft_workflow = read(".github/workflows/draft-github-prerelease.yml")
root_manifest = load_json("package.json")
package_manifests = [
    root_manifest,
    load_json("packages/core/package.json"),
    load_json("packages/voice/package.json"),
]

if ledger.get("schemaVersion") != 1:
    fail("schemaVersion must be 1")
if ledger.get("repository") != "frankxai/creator-intelligence-system":
    fail("repository identity is incorrect")
if ledger.get("defaultBranch") != "main":
    fail("defaultBranch must be main")

release = ledger["release"]
source = ledger["source"]
next_release = ledger["nextRelease"]
semver = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
full_sha = re.compile(r"^[0-9a-f]{40}$")

if not semver.fullmatch(release["version"]):
    fail("release.version must be SemVer")
if "-" not in release["version"] or not release["prerelease"]:
    fail("the first candidate must remain a prerelease")
if release["tag"] != f"v{release['version']}":
    fail("release tag must match version")
if release["status"] not in {"draft", "ready", "published"}:
    fail("release status must be draft, ready, or published")
if release["published"] != (release["status"] == "published"):
    fail("published flag must agree with release status")
if source["semanticTags"] != [] or source["githubReleaseCount"] != 0:
    fail("the audit must preserve the absence of semantic releases")

for field, value in {
    "source.auditedHead": source["auditedHead"],
    "release.targetSha": release["targetSha"],
    "nextRelease.auditedFromExclusive": next_release["auditedFromExclusive"],
    "nextRelease.auditedThroughInclusive": next_release["auditedThroughInclusive"],
}.items():
    if not full_sha.fullmatch(value):
        fail(f"{field} must be a full SHA")

if release["targetSha"] != source["auditedHead"]:
    fail("the alpha candidate must match the audited main boundary")
if next_release["version"] != "0.1.0-alpha.1":
    fail("the next candidate must be 0.1.0-alpha.1")
if next_release["targetSha"] is not None:
    fail("the next candidate may not have an invented target")
if next_release["status"] != "awaiting-prerelease-and-post-governance-boundary":
    fail("the next candidate queue state is incorrect")
if next_release["auditedFromExclusive"] != release["targetSha"]:
    fail("the next audit must begin after the current candidate")
if next_release["auditedThroughInclusive"] != source["auditedHead"]:
    fail("the next audit must end at the audited head")
if next_release["auditedCommitCount"] != 0:
    fail("no post-boundary source commits existed at audit")

try:
    git("cat-file", "-e", f"{release['targetSha']}^{{commit}}")
    git("merge-base", "--is-ancestor", release["targetSha"], "HEAD")
except subprocess.CalledProcessError:
    fail("the immutable alpha boundary must exist in HEAD history")

if int(git("rev-list", "--count", source["auditedHead"])) != source["commitCount"]:
    fail("audited commit count does not match Git history")
if int(git("rev-list", "--count", release["targetSha"])) != release["targetCommitCount"]:
    fail("candidate commit count does not match Git history")

boundary = ledger["receipts"]["releaseBoundary"]
receipt_commits: set[str] = set()
for receipt in boundary["pullRequests"]:
    number = receipt["number"]
    expected_url = f"https://github.com/frankxai/creator-intelligence-system/pull/{number}"
    if receipt["url"] != expected_url:
        fail(f"pull request #{number} has an incorrect URL")
    receipt_commits.add(receipt["mergeCommit"])
    receipt_commits.update(receipt["includedCommits"])
receipt_commits.update(item["commit"] for item in boundary["directCommits"])
actual_boundary = set(git("rev-list", release["targetSha"]).splitlines())
if receipt_commits != actual_boundary:
    fail("receipts must cover the exact alpha boundary")

for document in (changelog, notes, audit):
    if release["targetSha"] not in document:
        fail("release documents must name the immutable alpha boundary")
if "Candidate (unpublished)" not in changelog:
    fail("changelog must mark the candidate unpublished")
if "No Git tag or GitHub release has been published" not in readme:
    fail("README must state the unpublished release truth")
if "Repository release status — 2026-08-10" not in attestation:
    fail("attestation release-status clarification is missing")
if ledger["attestation"]["status"] != "protocol-document-not-release-receipt":
    fail("protocol attestation must not be treated as a release receipt")

expected_packages = {
    "creator-intelligence-system",
    "@cis/core",
    "@cis/voice",
}
manifest_names = {manifest.get("name") for manifest in package_manifests}
if manifest_names != expected_packages:
    fail("package manifest set is incomplete or unexpected")
for manifest in package_manifests:
    if manifest.get("version") != release["version"]:
        fail(f"{manifest.get('name')} version must match the candidate")
    if manifest.get("private") is not True:
        fail(f"{manifest.get('name')} must remain private")
package_state = ledger["packagePublishing"]
if package_state["status"] != "blocked":
    fail("npm publication must remain blocked")
if {item["name"] for item in package_state["packages"]} != expected_packages:
    fail("npm audit must cover every package name")
if any(item["registryStatus"] != "not-found" for item in package_state["packages"]):
    fail("npm audit must preserve the observed not-found state")

public = ledger["publicSurface"]
if public["primary"]["status"] != "repository-only":
    fail("GitHub must remain the declared primary surface")
if public["dedicatedProductionDomain"] is not None:
    fail("do not invent a dedicated production domain")

if "workflow_dispatch:" not in draft_workflow:
    fail("prerelease workflow must be manual-only")
if re.search(r"^  (push|pull_request|release|schedule):", draft_workflow, re.MULTILINE):
    fail("prerelease workflow may not have an automatic trigger")
if "environment: github-prerelease-draft" not in draft_workflow:
    fail("prerelease workflow must use its protected environment")
if "--draft" not in draft_workflow or "--prerelease" not in draft_workflow:
    fail("workflow may create only a draft prerelease")
if "gh release edit" in draft_workflow or "--latest" in draft_workflow:
    fail("workflow may not publish or promote a release")

existing_tag = git(
    "rev-parse",
    "--verify",
    f"refs/tags/{release['tag']}^{{commit}}",
    check=False,
)
if existing_tag and existing_tag != release["targetSha"]:
    fail("existing prerelease tag points to a different boundary")

mode = os.environ.get("RELEASE_MODE", "validate")
if mode == "github-prerelease-draft":
    approvals = ledger["approvals"]
    if release["status"] != "ready":
        fail("GitHub prerelease requires release.status=ready")
    for approval in (
        "validationComplete",
        "humanAttestationApproval",
        "humanPublicSurfaceAcknowledgement",
        "humanReleaseApproval",
    ):
        if not approvals[approval]:
            fail(f"GitHub prerelease requires {approval}")
    if os.environ.get("RELEASE_VERSION") != release["version"]:
        fail("workflow version must match the ledger")
    if os.environ.get("RELEASE_TARGET_SHA") != release["targetSha"]:
        fail("workflow target must match the ledger")
elif mode != "validate":
    fail(f"unknown RELEASE_MODE {mode!r}")

print(
    f"release contract ok: {release['tag']} {release['status']} at "
    f"{release['targetSha']}; npm={package_state['status']}"
)
