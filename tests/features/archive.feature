Feature: Repository archival

    The archival script should have predictable properties over time.

    First, changes to the output are intended to be additive only.

    Second, the script should come to a consistent final state regardless of
    reference; working from a stale file, a legacy file, or no file does not
    change the final output.

    Scenario: Raw download
        Given the output of the last tagged version for "MikeBishop/http2-certs"
        When the current script is called on "MikeBishop/http2-certs"
        Then the output is a superset of the last version

    Scenario Outline:  Reference files
        Given the <Reference Type> file is available
        When the script is called on "MikeBishop/http2-certs" with the reference file
        Then the output is the same
        But the error "<error>" is found on stderr

      Examples: Valid reference files
      | Reference Type     | error |
      | Stale              | None  |
      | Legacy             | None  |

      Examples: Invalid reference files
      | Reference Type     | error                            |
      | Wrong repo         | different repo                   |
      | Invalid magic      | does not appear to be generated  |
