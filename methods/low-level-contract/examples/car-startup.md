# Worked example: from Car readiness to Engine startup

Start with the behavior of the whole system, then follow its obligations down
to the smallest component that must make them true. Verify those obligations
from the bottom back up. The point is not to implement every box in a drawing.

This is a **simplified, single-threaded simulation**, not a vehicle controller
or a claim about real vehicle safety. `Ready` means only that this simulated
startup operation completed with the engine running and the modeled brake
availability check passing. It does not mean safe to drive or roadworthy.

The example works through stages 1–4 of the
[Low-Level Contract Method](../METHOD.md). Its type declarations, pseudocode
and test expectations are design artifacts, not an executable implementation.
Stages 5–8 below describe the remaining work and evidence; none is reported as
completed. The method remains optional and non-normative unless selected for
a bounded task under the receiving project's existing governance rules.

## 1. Topology hypothesis

### Begin with the whole-system requirement

**R1:** `Car.start()` may report `Ready` only after its owned `Engine` is
`Running`. If startup fails, the caller receives the reason; an engine failure
must retain the engine's specific reason through the Car boundary.

For this example, Car also checks a simple brake-availability flag before
asking Engine to start. This establishes an ordering relationship without
trying to model a complete brake controller.

```text
Car (coordinates startup; owns its components)
├── Engine (owns startup state and a simulated ignition plan)
├── BrakeSystem (answers the narrow availability check)
├── Transmission? (provisional; no behavior selected here)
└── Dashboard? (provisional; no presentation behavior selected here)

Car.start → BrakeSystem.check → Engine.start → explicit Car result
```

These are composition relationships: Car **has an** Engine and BrakeSystem;
it does not inherit from them. Properties such as color or rated power, if a
later requirement needs them, are fields or value objects. `RedCar` and
`HighPowerEngine` subclasses are not justified merely by different values.
Neither those fields nor the provisional Transmission and Dashboard need to
be implemented for R1.

Choose **Engine startup as the first implementation boundary**. Keep only the
minimal Car and BrakeSystem caller contracts necessary to show why that lower
boundary exists. Do not implement all three components at once. The direction
of design pressure is:

| Whole-system obligation | Consequence for the lower contract |
| --- | --- |
| Car cannot report Ready while Engine is still starting. | `Engine.start()` must distinguish a request being issued from the engine actually reaching Running. |
| Car must explain failed startup. | Engine must return a specific failure value that Car can preserve. |
| A second start must not ignite an already running engine again. | Engine needs an explicit already-running outcome and a no-side-effect repeated-call rule. |
| A startup attempt cannot wait forever in the simulation. | Engine must have a bounded attempt and a timeout outcome, with cleanup specified. |

This is how a high-level requirement reaches a low-level API. A generic
`void Engine.start()` that silently returns on both success and failure gives
Car no evidence for R1. A void-returning API could work with a separately
specified exception, status or asynchronous completion contract, but none is
implicit here. This example chooses an explicit result whose successful
variants guarantee that Engine is already Running when the call returns.

## 2. Type and interface surface

The following language-neutral declarations contain no implementation bodies.
`A | B` denotes a tagged union: exactly one listed variant is present. All
durations are nonnegative integer virtual milliseconds. The attempt deadline
is fixed at 100 ms for this teaching example, not a recommended physical value.

```text
EngineState = Stopped | Starting | Running | Failed
EngineFailure = NoFuel | IgnitionRejected | TimedOut
EngineStartResult = Started | AlreadyRunning | Failed(reason: EngineFailure)

SimulatedIgnition =
    Completes(afterMs: NonNegativeInteger,
              outcome: Ignited | NoFuel | IgnitionRejected)
  | NeverCompletes

Engine:
  create(plan: SimulatedIgnition) -> Engine
  start() -> EngineStartResult
  state() -> EngineState

BrakeStatus = Available | Unavailable
BrakeSystem:
  create(status: BrakeStatus) -> BrakeSystem
  check() -> BrakeStatus

CarState = Idle | Starting | Ready | Failed
CarFailure = BrakeUnavailable | EngineFailed(reason: EngineFailure)
CarStartResult = Ready | Failed(reason: CarFailure)

Car:
  create(ownedEngine: Engine, ownedBrakes: BrakeSystem) -> Car
  start() -> CarStartResult
  state() -> CarState
  engineState() -> EngineState
```

Qualify same-spelled variants by their type where needed. For example,
`EngineStartResult.Failed(NoFuel)` is an operation result, whereas
`EngineState.Failed` is a state. `Car.engineState()` is a read-only observation
of its owned Engine for this simulation; it does not expose mutable ownership.

### States, ownership and lifetime

- A new Engine is Stopped. A new Car is Idle. Car takes exclusive ownership
  of both components for its lifetime; the caller cannot start or mutate that
  Engine through another alias.
- Calls on one Car or Engine are serialized and non-reentrant. No internal
  thread safety is promised. The simulation has no independent stalls,
  background state changes or brake-status changes between calls.
- Both `start()` operations are synchronous. Starting is a transient internal
  state, never a returned terminal result. `Engine.start()` finishes in Running
  or Failed; `Car.start()` finishes in Ready or Failed. Callers cannot call
  again during Starting under the serialized-call rule.
- The minimum provisional Engine state is a state tag, its owned simulation
  plan and an optional stored failure reason. Failed has exactly one reason;
  other states have none. Car needs its owned components and a state tag.
  These storage choices may change without weakening the caller contract.
- The bounded simulated attempt is internal behavior, not a new public
  `IgnitionService` hierarchy. The plan supplies deterministic virtual events;
  no hardware, wall-clock sleep, resource thread or external I/O is involved.

### Engine postconditions

| State before call | Result | State after call and side effects |
| --- | --- | --- |
| Stopped; ignition succeeds before 100 ms | `Started` | Running; exactly one attempt. |
| Stopped; failure is observed before 100 ms | `Failed(NoFuel)` or `Failed(IgnitionRejected)` | Failed; preserve that reason; exactly one attempt. |
| Stopped; no completion before 100 ms | `Failed(TimedOut)` | Failed; cancel the pending simulated completion; exactly one attempt. |
| Running | `AlreadyRunning` | Remains Running; no new attempt or virtual-time advance. |
| Failed with reason `r` | `Failed(r)` | Remains Failed with the same reason; no new attempt or virtual-time advance. |

An event at exactly 100 ms is too late: timeout wins. A canceled or later event
cannot turn Failed into Running. There is no reset, stop or retry API in this
boundary. A new simulation instance is needed for another attempt after
failure. That deliberate rule avoids inventing recovery semantics.

### Car postconditions

Car checks brakes first on every call. Unavailable brakes yield
`Failed(BrakeUnavailable)`, set Car to Failed and leave Engine untouched.
When brakes are available, Car calls Engine exactly once:

- `Started` or `AlreadyRunning` permits Car to enter Ready and return Ready.
  Both Engine outcomes require `engineState() == Running` at that point.
- `Failed(r)` makes Car enter Failed and return `Failed(EngineFailed(r))`.
  Car must not replace the reason with a generic startup error.

A repeated successful Car start returns Ready after the Engine's
AlreadyRunning path, without another ignition attempt. A repeated failed
start returns the same reason with these immutable simulation inputs. Car
does not trust a cached Ready flag instead of following the component contract.
No callbacks, public mutable fields or additional component APIs are needed.

## 3. Behavioral pseudocode

Work out the lower operation first, then check that its caller can actually
fulfill R1. If the walk reveals missing information, revise stage 2 before
writing implementation bodies.

```text
Engine.start():
  if state is Running:
    return AlreadyRunning
  if state is Failed:
    return Failed(stored reason)

  require state is Stopped              // Starting calls are outside the contract
  set state to Starting
  begin one simulated attempt at virtual elapsed time 0
  observe the plan until completion or the 100 ms deadline:
    if the plan completes at a time strictly less than 100 ms:
      if its outcome is Ignited:
        finish the attempt; set state to Running
        return Started
      otherwise:
        finish the attempt; store the exact NoFuel or IgnitionRejected reason
        set state to Failed
        return Failed(stored reason)
    otherwise:
      cancel the pending simulated completion; store TimedOut
      set state to Failed
      return Failed(TimedOut)

Car.start():
  set state to Starting
  if owned brakes.check() is Unavailable:
    set state to Failed
    return Failed(BrakeUnavailable)      // do not call Engine.start()

  result = owned engine.start()
  match result:
    Started or AlreadyRunning:
      // Engine's postcondition guarantees Running before this line
      set state to Ready
      return Ready
    Failed(reason):
      set state to Failed
      return Failed(EngineFailed(reason))
```

The success return comes **after** the lower state transition. Moving it to
the point where the ignition request is merely issued would break the Car
requirement, even if the engine usually becomes Running later. Likewise,
discarding the error here would force Car either to guess or to lose R1's
failure information. Tests of the Engine postcondition are therefore part of
the evidence needed for the Car claim.

## 4. Test contract

These are explicit expected assertions to turn into executable tests before
implementation. They are **not test results**. Use a deterministic virtual
clock and fixture event log to observe attempt count, ordering and cancellation;
these are test instrumentation, not new production interfaces. Each row starts
with a fresh instance unless it specifies a sequence.

### Engine unit expectations

| ID | Setup and action | Expected assertions |
| --- | --- | --- |
| E1 | New Engine, `Completes(0, Ignited)`; call start. | Initially Stopped; result Started; final state Running; one attempt; Running recorded before returning Started. |
| E2 | `Completes(99, Ignited)`; call start. | Started and Running at virtual 99 ms; no timeout. |
| E3 | `Completes(0, NoFuel)`; call start. | Failed(NoFuel); final state Failed; reason retained; one attempt. |
| E4 | `Completes(20, IgnitionRejected)`; call start. | Failed(IgnitionRejected); final state Failed; reason retained; one attempt. |
| E5 | `NeverCompletes`; call start. | Failed(TimedOut) at virtual 100 ms; final state Failed; pending attempt canceled; no later transition. |
| E6 | `Completes(100, Ignited)`, then separately `Completes(101, Ignited)`; call start and advance the fixture beyond 101 ms. | Both time out at 100 ms; both remain Failed afterward; neither late event produces Started or Running. |
| E7 | Complete E1, then call start twice more. | Both later results AlreadyRunning; Running throughout; total attempts remains one; no additional virtual time. |
| E8 | For each of E3–E6, call start again after failure. | Same exact failure reason; Failed throughout; total attempts remains one; no additional virtual time. |

The typed plan rejects negative durations and unknown outcomes at construction
of its values. There is no untyped parsing boundary here. Concurrent calls are
outside this contract, so a concurrency test cannot establish a guarantee the
interface never made. A later concurrency requirement must revise stages 1–4.

### Car composition and integration expectations

Each of the following requires the real simulation Engine and BrakeSystem
composed in Car, rather than only a stub that always reports success.

| ID | Setup and action | Expected assertions |
| --- | --- | --- |
| C1 | Available brakes; Engine `Completes(20, Ignited)`; call Car.start. | Initially Car Idle and Engine Stopped; trace orders brake check, engine attempt, Engine Running, Car Ready, return Ready; both states match on return. |
| C2 | Unavailable brakes; otherwise successful Engine plan; call Car.start twice. | Both calls fail with BrakeUnavailable; Car Failed; Engine remains Stopped; zero engine calls and attempts. |
| C3 | Available brakes; separately use E3, E4 and E5 plans; call Car.start. | Failed(EngineFailed(NoFuel)), Failed(EngineFailed(IgnitionRejected)) and Failed(EngineFailed(TimedOut)), respectively; both components' relevant states Failed; Car never enters or reports Ready. |
| C4 | Available brakes; repeat the exact-deadline and late-success plans from E6. | Car fails with EngineFailed(TimedOut), never reports Ready, and remains Failed after advancing virtual time past the canceled event. |
| C5 | Complete C1, then call Car.start again. | Ready again with Engine Running; brakes checked again; second Engine result AlreadyRunning; total ignition attempts remains one. |
| C6 | After each C3 failure, call Car.start again. | Same nested Engine failure reason; no new ignition attempt; no Ready result. |

For example, C3's timeout assertions would read as follows in the receiving
project's ordinary test framework. This remains a test sketch, not runnable
code supplied by this document:

```text
car = Car.create(Engine.create(NeverCompletes), BrakeSystem.create(Available))
assert car.state() == Idle
result = car.start()
assert result == Failed(EngineFailed(TimedOut))
assert car.state() == Failed
assert car.engineState() == Failed
assert fixture.ignitionAttemptCount == 1
assert fixture.virtualElapsedMs == 100
assert fixture.pendingCompletionCount == 0
assert fixture.trace contains no Car.Ready transition

again = car.start()
assert again == result
assert fixture.ignitionAttemptCount == 1
assert fixture.virtualElapsedMs == 100
```

The Engine suite alone cannot prove Car's error mapping or ordering. The Car
suite alone, if it substitutes a success-only fake Engine, cannot prove the
lower state/result relationship. Both levels must pass on the same implemented
contracts before claiming the simulation meets R1. Repository documentation
checks are separate and cannot substitute for either suite.

## 5. Implementation — pending

Implement Engine only after reviewable stages 1–4 are agreed. Use its focused
tests to establish the state/result and timeout behavior. Keep the internal
simulation machinery as small as the demonstrated behavior permits; the
provisional storage and initial component drawing are not implementation duties.
No runtime implementation or executable startup tests are included here.

## 6. Executable verification — pending

Run E1–E8 against the implemented Engine, plus the receiving project's required
build and CI checks. Record the exact revision, commands and results. A type
sketch compiling or a documentation check passing would not prove these
behavioral assertions. Car integration checks C1–C6 remain pending until its
separate boundary is implemented. There are no physical-environment checks in
this simulation scope; substituting real hardware would require a new contract
and appropriate real-environment evidence, not a reuse of this safety disclaimer.

## 7. Audit — pending

Compare implementation and observed tests against R1, the type surface,
pseudocode and expectations. In particular, inspect every Started return for
a preceding Running transition, every failure path for reason preservation,
and every repeated/late-completion path for extra attempts or state changes.
List mismatches and unrun checks rather than treating planned tests as passes.
Use an independent reviewer when the project's selected governance profile or
local rules require one. No implementation audit has occurred in this example.

## 8. Next demonstrated boundary — planned, not proven

After Engine's implementation, verification and audit, take Car's actual
composition as the next bounded loop. Revisit its minimal caller contract in
stages 1–4, then implement and execute C1–C6. This verifies upward:

```text
Engine's state/result guarantee
  → Car's real component call order and reason mapping
    → observed evidence for whole-system requirement R1
```

Remove Transmission and Dashboard from the active implementation plan while
they have no demonstrated behavior. Do not build them to make the initial
diagram look complete. A real second use might later justify shared startup
logic; two similar class names in the sketch do not justify a generic framework.

What exists now is a reviewable chain of obligations and test expectations.
What remains unproven is every executable claim about Engine and Car. Even
after those simulation checks pass, they would establish only this bounded
startup behavior, not vehicle safety, release readiness or governance approval.
