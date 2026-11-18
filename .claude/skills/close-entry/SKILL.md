---
name: close-entry
description: "Close a finished backlog entry (BUG-N, FEAT-N): delete it or move it to docs/RESOLVED.md, fix every reference and commit. Use when an entry's work is done and verified on the keyboard, or when the user asks to close one."
---

# Close a backlog entry

Rules: `docs/DEVELOPER-GUIDE.md` §1 steps 5-6 and §3. Arguments: the
ID(s) to close.

1. **Check it's really done.** Every Implementation Plan step is
   **Done**, and the firmware was verified on the keyboard by the user
   (§1 step 5), not just built green. Record what the user actually
   reported, in their words where possible: never claim a check they
   didn't report. If a step is open, say so and stop: finish it or ask
   the user to drop it explicitly.
2. **Decide: delete, or move to `RESOLVED.md`.** Move only if the
   resolution taught something non-obvious (a ZMK behavior, an AZERTY
   trap, a build quirk). If unsure, ask. A `RESOLVED.md` entry keeps the
   ID and title, gets a `**Closed:** <date>` line, how it was verified,
   and the lesson in a few paragraphs, not a copy of the plan.
3. **Fix every reference.** `git grep -nw '<ID>'` across the repo:
   keymap and `.conf` comments, `README.md`, the guide, other entries'
   `Depends on` lines, `tools/`, `.github/workflows/` and
   `docs/HANDOFF.md`. Each one points to `docs/RESOLVED.md#<anchor>`,
   drops the dependency, or is reworded. Comments that explain why a
   key is where it is may keep the ID if it now resolves in
   `RESOLVED.md`. Don't touch `RESOLVED.md`'s historical mentions.
4. Run `git grep -nw '<ID>'` once more to check nothing stale is left.
5. Commit as `docs(<ID>): close it - <why it's done>` with "Effect on
   push: docs only" (check that's true: a `.keymap` or `.conf` comment
   edit starts a firmware build, so it goes through `ship-firmware`).
   Don't push without approval.
