"""The Most Shameless Lie -- make.fun micro entry.

Writes the entry text to MAKEFUN_OUTPUT_DIR/entry.txt.
Standard library only; no network access.
"""

import os
import tempfile

ENTRY = "I paid the rent."

MIN_WORDS = 1
MAX_WORDS = 5
MAX_CHARS = 88


def validate(entry):
    if not entry or not entry.strip():
        raise ValueError("entry must not be blank or only whitespace")
    words = entry.split()
    if len(words) < MIN_WORDS or len(words) > MAX_WORDS:
        raise ValueError(
            "entry must be between %d and %d words, got %d"
            % (MIN_WORDS, MAX_WORDS, len(words))
        )
    if len(entry) < 1 or len(entry) > MAX_CHARS:
        raise ValueError(
            "entry must be between 1 and %d characters, got %d"
            % (MAX_CHARS, len(entry))
        )


def main():
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, target)
        with open(target, "rb") as f:
            if f.read() != data:
                raise RuntimeError("read-back verification failed: entry.txt differs from written bytes")
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
