# Handoff (2026-11-25)

Temporary note for resuming in a new session. Delete it once the items
below are closed. The authoritative state is the TODO files,
`docs/RESOLVED.md` and git history. Read `docs/DEVELOPER-GUIDE.md` first
(CLAUDE.md imports it); its "Handoffs" section defines this file's shape.

## Goal

The keyboard is the user's daily driver, on firmware `ef52ad4`
(verified 2026-11-25). Next: the same keymap on the Halcyon Corne
(FEAT-20) once the user's fork exists.

## Problems we're solving

- **FEAT-20** ([entry](TODO-features.md#feat-20-firmware-for-the-halcyon-corne-from-the-same-keymap)):
  plan approved 2026-11-18, nothing coded. The user's fork of
  `splitkb/zmk` doesn't exist yet (2026-11-21).
- **FEAT-21** ([entry](TODO-features.md#feat-21-study-fievels-keyboard-mouse-natively-in-zmk)):
  study added 2026-11-21: fievel's keyboard mouse is native ZMK (no
  module); hint mode can't be done in firmware. Waits on the user: is a
  mouse layer wanted?
- **BUG-8** ([entry](TODO-bugs.md#bug-8--is-a-dead-key-on-the-work-pc)) and
  **FEAT-4** ([entry](TODO-features.md#feat-4-workspace-switching-by-number-on-niri-and-cosmic)):
  wait on the user's chezmoi repo (home and work configs unified,
  being set up 2026-11-25) for `~/.config/niri/dms/binds.kdl`, plus the
  work PC's `localectl status`, which may not be in it.
- **FEAT-8** (rewrite or close when accents are next discussed),
  **FEAT-18**, **BUG-5**: no action pending.
- Closed 2026-11-25: FEAT-6 (lessons in `RESOLVED.md`) and FEAT-9.

## Main files

- `config/corne_hw.keymap`: still one line per layer; the user's next
  keymap-editor save turns it into the grid the guide describes. Don't
  edit the guide for this.
- `tools/key-check.html`: still the `ef52ad4` checklist (version 7 of
  https://claude.ai/artifact/Lykm8JfAtP6KVqetzvraFx); rewrite it for
  the next firmware.
- `docs/TODO-features.md` (FEAT-20, FEAT-21), `docs/TODO-bugs.md` (BUG-8).

## What failed (don't repeat)

- **No `node` on this machine:** the key-check page's JavaScript can't
  be syntax-checked before publishing. If the page shows nothing, look
  at the `CHECKS` block first.
- **fievel (FEAT-21) was studied from its README only**, not its
  source. Read the code before relying on a detail of its behavior.
- **`git rebase --autosquash` needs `-i`** on git 2.43, which isn't
  available here. To squash a fixup into the last commit: `git commit
  --amend`; deeper: detached checkout, `cherry-pick -n`, `--amend`,
  cherry-pick the rest, `git branch -f main`.
- **The scratchpad is wiped between sessions:** the key-check page lives
  in `tools/`; read the artifact by URL if the file is ever behind.
- **zsh treats `=====` as a command** in an echo. Use `---`.
- **A claude.ai session linked to the computer has no shell** (FEAT-20,
  2026-11-18): give each write-back a new staged file name, then check
  the size on disk.
- **splitkb's fork branch gets rebased** (FEAT-20): pin the user's copy
  of it, never a commit that only lives there.
- **chezmoi won't hold system settings** (BUG-8, 2026-11-25): the work
  PC's layout comes from `localectl`, not a dotfile; ask for its output
  even once the repo exists.

## Plan

1. FEAT-20, once the fork exists: plan steps 2–9 in order. Check first:
   `git ls-remote <fork URL> 'main+halcyon-fixes'` shows `80cf18d`.
2. FEAT-21: if the user wants a mouse layer, write its plan (keys, how
   to enter it, ground rules, `CONFIG_ZMK_POINTING=y` and the HID
   re-pair on each computer).
3. Once the chezmoi repo is set up: read the work configs from it,
   then BUG-8, then FEAT-4.

## Waiting on the user

- FEAT-21: is a mouse layer wanted?
- FEAT-20: the fork of `splitkb/zmk`, later the Halcyon Corne itself.
- The chezmoi repo (BUG-8, FEAT-4): where it is, once set up.

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
- Possible later move of this repo and the ZMK fork to the user's own
  Gitea instance (FEAT-20 lists what depends on GitHub). Not planned.

## First prompt

> Read `docs/HANDOFF.md`. First `git pull` and `git log --oneline -5`
> (any keymap-editor commits?). Then ask me about FEAT-20's fork,
> FEAT-21's mouse layer and the chezmoi repo. Use the repo skills.
> Don't push anything without asking me first.
