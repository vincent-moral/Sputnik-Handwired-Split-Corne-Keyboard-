# Developer guide

How work is done in this repo. **Read this before changing anything**,
whether you're a person or an AI. Adapted from the workflow used in
`homelab-iac`, keeping only what applies to a keymap repo.

The layout's ground rules (AZERTY OS, home-row mods, same-hand rule and
its exceptions) live in [`README.md`](../README.md#layout-ground-rules):
check every change against them.

## 1. The workflow

1. **Backlog first.** Anything non-trivial gets an entry (`BUG-N` or
   `FEAT-N`, see §3) with a Spec and an Implementation Plan before the
   keymap is changed.
2. **Change locally, as small atomic commits**, one logical change each.
   A keymap change updates the README's layer diagrams **in the same
   commit** (R1).
3. **Push only with explicit approval.** A push to `main` makes GitHub
   Actions build new firmware. Nothing changes on the keyboard until the
   user flashes it, but a broken build blocks every later change.
4. **Check the build** after a push (Actions tab, or
   `gh run list --limit 1`). "The build is green" only proves it
   compiles.
5. **Verify on the keyboard** after flashing: type every changed key on
   the AZERTY OS and check the character it produces. Close the entry
   only after that.
6. **Close the loop in the same session:** mark plan steps **Done**,
   then delete the entry, or move it to `docs/RESOLVED.md` if the
   resolution taught something non-obvious.

### Who may change what

- **The keymap is only changed in this repo** and flashed from the
  binaries GitHub Actions builds. No ZMK Studio edits.
- **The user also edits it with Nick Coutsos's
  [keymap-editor](https://nickcoutsos.github.io/keymap-editor/)**, which
  commits straight to `main` on GitHub and draws its layout from
  `config/corne_hw.json`. So:
  - `git pull` before changing anything: the remote may have editor
    commits.
  - The editor rewrites `config/corne_hw.keymap` in its own format (each
    layer's bindings on one line). Keep that format so its diffs stay
    readable; comments outside the combos may not survive an editor save.
  - Editor commits don't follow the commit format below or update the
    README; check the README diagrams after one (R1).
  - The editor shows QWERTY keycodes, not what AZERTY types (`FEAT-5`).
- **AI assistants** prepare local commits and stop there. They don't
  push without explicit approval for that push.
- **A command for the user fits on one short line** (they copy it from a
  neovim plugin, which breaks long lines). Anything longer becomes a
  script first.

### Commits

- Subject: `type(ID): what changed`, with `type` one of `feat`, `fix`,
  `docs`, `chore`, `ci`, and the backlog ID when there is one.
  Example: `feat(FEAT-2): plain ^ on the nav layer`.
- Body: **why**, and an **`Effect on push:`** line, for example
  "CI builds new firmware; nothing changes until flashed" or
  "docs only".
- A mistake caught before pushing is squashed into the commit it fixes,
  not added as a follow-up. Pushed history is never rewritten.

## 2. Rules

### R1. One source of truth per fact
A fact written in two places drifts. The keymap owns the bindings; the
README's diagrams describe what they type, and must change with it
(until `FEAT-5` generates them). Link instead of copying anywhere else.

### R2. Pin every version
A floating version changes the firmware without a commit: ZMK on
`main` can change what a binding does between two builds of the same
keymap ([`BUG-1`](RESOLVED.md#bug-1-zmk-and-its-build-workflow-floated-on-main)). Tools come from pixi when it has them.

### R3. Check how the tool behaves; don't assume it
Before relying on how ZMK, the OS layout or an app handles a key,
confirm it in the docs or source, or test it on the keyboard. Examples
of traps here: QWERTY keycodes typed through an AZERTY layout, dead
keys (`^` from the combo), keypad digits versus number-row digits.

### R4. Comments and docs explain why, and stay true
Comments say why a key is where it is. A behavior change updates the
comments and docs it contradicts in the same commit. State-dependent
claims carry a date.

## 3. The backlog

- `docs/TODO-bugs.md` (`BUG-N`), `docs/TODO-features.md` (`FEAT-N`).
  IDs are never reused.
- Entry template: `**Priority:**` and `**Complexity:**` (level first, then
  the reason), optional `**Quick win:** yes ...`, then `### Spec`,
  `### Implementation Plan` (numbered steps; finished ones start with
  `**Done (date):**`), optional `### Prerequisites` for open questions
  addressed to the user. Unknown sections stay `_Not yet discussed._`
  rather than invented.
- `**Depends on X**` lead-ins link entries.
- When closing an entry, `git grep -nw '<ID>'` and fix every reference.

## 4. Borrowed ideas

Entries marked **From Arsenik** come from
[Arsenik](https://github.com/OneDeadKey/arsenik) and its split variant
[Selenium](https://onedeadkey.github.io/selenium/), as implemented for ZMK
by [Ækeynox](https://github.com/OneDeadKey/zmk-config-aekeynox).

- Each one is studied with the user before any plan: it's adopted only
  if it fits the ground rules in the README.
- **Once one is adopted, the README credits Arsenik** (same commit as the
  keymap change), saying what was taken.

## 5. For AI assistants

- Read this guide, then the backlog, before assuming something is new.
- Follow §1's authorization rules exactly: prepare, explain, ask.
- Keep the user's decisions: don't move a key they placed, or change an
  accepted exception, without saying so explicitly.
