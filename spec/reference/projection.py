"""Normative byte framing; target repositories also validate task semantics."""
import re

MARKER = b"<!-- governance:tasks -->\n\n"
TERMINAL = b"_Queue complete._\n"
TASK_HEADER = re.compile(r"### ([A-Z][A-Z0-9]*-[A-Z0-9]+-[0-9]{3}) — (\S[^\n]*)\n")


def _text(value: bytes) -> str:
    if not isinstance(value, bytes):
        raise ValueError("expected bytes")
    try:
        text = value.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ValueError("invalid UTF-8") from error
    if "\r" in text or "\x00" in text or "\ufeff" in text:
        raise ValueError("noncanonical encoding")
    return text


def task_id(block: bytes) -> str:
    text = _text(block)
    match = TASK_HEADER.match(text)
    if not match or not block.endswith(b"\n") or block.endswith(b"\n\n"):
        raise ValueError("task header or final LF")
    body = text[match.end():]
    if not body.strip("\n") or re.search(r"^### |^_Queue complete\._$", body, re.M):
        raise ValueError("empty or mixed task block")
    if "<!-- governance:tasks -->" in text:
        raise ValueError("reserved marker in task")
    return match.group(1)


def parse_todo(before: bytes) -> tuple[bytes, tuple[bytes, ...]]:
    _text(before)
    if before.count(b"<!-- governance:tasks -->") != 1 or MARKER not in before:
        raise ValueError("missing or ambiguous task region")
    header, region = before.split(MARKER)
    if not header.startswith(b"# ") or not header.endswith(b"\n\n"):
        raise ValueError("header framing")
    if re.search(br"^### ", header, re.M):
        raise ValueError("task outside region")
    prefix = header + MARKER
    if region == TERMINAL:
        return prefix, ()
    starts = [m.start() for m in re.finditer(br"^### ", region, re.M)]
    if not starts or starts[0] != 0:
        raise ValueError("invalid task region")
    blocks = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(region)
        block = region[start:end]
        if index + 1 < len(starts):
            if not block.endswith(b"\n\n"):
                raise ValueError("missing block separator")
            block = block[:-1]  # Remove exactly the separator LF, never trim.
        task_id(block)
        blocks.append(block)
    ids = [task_id(block) for block in blocks]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate task ID")
    return prefix, tuple(blocks)


def project_amendment(before_todo: bytes, new_blocks: list[bytes]) -> bytes:
    header, pending = parse_todo(before_todo)
    if not isinstance(new_blocks, (list, tuple)) or not new_blocks:
        raise ValueError("nonempty ordered additions required")
    ids = [task_id(block) for block in (*pending, *new_blocks)]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate task ID")
    rendered = b"\n".join(new_blocks)
    return before_todo + b"\n" + rendered if pending else header + rendered
