# Public v0.1 STRICT release checklist

> Historical STRICT release evidence. The v0.2 PRACTICAL/REVIEWED profile guidance is not validated by this checklist.

> Evidence availability, 2026-09-24: the historical lab repositories have been
> deleted. Checked items below record the original v0.1 review, not current
> access to its private logs or records. See [validation status](docs/VALIDATION.md)
> for the access limits and [current versions](README.md#versions) for releases.

- [x] Independent source review, including safe-startup commissioning corrections, passed at `e85eac8` on 2026-09-20; hosted CI `35478614113` verified the same commit/tree. Live enforcement remains separate below.
- [x] Root guide and Skill reference copy are byte-identical.
- [x] Agent Skill frontmatter and standalone package extraction/reference resolution are tested; host-agent behavioral commissioning remains separate.
- [x] Greenfield lab bootstrap and its first real task are verified through deployed historical main audit `35473132141`; independent deployment/acceptance review passed on 2026-09-20. Remaining commissioning flows are listed separately below.
- [x] Existing-repository adoption and its first real task independently passed: PR2, normal merge `c5a96cc4`, main audit `35500883610`, four project tests and 86 governance tests. Original code/tests, strict legacy CI, thread resolution, merge-only and no-bypass controls were preserved against the agreed baseline. The disposable fixture's agent-added one-review requirement was explicitly corrected before adoption; preservation of that original requirement is not claimed.
- [x] First real task PR10 completed exact-source CI → independent verifier → trusted finalization → normal protected merge `c8f65acd` → historical main audit `35473132141` using repaired main `a2d6c7ed`. Failed earlier audit runs remain preserved.
- [x] PR14 finalized two discovered additions in order (`LAB-M0-003,LAB-M0-004`) and created canonical `PA-0001`; normal merge `269e7106` and main audit `35473975700` passed.
- [x] Owner-initiated PA-0002 completed through `/project amend-plan` in PR16: TODO-only candidate, independent final reconciliation, normal protected merge `aea844c5`, build `35475360233` and main audit `35475360235` PASS.
- [x] Terminal state completed in PR27/main `67d924e2` (audit `35478836981`), then only trusted owner PA-0004 reopened TODO in PR28/main `918231b4` (audit `35479517957`); both deployed states independently accepted, PROGRESS/history preserved.
- [x] Independent live review passed stale SHA, changed body, self-verification, historical amendment edit and direct TODO edit in never-merge PR18–22 at `aea844c5`; all twenty attempt slots stayed absent. PR5 separately preserves generic Actions final-status spoof rejection and environment denial evidence.
- [x] Controlled live lost-response, duplicate-command and post-publication failure cases passed in PR29–53: 25 independent outcome audits, 37 retained run logs, 38 old plus 66 new immutable refs preserved. Three never-merge fixtures finalized; 22 correctly refused. Duplicate commands used ordinary workflow serialization.
- [x] Pre-bootstrap lab trials validate minimal-token tag-ruleset views and hidden bypass edit/restore detection, including a same-second pair; independently reviewed at lab `ed3c66e`. This is finite provider-behavior evidence, not a permanent guarantee; drift cannot re-attest existing histories.
- [x] No private/bootstrap-only self-writing workflow remains in the distributable tree.
- [x] Design distinctions describe the actual protocol, without competitor names, links or unsupported uniqueness claims; independently reviewed on 2026-09-19.
- [x] MIT license is selected and added, including the standalone Skill copy.
- [x] Repository description/topics are set.
- [x] Public README wording is reviewed for claims that exceed tested behavior.
- [x] The allowlisted public export excludes private bootstrap/review files and Git history. Publication uses a separate fresh repository; the original private development history is retained.

Publication requires successful hosted CI and independent artifact review of the
exact clean candidate, followed by the owner or their authorized delegate's final
decision. Only the clean repository may become public.

Local checks and their limits are described in [validation status](docs/VALIDATION.md).
The source and standalone Skill candidate ZIPs are deterministic for the same
source and Python/zlib toolchain and include SHA-256 checksums. They omit private
review briefs and Git history. Exporting them does not clean the existing Git
history, commission a target repository, authorize a merge or publish v0.1.
