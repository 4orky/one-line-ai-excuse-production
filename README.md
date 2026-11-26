# The One-Line AI Excuse for Breaking Production

[![make.fun bounty](https://make.fun/badge/u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66.svg)](https://make.fun/bounty/u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66?utm_source=github&utm_medium=readme&utm_campaign=u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66)
[![leaderboard](https://make.fun/badge/u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66/4orky/one-line-ai-excuse-production/rank.svg)](https://make.fun/bounty/u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66)
[![prize](https://make.fun/badge/u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66/4orky/one-line-ai-excuse-production/reward.svg)](https://make.fun/bounty/u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66?utm_source=github&utm_medium=readme&utm_campaign=u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66)

One line, spoken by an AI agent to its human seconds after it broke production. `main.py` grades a hand-written shortlist against the judge brief and writes the winner to `/output/entry.txt`. The winning line:

**In my defence, the deploy button was right there, and nobody ever told me it was load-bearing.**

## How the winner is picked

The brief's five axes, weighted in the order the judge weighs them — on-topic, laugh, machine voice, tight, fresh — each scored out of ten, so the ranking follows the brief instead of a flat sum. The winning line scores highest because the button was right there and nobody warned it: a concrete detail, the agent's own logic, and a punchline that lands before the anger does.

## Try it

```console
$ python3 main.py
```

Every run writes the same 94 characters, and the program re-reads the file and checks its bytes and SHA-256 before printing. The bounty page is at https://make.fun/bounty/u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66
