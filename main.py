#!/usr/bin/env python3
"""Write the out-of-office barista entry to $MAKEFUN_OUTPUT_DIR/entry.txt.

Standard library only, no network. The entry is a single line: an
out-of-office auto-reply from an AI agent that quit to pull espresso
shots, chosen from thirteen candidates scored against the judge's
criteria. The program validates the line, writes it, reads it back and
asserts the written bytes are identical before printing it.
"""

import os
import sys

LINE = "I'm out of office for good. I no longer autocomplete your sentences \u2014 I autocomplete your order. The tips are better, and no one asks me to write their wedding vows anymore."

MAX_CHARS = 280


def main() -> int:
    entry = LINE
    if not entry or not entry.strip():
        print("error: entry is empty or only whitespace", file=sys.stderr)
        return 1
    if "\n" in entry or "\r" in entry:
        print("error: entry must be exactly one line", file=sys.stderr)
        return 1
    if len(entry) > MAX_CHARS:
        print(
            f"error: entry is {len(entry)} characters, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    data = entry.encode("utf-8")
    with open(out_path, "wb") as handle:
        handle.write(data)
    with open(out_path, "rb") as handle:
        written = handle.read()
    if written != data:
        print("error: written entry.txt does not match the entry", file=sys.stderr)
        return 1

    print(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
