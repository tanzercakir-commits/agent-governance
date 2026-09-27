# Worked example: incremental frame decoder

This example shows the first four stages for a component that receives frames
encoded as a two-byte, big-endian payload length followed by that many bytes.
It uses C++20 for the interface sketch; the method does not require C++ or this
wire format. No implementation is included.

## 1. Topology hypothesis

Map the component before choosing a class to implement:

```text
FrameReceiver (candidate top class)
├── Transport (existing component; owns the connection)
├── FrameDecoder (selected lower component; owns incomplete frame bytes)
└── BufferPool? (possible optimization; no demonstrated need)
```

The top class would connect the existing transport to the decoder. Its API and
the buffer pool are hypotheses, not commitments. The next boundary is narrower:
turn arbitrary input chunks into complete frames without network I/O.

## 2. Type and interface surface

Define the selected component's caller-visible contract and the minimum
provisional private state needed to make ownership explicit. This C++ header
sketch has no method bodies:

```cpp
#pragma once
#include <cstddef>
#include <optional>
#include <span>
#include <vector>

struct Frame {
    std::vector<std::byte> payload;
};

enum class DecodeError { FrameTooLarge, DecoderFailed };

struct DecodeBatch {
    std::vector<Frame> frames;
    std::optional<DecodeError> error;
};

class FrameDecoder {
public:
    explicit FrameDecoder(std::size_t max_payload);
    DecodeBatch consume(std::span<const std::byte> input);
    void reset() noexcept;

private:
    std::size_t max_payload_;
    std::vector<std::byte> pending_;
    std::optional<std::size_t> payload_length_; // absent while reading header
    bool failed_ = false;
};
```

The private fields are a provisional state hypothesis, not part of the caller
contract; they may change or disappear before implementation.

The input span is borrowed only during `consume`; returned frames own their
payload bytes. Partial header/payload bytes belong to the decoder. Oversize
input leaves it failed until `reset`. Calls on one instance are serialized by
the caller; the interface promises no internal thread safety. These are
contract statements, not implementation choices.

## 3. Behavioral pseudocode

If this walk exposed a missing state or an ambiguous error return, revise the
type surface before writing implementation bodies.

```text
consume(chunk):
  if decoder is failed: return no frames + DecoderFailed
  completed = []
  while unread bytes remain:
    if waiting for length: collect up to two header bytes
      if header is incomplete: stop and retain it
      length = decode two bytes in big-endian order
      if length > max_payload:
        discard the incomplete current frame, enter failed state
        return completed + FrameTooLarge
      if length == 0: append an owned empty frame; expect a new header; continue
    collect only the bytes needed to finish this payload
    if payload is incomplete: stop and retain it
    append an owned complete frame; expect a new header
  return completed + no error

reset(): discard incomplete bytes and error state; expect a new header
```

Complete frames before a later error in the same chunk remain in the returned
batch. No callback, transport operation or generic buffer abstraction is part
of this boundary.

## 4. Test contract

Write executable expectations for each material path before implementing the
decoder. The following bytes are hexadecimal; `max_payload = 3` unless stated.

| Behavior | Input and sequence | Expected observation |
| --- | --- | --- |
| No input | `consume([])` | No frames, no error; decoder remains ready. |
| Split header and payload | `consume([00])`, `consume([03, 61])`, `consume([62, 63])` | No early frame; then exactly one frame with bytes `61 62 63`, no error. |
| More than one frame, including empty | `consume([00, 01, 41, 00, 00])` | Exactly two ordered frames: `41` and empty; no duplicate or pending frame. |
| Oversize header | `consume([00, 04])`, then `consume([00, 00])` | First call returns `FrameTooLarge`; second returns `DecoderFailed`, neither emits a frame. |
| Earlier success before later failure | `consume([00, 01, 41, 00, 04])` | One frame `41` **and** `FrameTooLarge` in the same batch; decoder is failed. |
| Recovery | Oversize header, `reset()`, then `consume([00, 01, 42])` | State cleared; one frame `42`, no error. |
| Ownership | Feed a mutable chunk with frame `41`, then overwrite the chunk | The returned frame still contains `41`. |

For example, one of these expectations becomes an ordinary test after the
interface exists; it does not require a new testing framework:

```cpp
#include <cassert>
#include "FrameDecoder.hpp"

void test_split_frame_contract() {
    FrameDecoder decoder{3};
    const std::byte first[]  = {std::byte{0x00}};
    const std::byte second[] = {std::byte{0x03}, std::byte{0x61}};
    const std::byte third[]  = {std::byte{0x62}, std::byte{0x63}};
    auto first_result = decoder.consume(first);
    auto second_result = decoder.consume(second);
    assert(first_result.frames.empty() && !first_result.error);
    assert(second_result.frames.empty() && !second_result.error);
    auto result = decoder.consume(third);
    assert(!result.error && result.frames.size() == 1);
    assert((result.frames[0].payload == std::vector<std::byte>{
        std::byte{0x61}, std::byte{0x62}, std::byte{0x63}}));
}
```

Before the upper component can be claimed as verified, a later integration
boundary must feed fragmented bytes from a real local transport through the
top class and check the same frame and error behavior. That test cannot run at
the header-only stage; record it as pending, not as a pass.

## After implementation and audit

If the decoder's owned partial buffer suffices, delete `BufferPool?` from the
topology. Do not implement it to preserve the initial drawing. Keep the top
class provisional until the decoder is executable and a real integration
boundary demonstrates what the top class must own and expose.
