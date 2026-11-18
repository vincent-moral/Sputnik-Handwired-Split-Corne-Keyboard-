# Handoff (2026-11-18)

Temporary note for resuming in a new session. Delete it once the items
below are closed. The authoritative state is the TODO files,
`docs/RESOLVED.md` and git history. Read `docs/DEVELOPER-GUIDE.md` first
(CLAUDE.md imports it); its "Handoffs" section defines this file's shape.

## Goal

The keyboard is the user's daily driver and the firmware is stable
(BUG-9's balanced Low and Raise, flashed 2026-10-25). They're practising
on keybr and Monkeytype now. What's left is small items that wait on
the user, and two studies that only come back if the practice asks for
them.

## Problems we're solving

- **FEAT-9** ([entry](TODO-features.md#feat-9-single-key-shortcuts-on-the-nav-layer)):
  step 4, the review "is it used?", was due around 2026-11-06 and is
  **overdue**. Ask the user; if unused, remove the keys (a firmware
  change).
- **BUG-8** ([entry](TODO-bugs.md#bug-8--is-a-dead-key-on-the-work-pc)) and
  **FEAT-4** ([entry](TODO-features.md#feat-4-workspace-switching-by-number-on-niri-and-cosmic)):
  blocked on the work PC's `localectl status` and
  `~/.config/niri/dms/binds.kdl`. The user forgot them twice (last asked
  2026-11-01).
- **FEAT-6** ([entry](TODO-features.md#feat-6-home-row-mods-that-only-trigger-with-the-other-hand)):
  fast typing gives `fi` instead of `I` (reported 2026-11-01). Candidate:
  a shorter `tapping-term-ms` on `hsl`/`hsr`. The user chose practice
  first; tuning waits for a measurement (FEAT-19).
- **FEAT-19** ([entry](TODO-features.md#feat-19-study-measuring-typing-per-key-and-the-firmwares-decisions)):
  study only, no decision taken. The user checks whether keybr's
  profile page can export data. A custom trainer comes back only if
  they want per-key stats and hold-tap tuning.
- **FEAT-8** (rewrite or close when accents are next discussed),
  **FEAT-18**, **BUG-5**: no action pending.

## Main files

- `config/corne_hw.keymap`: `hsl`/`hsr` (FEAT-6 timing), `ltsl`/`mtsl`
  (BUG-9), the nav layer (FEAT-9).
- `tools/key-check.html`: the verification page (pinned artifact
  https://claude.ai/artifact/Lykm8JfAtP6KVqetzvraFx, version 6); its
  checklist still holds BUG-9's checks.
- `.claude/skills/`, `AGENTS.md`: added 2026-11-18, copied and adapted
  from `homelab-iac`.

## What failed (don't repeat)

- **Pushed to `dev` without asking** (BUG-6). Every push needs its own
  approval, `dev` included; "you can push to dev" for one change doesn't
  cover the next.
- **Claimed checks the user hadn't reported** (BUG-9 "digits too").
  Write only what the pasted report says; the rest is "not reported".
- **A Kconfig claim without reading the build** (BUG-6 said our Kconfig
  set `ZMK_USB=y`; it was nice!nano's defconfig). Read the build log
  and the board files before explaining a Kconfig value (R3).
- **Said a web page could measure the hold time of `f`.** It can't: an
  undecided hold-tap holds back later key events and replays them, so
  only the keyboard (ZMK's USB log) sees real timing (FEAT-19).
- **`git rebase --autosquash` needs `-i`** on git 2.43, which isn't
  available here. To squash a fixup: detached checkout of the target,
  `cherry-pick -n` the fix, `commit --amend`, cherry-pick the rest,
  `git branch -f main`.
- **The scratchpad is wiped between sessions:** the key-check page was
  lost twice. It now lives in `tools/`; read the artifact by URL
  (`path: index.html`) if the file is ever behind.
- **zsh treats `=====` as a command** (`=` expansion) in an echo. Use
  `---` as a separator.

## Plan

1. Ask about FEAT-9's use (overdue). If unused: remove the keys with
   `keymap-change`, then `ship-firmware`; if used, close it with
   `close-entry`.
2. When the user brings the work-PC dumps: BUG-8, then FEAT-4. Check:
   `localectl status` shows the layout and variant; `binds.kdl` lists
   the workspace bindings.
3. When the user reports on keybr's export: update FEAT-19's
   Prerequisites, nothing else.
4. FEAT-6 only if the user asks for tuning: measure first (ZMK USB log,
   FEAT-19), then change `tapping-term-ms`.

## Waiting on the user

- FEAT-9: is the nav layer's undo/copy/paste row used?
- Work-PC dumps for BUG-8 and FEAT-4.
- keybr's data export (FEAT-19).
- Approval to push the 2026-11-18 commits (skills, guide, handoff, the
  build's `.claude/**` ignore).

## Working agreements

- Push only with explicit approval for each push. Firmware goes to `dev`
  first, `main` is fast-forwarded after a green build, then `dev` is
  deleted. Docs-only commits go straight to `main`, still with approval.
- The user flashes only binaries built by GitHub Actions; the
  keymap-editor commits straight to `main`, so `git pull` first.
- Commands for the user fit on one short line.
- Everything is configured on the keyboard, never in the OS or an app.
- No ApeKey or other secret in the repo.
- Times in Europe/Paris; GitHub Actions logs are UTC.

## First prompt

> Read `docs/HANDOFF.md`. First `git pull` and `git log --oneline -5`
> (any keymap-editor commits?). Then ask me about FEAT-9's review. Use
> the repo skills. Don't push anything without asking me first.
