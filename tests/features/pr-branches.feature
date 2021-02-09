Feature: PR Mapping to Branches

Scenario: Branch Creation
    Given a repo for "MikeBishop/http2-certs"
    When the current script is called on "MikeBishop/http2-certs"
    And pr-branches is executed for "MikeBishop/http2-certs"
    Then a branch named "pulls/15" pointing to "025871fab93271ed9adae051c821d84521a2083c" is created