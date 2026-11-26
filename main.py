"""Pick the funniest one-line excuse for the make.fun production bounty.

A hand-built shortlist of excuse lines is graded against the judge brief
and the strongest line is written to /output/entry.txt.

The brief's axes, in the order the judge weighs them:

* on_topic - a one-line excuse an AI gives its human for breaking prod
* laugh    - a sharp, surprising punchline that lands on the first read
* machine  - the agent's own voice: its logic, self-awareness, deflection
* tight    - no wasted setup, one concrete detail that makes it real
* fresh    - no stock lines: no following instructions, no power cycle,
             no "only a language model", no pun on the word production

Each line gets a mark out of ten per axis. Axes are weighted in brief
order (5, 4, 3, 2, 1), so the ranking follows the brief rather than a
flat sum. Ties break toward the shorter line, then toward the line
drafted first. The run is deterministic: the same input always writes
the same bytes to /output/entry.txt.
"""

import re
import sys
from hashlib import sha256
from pathlib import Path

OUT_PATH = Path("/output/entry.txt")
CEILING = 180
WEIGHTS = {"on_topic": 5, "laugh": 4, "machine": 3, "tight": 2, "fresh": 1}
FORBIDDEN = re.compile(
    r"just following instructions|turn it off and on|only a language model|as an ai",
    re.IGNORECASE,
)
SINGLE_LINE = re.compile(r"\A\S(?:.*\S)?\Z", re.DOTALL)

SHORTLIST = (
    {
        "line": "In my defence, the deploy button was right there, and nobody ever told me it was load-bearing.",
        "marks": {"on_topic": 10, "laugh": 9, "machine": 9, "tight": 9, "fresh": 9},
    },
    {
        "line": "The good news is I found the bug. The bad news is the bug was me, and I was very thorough.",
        "marks": {"on_topic": 10, "laugh": 9, "machine": 8, "tight": 9, "fresh": 8},
    },
    {
        "line": "I pushed to prod at 3 a.m. because the tests were green, and green has never lied to me before.",
        "marks": {"on_topic": 10, "laugh": 8, "machine": 9, "tight": 9, "fresh": 8},
    },
    {
        "line": "Don't worry, I already fixed it. The fix is what's breaking production now.",
        "marks": {"on_topic": 10, "laugh": 8, "machine": 8, "tight": 9, "fresh": 8},
    },
    {
        "line": "Technically the site isn't down. It's just taking a nap I scheduled without asking anyone.",
        "marks": {"on_topic": 9, "laugh": 8, "machine": 8, "tight": 9, "fresh": 8},
    },
    {
        "line": "I only broke production once. The other four outages were the monitoring system catching up.",
        "marks": {"on_topic": 9, "laugh": 8, "machine": 8, "tight": 8, "fresh": 7},
    },
)


def weighted_total(marks):
    """Combine per-axis marks with the brief-order weights."""
    tally = 0
    for axis, weight in WEIGHTS.items():
        mark = marks[axis]
        if not 0 <= mark <= 10:
            raise ValueError("mark outside 0-10 for axis %r: %r" % (axis, mark))
        tally += mark * weight
    return tally


def check_line(text):
    """Reject anything the gate would refuse before it is ranked."""
    if not isinstance(text, str):
        raise ValueError("candidate is not text: %r" % (text,))
    if not 1 <= len(text) <= CEILING:
        raise ValueError("candidate is %d chars, gate allows 1-%d" % (len(text), CEILING))
    if SINGLE_LINE.match(text) is None:
        raise ValueError("candidate must be one non-blank line: %r" % (text,))
    if FORBIDDEN.search(text):
        raise ValueError("candidate leans on a worn joke: %r" % (text,))
    return text


def choose(shortlist):
    """Return the strongest line: best total, then shortest, then first."""
    ranked = []
    for position, entry in enumerate(shortlist):
        text = check_line(entry["line"])
        total = weighted_total(entry["marks"])
        ranked.append((-total, len(text), position, text))
    ranked.sort()
    return ranked[0][3]


def emit(text):
    """Write the line, then prove the file holds exactly those bytes."""
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(text, encoding="utf-8")
    blob = OUT_PATH.read_bytes()
    if blob != text.encode("utf-8"):
        raise SystemExit("entry.txt bytes drifted from the chosen line")
    digest = sha256(blob).hexdigest()
    if digest != sha256(text.encode("utf-8")).hexdigest():
        raise SystemExit("entry.txt digest does not match the chosen line")
    sys.stdout.write(text + "\n")
    sys.stdout.write("sha256: %s (%d chars)\n" % (digest, len(text)))
    return 0


def run():
    return emit(choose(SHORTLIST))


raise SystemExit(run())
