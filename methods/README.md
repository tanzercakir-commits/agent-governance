# Working Methods

Methods are optional development workflows. They describe how to do a task;
PRACTICAL, REVIEWED and STRICT governance profiles determine what must be true
before the task can be accepted. Methods are non-normative by default.

An owner may select a method for a bounded task through its existing authorized
scope or decision record. Without explicit selection, the project owes no
method artifacts or additional CI status. Using a method does not replace the
checks required by the chosen governance profile.

## Low-Level Contract Method

Best for complex low-level components, concurrency or lifetime-sensitive code,
difficult rewrites, and work where design and implementation tend to drift.

Flow: topology → type and interface surface → behavioral pseudocode → test
contract → implementation → executable verification → audit → next demonstrated
boundary.

[Read the Low-Level Contract Method](low-level-contract/METHOD.md).
