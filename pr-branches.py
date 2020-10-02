#!/usr/bin/env python3

import argparse
import os
import sys
import shared.archive_reference as archive_reference

parser = argparse.ArgumentParser(
    description="Identify the source repos and forks of PRs from an archive"
)
parser.add_argument("input", help="GitHub archive file")
parser.add_argument("git_dir", help="Local directory with git repo", default=".")
parser.add_argument(
    "--include-merged",
    dest="merged",
    default=False,
    action="store_true",
    help="include merged PRs in analysis",
)
parser.add_argument(
    "--dry-run",
    dest="dryRun",
    default=False,
    action="store_true",
    help="Show what would be done, without making any changes",
)
parser.add_argument("repo", help="target GitHub repo")
args = parser.parse_args()

reference = archive_reference.loadReference(args.input, args.repo)

target_prs = (
    reference.prs.values()
    if args.merged
    else (pr for pr in reference.prs.values() if pr["state"] != "MERGED")
)
commits = {pr["headRefOid"] + ":pulls/" + str(pr["number"]) for pr in target_prs}

if any(commits):
    output = list()
    output.append("https://github.com/" + args.repo)
    output.extend(commits)
    command = "git -C " + args.git_dir + " fetch "
    command += "--dry-run " if args.dryRun else ""
    command += " ".join(output)
    os.system(command)
else:
    print("Nothing to do")
