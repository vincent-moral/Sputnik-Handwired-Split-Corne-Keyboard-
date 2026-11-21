# Handoff (2026-11-18)

Temporary note for resuming in a new session. Delete it once the items
below are closed. The authoritative state is the TODO files,
`docs/RESOLVED.md` and git history. Read `docs/DEVELOPER-GUIDE.md` first
(CLAUDE.md imports it); its "Handoffs" section defines this file's shape.

## Goal

The keyboard is the user's daily driver and the firmware is stable
(BUG-9's balanced Low and Raise, flashed 2026-10-25). They're practising
on keybr and Monkeytype now. Next: the same keymap on the Halcyon Corne
that will replace the Sputnik (FEAT-20), ready before the keyboard
arrives. The rest is small items that wait on the user, and two studies
that only come back if the practice asks for them.

## Problems we're solving

- **FEAT-20** ([entry](TODO-features.md#feat-20-firmware-for-the-halcyon-corne-from-the-same-keymap)):
  plan approved 2026-11-18, nothing coded. Waits on the user's fork of
  `splitkb/zmk` (plan step 1); steps 2–9 need no keyboard, step 10
  does. Every question in it is answered.
- **FEAT-9** ([entry](TODO-features.md#feat-9-single-key-shortcuts-on-the-nav-layer)):
  reviewed 2026-11-21: unused, all seven keys removed (committed, not
  pushed). Waits on flashing and plan step 5.
- **BUG-8** ([entry](TODO-bugs.md#bug-8--is-a-dead-key-on-the-work-pc)) and
  **FEAT-4** ([entry](TODO-features.md#feat-4-workspace-switching-by-number-on-niri-and-cosmic)):
  blocked on the work PC's `localectl status` and
  `~/.config/niri/dms/binds.kdl`. The user forgot them twice (last asked
  2026-11-01).
- **FEAT-6** ([entry](TODO-features.md#feat-6-home-row-mods-that-only-trigger-with-the-other-hand)):
  fast typing gives `fi` instead of `I` (reported 2026-11-01). Candidate:
  `tapping-term-ms` 200 on `hsl`/`hsr` committed 2026-11-21 (tuned by
  feel; FEAT-19 dropped, its lessons in `RESOLVED.md`). Not pushed.
- **FEAT-8** (rewrite or close when accents are next discussed),
  **FEAT-18**, **BUG-5**: no action pending.

## Main files

- `docs/TODO-features.md`: FEAT-20, added 2026-11-18. Its plan lists
  every file it touches: `config/west.yml`, `build.yml`,
  `config/halcyon_corne.keymap` and `.conf` (new), `build.yaml`,
  `tools/zmk_build.py`, README, guide, `keymap-change` and
  `ship-firmware` skills.
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
  only the keyboard (ZMK's USB log) sees real timing (FEAT-19, in
  `RESOLVED.md`).
- **`git rebase --autosquash` needs `-i`** on git 2.43, which isn't
  available here. To squash a fixup: detached checkout of the target,
  `cherry-pick -n` the fix, `commit --amend`, cherry-pick the rest,
  `git branch -f main`.
- **The scratchpad is wiped between sessions:** the key-check page was
  lost twice. It now lives in `tools/`; read the artifact by URL
  (`path: index.html`) if the file is ever behind.
- **zsh treats `=====` as a command** (`=` expansion) in an echo. Use
  `---` as a separator.
- **FEAT-20 was written from a claude.ai session linked to the
  computer, without a shell on it** (2026-11-18): files can be read
  and written there, but git, pixi and podman can't run, so the user
  commits. Writing a file back twice under the same staged name saved
  the older copy, silently, twice: give each write-back a new staged
  file name, then check the size on disk.
- **splitkb's fork branch gets rebased** (FEAT-20): never pin a commit
  that only lives there. Pin the user's copy of it.

## Plan

1. FEAT-9: removal committed 2026-11-21 (unused). After pushing and
   flashing, its plan step 5, then `close-entry`.
2. FEAT-20, once the user has forked `splitkb/zmk`: plan steps 2–9 in
   order, each with the check its step names. Step 2 alone first, and
   compare the Sputnik's build warnings with the last build before
   adding the Halcyon. Check the fork first:
   `git ls-remote <fork URL> 'main+halcyon-fixes'` shows `80cf18d`.
3. When the user brings the work-PC dumps: BUG-8, then FEAT-4. Check:
   `localectl status` shows the layout and variant; `binds.kdl` lists
   the workspace bindings.
4. FEAT-6: after flashing, follow its plan step 9 (tune by feel).

## Waiting on the user

- FEAT-20: their fork of `splitkb/zmk` (its URL goes in `west.yml`),
  and the Halcyon Corne itself for plan step 10.
- Approval to push FEAT-9's removal and FEAT-6's 200 ms (firmware).
- FEAT-20's fork: doesn't exist yet (2026-11-21).
- Work-PC dumps for BUG-8 and FEAT-4.
- Approval to push the 2026-11-18 commits (skills, guide, handoff, the
  build's `.claude/**` ignore, and FEAT-20's docs commit).

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
> (any keymap-editor commits?). Then ask me about FEAT-9's review, and
> whether my fork of splitkb/zmk exists for FEAT-20. Use the repo
> skills. Don't push anything without asking me first.
