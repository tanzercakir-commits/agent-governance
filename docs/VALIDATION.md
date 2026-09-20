# Validation status

The repository provides the v0.1 guide and skill. The reference Python contracts
and their tests are executable specification evidence, not an installed runtime.

## Reproducible local checks

From the repository root, using Python 3.10 or later:

```bash
python3 scripts/build_guide.py --check
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 scripts/check_mutations.py
python3 scripts/package_release.py --output dist
```

The suite checks canonical PR-body hashing, literal task-region byte vectors,
durable/concurrent one-shot admission with a local SQLite test adapter, failure
and UNKNOWN outcomes, and generated-guide equality. The mutation check seeds
latest-success-only acceptance and an extra amendment separator into disposable
copies and requires their behavioral regressions to fail.

The release packager checks the standalone skill's local references and license,
constructs deterministic archives and verifies them after extraction. That is
file portability evidence; it does not demonstrate that every coding agent
correctly follows the skill.

The source suite currently contains 36 tests. Three source regressions also check
the exact PR-head checkout in both build jobs, the policy job's evidence-reading
permissions, and the hidden-ruleset-field attestation contract. These clause and
workflow checks do not prove the corresponding live GitHub behavior.
An additional offline regression checks the three token steps against the
reviewed action revision's required inputs; its fixture is included in source
exports. It detects the `client-id`/`app-id` mismatch found during commissioning.
The safe-startup regression checks that the workflow templates consistently use
Python 3.11+ `-P` with the protected governance import path. The receiving lab
also executes the actual commands under harmless root-module shadows; its
local evidence remains distinct from hosted-runtime and live acceptance.

## Live commissioning evidence

The [operational failure model](FAILURE_MODES.md) and the corresponding
AGENTS/MASTER_PROMPT rules were derived from commissioning observations. Source
validation and packaging check that the documentation and portable guide copies
are present and consistent. The existing executable contracts do not measure
compliance with these working practices, and the historical live results below
are not a before/after evaluation of their effect. Recurrence and cost reduction
remain unmeasured; objective project-specific controls need their own validation.

The private commissioning lab has independently verified these deployed flows:

| Flow | Retained evidence |
| --- | --- |
| Greenfield setup and a first real task | PR10, protected merge `c8f65acd`, historical main audit [35473132141](https://github.com/tanzercakir-commits/agent-governance-lab/actions/runs/35473132141) |
| Existing-repository adoption and a real task | Adoption-lab PR2, protected merge `c5a96cc4`, main audit [35500883610](https://github.com/tanzercakir-commits/agent-governance-adoption-lab/actions/runs/35500883610); four project tests and 86 governance tests; independent deployed acceptance passed |
| Zero, one and multiple discovered additions; owner-initiated amendment | Task PR10/14/17 and amendment PR16, with signed records, independent final reconciliation and successful deployed audits |
| Terminal queue and trusted owner reopening | Task PR27/main `67d924e2`, then amendment PR28/main `918231b4`; audits [35478836981](https://github.com/tanzercakir-commits/agent-governance-lab/actions/runs/35478836981) and [35479517957](https://github.com/tanzercakir-commits/agent-governance-lab/actions/runs/35479517957) |
| Invalid authorization, stale state and protected-path edits | Never-merge PR18–22; all attempt slots stayed absent |
| Corrupted signatures and cross-PR record replay | Never-merge PR25–26; actual signed-record reader rejected both |
| Controlled lost responses, later request failures and duplicate commands | Never-merge PR29–53; all 25 independently checked against signed records and actual workflow traces |

Earlier failed runs and attempt records are retained. Maintenance deployments
have separate evidence; their failed ordinary task audits are not reported as
successful governed tasks. Lab links remain private until separately published.

The controlled batch exercised actual GitHub requests: deliberately invalid test
credentials caused definite HTTP rejection, or the client discarded an actual
acknowledgement. These were injected client faults, not observed provider outages.
Twenty-two fixtures refused completion. PR43 and PR52 completed the protocol
despite a failed workflow after a lost final response; PR53 admitted one of two
authentic simultaneous owner commands and refused the other. Those three
fixtures remain never-merge tests, not completed project tasks. The duplicate
case exercised existing workflow serialization; it does not establish a raw
simultaneous claim-write race. The separate provider trial below covers that
boundary. Every observed run and immutable record was retained.

The live commissioning gates above are complete. Public v0.1 preparation also
requires the final distributable source/CI/artifact review and a clean repository
created from the public export. The original private development history is
retained separately; exporting ZIPs does not sanitize that existing repository.

The disposable adoption fixture was initially configured by the agent to require
one approving GitHub review, although the owner works with one account. That
test-setup mistake was explicitly corrected before adoption: the review count
changed from one to zero, with both baseline snapshots retained. Subsequent
adoption checks confirmed preservation of the original function/tests, strict
legacy CI, thread resolution, merge-only, no-bypass and immutable-record controls.
The task added a stdin CLI and two tests; original tests remained intact. It does
not establish preservation of the fixture's original one-review requirement.
This fixture correction does not change the protocol's requirement to preserve
stricter controls in actual receiving projects.

The lab has recorded pre-bootstrap trials with the actual minimal App token:
one-winner concurrent ref creation, denied update/delete and ruleset administration,
and detection of hidden bypass edit/restore, disable/restore and recreation.
Its [protection evidence](https://github.com/tanzercakir-commits/agent-governance-lab/blob/ed3c66e23d3b9f0d7969d00637a5a9c6db3236db/commissioning/PROTECTION_VALIDATION.md)
retains both preliminary and qualifying observations. The lab is currently private.
Independent review passed that checkpoint, and [hosted CI](https://github.com/tanzercakir-commits/agent-governance-lab/actions/runs/35463950097)
verified its exact commit, 57 governance tests and scaffold check. These results
establish the provider-protection checkpoint; later task acceptance is recorded
above, including the separately commissioned existing-repository adoption.

The ruleset timestamp assumption remains explicit: finite commissioning trials
are not a permanent provider guarantee. Runtime tokens retain minimal
contents/statuses permissions; missing bypass data is not treated as an empty
bypass list. Protection drift cannot be fixed by refreshing the attestation over
old attempt histories.

A local pass cannot mark those gates complete. Protected merges, signing-secret
or ruleset installation, history replacement and public visibility changes need
separate owner authorization. The source's original private review evidence is
retained in its development history; release ZIPs omit private review briefs and
Git history. That clean export does not sanitize the existing Git history.
