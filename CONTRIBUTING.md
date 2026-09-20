# Contributing

Changes to the governance specification should be treated as changes to a protocol, not casual documentation edits.

Before proposing a normative change:

1. State the failure mode or capability gap.
2. Identify which trust boundary changes.
3. Edit the canonical source under `spec/parts/`, run `python3 scripts/build_guide.py`, and commit both generated guide copies together.
4. Run `python3 scripts/build_guide.py --check`, `python3 scripts/validate_repo.py`, `python3 -m unittest discover -s tests -v`, and `python3 scripts/check_mutations.py` before opening a PR. Reference contracts under `spec/reference/` are embedded into both guides; test behavior with literal outputs and adversarial cases.
5. Update DESIGN/THREAT_MODEL when the trust model changes.
6. Add or update an example when semantics change.
7. Check that the proposal does not create a silent bypass for ordinary task ordering, verifier separation or evidence provenance.

Public contributions should use pull requests. No accepted plan-amendment file in an instantiated target repository should ever be edited in place.
