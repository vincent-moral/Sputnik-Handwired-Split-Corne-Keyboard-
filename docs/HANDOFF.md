# Handoff (2026-11-21)

Temporary note for resuming in a new session. Delete it once the items
below are closed. The authoritative state is the TODO files,
`docs/RESOLVED.md` and git history. Read `docs/DEVELOPER-GUIDE.md` first
(CLAUDE.md imports it); its "Handoffs" section defines this file's shape.

## Goal

The keyboard is the user's daily driver. Today's firmware (`ef52ad4`)
fixes missed capitals (FEAT-6) and removes unused nav keys (FEAT-9); it
is built and on `main`, not yet flashed. Next: verify it, then the same
keymap on the Halcyon Corne (FEAT-20) once the user's fork exists.

## Problems we're solving

- **FEAT-6** ([entry](TODO-features.md#feat-6-home-row-mods-that-only-trigger-with-the-other-hand)):
  `tapping-term-ms` 280 → 200 on `hsl`/`hsr` (2026-11-21), tuned by
  feel. Waits on flashing, the key check and a few days of daily use
  (plan step 9).
- **FEAT-9** ([entry](TODO-features.md#feat-9-single-key-shortcuts-on-the-nav-layer)):
  unused, all seven keys removed (2026-11-21). Waits on flashing and
  plan step 5, then `close-entry`.
- **FEAT-20** ([entry](TODO-features.md#feat-20-firmware-for-the-halcyon-corne-from-the-same-keymap)):
  plan approved 2026-11-18, nothing coded. The user's fork of
  `splitkb/zmk` doesn't exist yet (2026-11-21).
- **FEAT-21** ([entry](TODO-features.md#feat-21-study-fievels-keyboard-mouse-natively-in-zmk)):
  study added 2026-11-21: fievel's keyboard mouse is native ZMK (no
  module); hint mode can't be done in firmware. Waits on the user: is a
  mouse layer wanted?
- **BUG-8** ([entry](TODO-bugs.md#bug-8--is-a-dead-key-on-the-work-pc)) and
  **FEAT-4** ([entry](TODO-features.md#feat-4-workspace-switching-by-number-on-niri-and-cosmic)):
  blocked on the work PC's `localectl status` and
  `~/.config/niri/dms/binds.kdl` (last asked 2026-11-01).
- **FEAT-8** (rewrite or close when accents are next discussed),
  **FEAT-18**, **BUG-5**: no action pending.
- Closed today: FEAT-19, dropped (lessons in `RESOLVED.md`).

## Main files

- `config/corne_hw.keymap`: `hsl`/`hsr` (FEAT-6), the nav layer (FEAT-9).
  Still one line per layer: the user's next keymap-editor save turns it
  into the grid the guide describes. Don't edit the guide for this.
- `README.md`, `keymap_drawer.config.yaml`, `keymap-drawer/`: FEAT-9's
  legends and nav note removed, FEAT-6's 200 ms in the ground rules.
- `tools/key-check.html`: rewritten for `ef52ad4` (FEAT-6 and FEAT-9
  checks, `RES` `res-1121`), published as version 7 of
  https://claude.ai/artifact/Lykm8JfAtP6KVqetzvraFx.
- `docs/TODO-features.md` (FEAT-6, FEAT-9, FEAT-21), `docs/RESOLVED.md`
  (FEAT-19).

## What failed (don't repeat)

- **Explained build warnings before checking them** (2026-11-21): said
  three `keymap.c` warnings were "apparently from `settings_reset`".
  `tools/zmk_build.py` prints warnings after all the sizes, not per
  target. Building the previous commit showed them identical, so they
  aren't new. To build an older keymap: `git checkout <commit> --
  config/`, `pixi run build`, `git checkout HEAD -- config/` (the build
  copies the working tree's `config/`).
- **No `node` on this machine:** the key-check page's JavaScript wasn't
  syntax-checked before publishing. If the page shows nothing, look at
  the `CHECKS` block first.
- **fievel (FEAT-21) was studied from its README only**, not its
  source. Read the code before relying on a detail of its behavior.
- **Pushed to `dev` without asking** (BUG-6). Every push needs its own
  approval, `dev` included.
- **Claimed checks the user hadn't reported** (BUG-9). Write only what
  the pasted report says; the rest is "not reported".
- **A Kconfig claim without reading the build** (BUG-6). Read the build
  log and the board files before explaining a Kconfig value (R3).
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

## Plan

1. When the user pastes the key-check report: record it in FEAT-6 and
   FEAT-9 as reported (unreported checks say so). FEAT-9 all passed →
   `close-entry`. FEAT-6 stays open for daily use (step 9).
2. FEAT-6 after a few days: stray capitals in rolls → 230 ms; capitals
   still missed → 170 ms (`keymap-change`, then `ship-firmware`).
3. FEAT-20, once the fork exists: plan steps 2–9 in order. Check first:
   `git ls-remote <fork URL> 'main+halcyon-fixes'` shows `80cf18d`.
4. FEAT-21: if the user wants a mouse layer, write its plan (keys, how
   to enter it, ground rules, `CONFIG_ZMK_POINTING=y` and the HID
   re-pair on each computer).
5. Work-PC dumps: BUG-8, then FEAT-4.

## Waiting on the user

- Flash `ef52ad4` (`gh run download 44941738003`, artifact `firmware`:
  left `corne_hw_left-studio-rpc-usb-uart`, right `corne_hw_right`),
  then run the key check and paste its report.
- Approval to push `e5c7fde` (key-check page, docs only) and this
  handoff commit.
- FEAT-21: is a mouse layer wanted?
- FEAT-20: the fork of `splitkb/zmk`, later the Halcyon Corne itself.
- Work-PC dumps for BUG-8 and FEAT-4.

## In progress

- Firmware `ef52ad4` (FEAT-6, FEAT-9): `dev` build green 2026-11-21
  20:35 (19:35 UTC), all five jobs, no annotations; `main`
  fast-forwarded, `dev` deleted, `main`'s own build green. Not flashed.

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
> (any keymap-editor commits?). Then ask me whether I flashed `ef52ad4`
> and for the key-check report (FEAT-6, FEAT-9). Use the repo skills.
> Don't push anything without asking me first.
