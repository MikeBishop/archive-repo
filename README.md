# archive-repo
Captures and stores data about a GitHub repo for archival purposes

# Archive command

usage: python3 -m archive-repo archive [-h] [--reference [REFFILE]] [--issues-only] [--quiet] repo githubToken [outFile]

Archive repo issues and PRs.

positional arguments:
- `repo`:  The GitHub repository to fetch, e.g. "quicwg/base-drafts"
- `githubToken`:  A token for a GitHub account with permission to read the
  selected repository; see https://github.com/settings/tokens
- `outfile`:  Where the output should be written; if omitted, stdout is used.

optional arguments:
- `-h`: Displays help text
- `--reference`: Optionally, previous output of this script.  Makes the new run
  faster, since only new/changed issues and PRs need to be fetched.
- `--issues-only`:  Only fetch issues, not PRs
- `--quiet`:  Only write errors to stderr; otherwise, status is written to
  stderr

Note that providing an output file can make processing faster if the respository
has not changed since the reference file was generated.

# Generate PR Branches

usage: python3 -m archive-repo pr_branches [-h] [--include-merged] [--dry-run] input repo git_dir

Identify the source repos and forks of PRs from an archive, creating local branches as needed

positional arguments:
- `input`:  Archive file generated by `python3 -m archive-repo archive`
- `repo`:  Target GitHub repo
- `git_dir`:  Local directory with git repo (default: local directory)

optional arguments:
- `-h`: Display help message
- `--include-merged`: include merged PRs in analysis
- `--dry-run`: Show what would be done, without making any changes
