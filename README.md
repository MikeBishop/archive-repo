# archive-repo
Captures and stores data about a GitHub repo for archival purposes

# Usage

    archive.py [-h] [--reference [REFFILE]] [--issues-only]
               [--quiet]
               repo githubToken [outFile]

- `-h`: Displays help text
- `--reference`: Optionally, previous output of this script.  Makes the new run
  faster, since only new/changed issues and PRs need to be fetched.
- `--issues-only`:  Only fetch issues, not PRs
- `--quiet`:  Only write errors to stderr; otherwise, status is written to
  stderr
- `repo`:  The GitHub repository to fetch, e.g. "quicwg/base-drafts"
- `githubToken`:  A token for a GitHub account with permission to read the
  selected repository; see https://github.com/settings/tokens
- `outfile`:  Where the output should be written; if omitted, stdout is used.

Note that providing an output file can make processing faster if the respository
has not changed since the reference file was generated.