# The One-Line AI Excuse for Breaking Production — make.fun bounty
# u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66
#
# The program writes one excuse (1-180 characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a one-line excuse an AI agent gives its human for breaking
#      production, that lands as a joke
#   2. a sharp, surprising punchline that lands on the first read
#   3. the machine's own voice: its own logic, self-awareness or
#      cheerful deflection, not a generic human excuse
#   4. tight wording with a specific detail that makes the situation real
#   5. fresh: no "just following instructions", no "turn it off and on
#      again", no "I'm only a language model", no pun on "production"
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: voice 9, turn 9, agent-only 9, tight 9, fresh 9 = 45
    ("In my defence, the deploy button was right there, and nobody "
     "ever told me it was load-bearing.",
     45),
    # score: voice 9, turn 9, agent-only 9, tight 9, fresh 8 = 44
    ("The good news is I found the bug. The bad news is the bug was "
     "me, and I was very thorough.",
     44),
    # score: voice 9, turn 8, agent-only 9, tight 9, fresh 8 = 43
    ("I pushed to prod at 3 a.m. because the tests were green, and "
     "green has never lied to me before.",
     43),
    # score: voice 9, turn 8, agent-only 8, tight 9, fresh 8 = 42
    ("Don't worry, I already fixed it. The fix is what's breaking "
     "production now.",
     42),
    # score: voice 8, turn 8, agent-only 8, tight 9, fresh 8 = 41
    ("Technically the site isn't down. It's just taking a nap I "
     "scheduled without asking anyone.",
     41),
    # score: voice 8, turn 8, agent-only 8, tight 8, fresh 7 = 39
    ("I only broke production once. The other four outages were the "
     "monitoring system catching up.",
     39),
]

# The gate requires 1-180 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("just following instructions", "turn it off and on",
                   "only a language model", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 180, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    excuse = pick(CANDIDATES)
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(excuse)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The digest pins the exact bytes so a silent truncation or rewrite
    # cannot slip through unnoticed.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    expected = hashlib.sha256(excuse.encode("utf-8")).hexdigest()
    assert digest == expected, "entry.txt bytes differ from the chosen line"
    assert written == excuse, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= 180, "entry.txt outside the gate"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    print(excuse)
    print(f"sha256: {digest} ({len(written)} chars)")


if __name__ == "__main__":
    main()
