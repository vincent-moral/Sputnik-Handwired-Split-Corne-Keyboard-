# Features

Capabilities to add that don't exist yet. Reference an entry by its ID (`FEAT-N`).

## FEAT-4: Workspace switching by number on niri and COSMIC

**Priority:** Low until confirmed — the digits on the low layer are
keypad keys, so Super+1…9 bound to number-row keys probably won't match,
and Super on the left pinky plus the low layer on the left thumb breaks
the same-hand rule anyway.

**Complexity:** _Not yet discussed._

**Depends on** the niri config (see Prerequisites).

### Spec
- Unconfirmed (2026-10-16): whether Super+keypad digit triggers niri's
  and COSMIC's workspace shortcuts on an AZERTY layout. Super+U/I and
  Super+PgUp/PgDn are the alternatives.
- Work config read on 2026-10-20 (`config.kdl`): the bindings are in
  `include "dms/binds.kdl"`, not yet seen. Its own binds: Alt+Tab and
  Alt+Shift+Tab (fine with the right Alt, `l`), Alt+`` ` `` and
  Alt+Shift+`` ` `` — on AZERTY `` ` `` only exists as AltGr+7: whether niri
  matches Alt+AltGr+7 is untested, a binding to track.

### Implementation Plan
_Not yet discussed._

### Prerequisites
- `~/.config/niri/dms/binds.kdl` from the work PC: read it from the
  user's chezmoi repo once it's set up (2026-11-25), which unifies the
  home and work configs.
- Does the user switch workspaces by number?

## FEAT-8: One accent key (1dk) instead of the accent combos

**Priority:** Low — capital accented letters (É, À, Ç, È) can't be
typed at all today: Shift plus an accent combo types a digit. This gap
exists whether or not 1dk is adopted. The user's standard AZERTY
keyboards can't type them either, so it isn't a priority (2026-10-16).

**Complexity:** Medium — two extra layers (accents, shifted accents) and
the capitals trick; the key's position conflicts with `'`.

**From Arsenik** (guide §4): Ækeynox's AZERTY-1dk.

### Spec
- Tap the accent key, then a letter: à é è ù ç â ê î ô û œ µ €, plus the
  dead diaeresis on a double tap. Sequential, unlike the current combos,
  which press two keys with the same hand at once (to confirm with the
  user whether the combos were an intended exception).
- Capitals on Linux: Ækeynox wraps the key in Caps Lock (`&caps N2` = É),
  which works on the Linux AZERTY layout.
- Conflict: Ækeynox puts the accent key on the outer right home key,
  where `'` went on 2026-10-16, and types `'` as accent key + Space.

### Implementation Plan
_Not yet discussed._

### Prerequisites
- Study with the user: does it fit the README's ground rules?
- Were the accent combos an intended exception to the same-hand rule?
- Where would the accent key go, given that `'` must stay one keypress?

## FEAT-18: Low's digits without NumLock

**Priority:** Low — works on both PCs today (NumLock on at startup:
niri's `numlock` at work, 2026-10-20), but breaks plug and play on any
computer where NumLock is off: the digits become arrows and Home/End.

**Complexity:** Low to change, but a trade-off.

### Spec
- Low sends keypad digits (`KP_N1`…), which need NumLock.
- Alternative: number-row digits, which AZERTY types with Shift
  (`LS(N1)`…), whatever NumLock says. Cost: every digit sends Shift, so a
  digit inside a shortcut, or an app reading Shift, behaves differently;
  keypad digits were the original choice for that reason (R3).

### Implementation Plan
_Not yet discussed._


## FEAT-20: Firmware for the Halcyon Corne, from the same keymap

**Priority:** Medium — the Halcyon Corne replaces the Sputnik; both
must type the same thing until then, and the keymap must stay one
file (R1). Not urgent: the keyboard isn't bought yet (2026-11-18).

**Complexity:** Medium — no keymap change, but ZMK moves to splitkb's
fork for both keyboards, and the build tooling assumes one shield.

### Spec
- The repo builds firmware for both keyboards from
  `config/corne_hw.keymap`: the Sputnik (nice!nano) as today, and the
  Halcyon Corne rev2 (Halcyon Wireless controller, LiPo battery
  board). No dongle, although the bundle includes one: the left half
  is central and talks to the computers over Bluetooth profiles, as on
  the Sputnik.
- Decided (user, 2026-11-18): Halcyon Corne rev2, no Halcyon module
  planned, Bluetooth name "Halcyon Vincent" (15 characters; the
  Sputnik stays "Clavier Vincent"). The user forks splitkb's ZMK to
  their GitHub account. Underglow off: nothing in the keymap uses
  it. Everything up to flashing is prepared and built before the
  keyboard arrives.
- splitkb's support (read 2026-11-18):
  - Boards and shields are in `splitkb/zmk-halcyon-module` (`main` at
    `0b95571`, 2026-11-05): board `halcyon_wireless//zmk`, shields
    `halcyon_corne_left` / `halcyon_corne_right`, battery shield
    `mod_battery_lipo`. Its template `splitkb/zmk-halcyon-config`
    floats both the module and ZMK (R2 forbids that here).
  - The module needs splitkb's ZMK fork, branch
    `main+halcyon-fixes` (`80cf18d`, 2026-11-04): ZMK `4dd95d7`, the
    commit pinned here (`BUG-1`), plus 11 commits of power, sleep and
    BLE options. The wireless board's defconfig sets two of them
    (`ZMK_EXT_POWER_START`, `ZMK_SLEEP_POWER_OFF_ON_SUSPEND_FAILURE`),
    which upstream ZMK doesn't define. A `west.yml` holds one ZMK, so
    **the Sputnik moves to the fork too.**
  - splitkb rebases that branch: nine of the 11 commits were
    re-committed together on 2026-10-12, and the module's commit
    `d5ed4c1` links to a fork commit (`b315fde`) that is no longer on
    the branch. A pinned commit can vanish, hence the user's copy.
    The module's own history is linear (author and commit dates
    match): it is pinned straight from splitkb.
  - What stays the same: the keymap, the drawing, the audit, the
    cheatsheet, the key-check page, the skills and the workflows all
    live in this repo and never read ZMK's source. `build.yml` keeps
    ZMK's own build workflow at `4dd95d7`: the fork doesn't change it.
  - Effect on the Sputnik: every new option defaults to today's
    behavior except one ungated change in `pm.c`: a device that fails
    to suspend is now skipped instead of cancelling sleep. The
    module's code is gated by devicetree compatibles that only splitkb
    boards declare, so it compiles nothing into the Sputnik. Its
    `.uf2` won't be byte-identical (`FEAT-13`'s check); the build log
    and a day of use are the check.
  - Upgrading ZMK later means waiting for splitkb to rebase their
    branch, syncing the user's fork, then moving `west.yml` and
    `build.yml` together to the new base, as `BUG-1` requires.
- The keymap fits as is: the module's 42-key physical layout
  `splitkb_halcyon_corne` (`default_transform`) has the same key
  order as the Sputnik (three rows of 12, then the six thumbs 36–41),
  so the hold-trigger positions and the BT layer keep their meaning.
  The shield's default layout is `splitkb_halcyon_corne_hlc`: 52 keys,
  10 of them on Halcyon modules. With no module it goes back to 42.
- How ZMK picks files (`post_boards_shields.cmake` at `4dd95d7`): the
  keymap is `config/<shield name>.keymap`, and every
  `config/<shield>.conf` that exists is merged (`halcyon_corne.conf`
  for both halves, `halcyon_corne_right.conf` for the right one).
  `.conf` files can't include each other, so the shared settings are
  repeated, each file pointing to the other.
- **Maybe later (user, 2026-11-18): this repo and the ZMK fork may
  move to the user's own Gitea instance.** Not part of this entry. Unchecked,
  what depends on GitHub today: the keymap-editor
  (it commits to GitHub), the build and draw workflows (ZMK's reusable
  workflow, `GITHUB_TOKEN`, artifacts), and `gh` in the skills. The
  ZMK fork's URL in `west.yml` would change with it.
- Unchecked:
  - Whether keymap-editor is confused by a second `.keymap` file in
    `config/` (`FEAT-11`'s kind of test).
  - Whether the right half warns about USB like the Sputnik did
    (`BUG-6`): the board's defconfig sets `ZMK_USB=y` too.

### Implementation Plan
Approved 2026-11-18; the user codes it later. Each step is one commit
unless it says otherwise; `git pull` first (keymap-editor commits).

1. **User:** fork `splitkb/zmk` to their GitHub account, branch
   `main+halcyon-fixes` included. Check: commit `80cf18d` shows on
   the fork's branch.
2. **ZMK from the fork** (`chore(FEAT-20)`). `config/west.yml`:
   - remote for the user's account; project `zmk` from it at
     `80cf18d57c52a8ed4badc7f330cec7eada6521d8`, `import:
     app/west.yml`;
   - remote `splitkb`, project `zmk-halcyon-module` at
     `0b95571b332862a6fda8d62a0f0a4c6ccd7895dc`;
   - comments: why the fork (this entry), and that its base is the
     `4dd95d7` of `build.yml`.
   `build.yml`: same pin, comment now says "the base of the fork in
   `config/west.yml`". Check: `pixi run build` builds the Sputnik's
   three targets; read every warning against the last build.
3. **The Halcyon targets** (`feat(FEAT-20)`):
   - `config/halcyon_corne.keymap`: a comment saying why it exists,
     `#include "corne_hw.keymap"`, then `/ { chosen {
     zmk,physical-layout = &splitkb_halcyon_corne; }; };` (42 keys,
     no module).
   - `config/halcyon_corne.conf`: `CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=600000`,
     `CONFIG_ZMK_STUDIO=y`, `CONFIG_ZMK_STUDIO_LOCKING=n`,
     `CONFIG_ZMK_KEYBOARD_NAME="Halcyon Vincent"`, and
     `CONFIG_ZMK_RGB_UNDERGLOW=n`: the module's board file for this
     shield turns underglow on, and the keymap has no key for it.
     `config/corne_hw.conf` gets a matching "keep in
     step with" comment. Sleep itself is already on in the board's
     defconfig.
   - `build.yaml`, on `halcyon_wireless//zmk`: `halcyon_corne_left
     mod_battery_lipo` with the `studio-rpc-usb-uart` snippet;
     `halcyon_corne_right mod_battery_lipo`; `settings_reset`. Each
     gets an `artifact-name` (`halcyon_corne_left`,
     `halcyon_corne_right`, `halcyon_settings_reset`) so the Actions
     artifacts say which keyboard they are for. No
     `ZMK_SPLIT_ROLE_CENTRAL=n`: that is for dongle builds.
4. **Local build tool** (`fix(FEAT-20)`, same commit as step 3 if it
   is needed to build it): `tools/zmk_build.py` passes the shield
   unquoted to its `build` function and names logs after it; quote
   the shield and name targets by `artifact-name` when there is one.
   Check: `pixi run build` builds all six targets.
5. **Read the build** for the Halcyon: the right half's USB warning
   (if present, `config/halcyon_corne_right.conf` with
   `CONFIG_ZMK_USB=n`, as in `BUG-6`), any sensor warning, and that
   underglow is off in both halves' `.config`.
6. **keymap-editor test**, as for [`FEAT-6`](RESOLVED.md#feat-6-home-row-mods-that-only-trigger-with-the-other-hand): on a throwaway
   branch, open and save one key. Check: it still edits
   `config/corne_hw.keymap`, and `config/halcyon_corne.keymap` is
   untouched.
7. **Docs** (same commit as step 3): README "Building and flashing"
   for both keyboards: which artifacts go where; on the Halcyon,
   double-tap reset, copy to the `HALCYON` drive, then press reset
   once more after flashing (splitkb's docs: a bootloader bug that
   drains the battery otherwise); first flash with `settings_reset`
   on both halves. The guide's keymap-editor note and the
   `keymap-change` and `ship-firmware` skills: two keyboards, one
   keymap.
8. **Ship** with `ship-firmware`: all six jobs green.
9. **Sputnik check**, flashed from that build: a day of use, sleep
   and wake, Bluetooth profiles. Then `key-check` can close the
   Sputnik side.
10. **When the Halcyon arrives:** `settings_reset` then the firmware
    on both halves, pair as "Halcyon Vincent", and run the key check
    over every key (a full pass, since everything is new to this
    hardware). Then `close-entry`.

### Prerequisites
- None left: the user answered every question on 2026-11-18. The
  keyboard itself is only needed for step 10.

## FEAT-21: Study: fievel's keyboard mouse, natively in ZMK?

**Priority:** Low — a study; nothing is broken.

**Complexity:** Low for the mouse layer (native ZMK, no module); hint
mode can't be done in firmware at all.

### Spec
Study only (2026-11-21): **the user has taken no decision.** The
question: can ZMK do what
[fievel](https://github.com/MontyTheSoftwareEngineer/fievel) does
natively, or does it need a ZMK module?

What fievel is (README read 2026-11-21, source not read): **a Rust
program on the computer**, not firmware. It reads the keyboard through
the OS (evdev and uinput on Linux) and drives the mouse from the
keyboard. So adopting fievel itself would break the plug-and-play rule
(everything on the keyboard): it needs an install and permissions on
every computer, the work PC included.

Its features, against ZMK at our pin (`4dd95d7`, checked in its source
and docs 2026-11-21):

| fievel | ZMK | How |
|---|---|---|
| Mouse mode, held or toggled (F3, chord D+F) | Native | a layer: `&mo`, `&tog`, or a combo |
| Move with H/J/K/L, easing | Native | `&mmv` (`zmk,behavior-input-two-axis`: `time-to-max-speed-ms`, `acceleration-exponent`); no easing on release (stops at once) |
| Fast / slow keys | Native | a layer override on `mmv_input_listener` with `&zip_xy_scaler`, or several `&mmv` instances with their own speeds |
| Left/right/middle click, drag | Native | `&mkp LCLK` etc., held for a drag |
| Scroll, Home/End by chording scroll keys | Native | `&msc`; combos for Home/End |
| Chorded home-row mods (A+S = Super, 25 ms) | Native | combos with a short `timeout-ms`; but it competes with our hold-tap home-row mods (README ground rules) |
| Caps Lock: tap Ctrl, hold nav | Native | a hold-tap |
| Hint mode (labels on clickable things), locator, keycast, on-screen indicator | **Impossible in firmware** | needs to see or draw on the screen; a ZMK module can't either |
| Odometer | Not native | a module could count `&mmv` output; little use |

Notes:
- Mouse keys are HID mouse reports: AZERTY doesn't touch them (R3).
- `CONFIG_ZMK_POINTING=y` changes the HID descriptor: each paired
  computer must refresh it (ZMK docs: re-pair) or the mouse doesn't
  work over Bluetooth.
- Known for the browser: Vimium C (already used) gives hints there.
  Outside the browser, hints need a computer-side tool, which conflicts
  with the plug-and-play rule.
- `FEAT-20` moves ZMK to splitkb's fork: check pointing is there too
  before planning.

**Conclusion:** everything fievel does with the keyboard alone (mouse
mode, movement, speeds, clicks, scroll, chords) is native ZMK; no
module. Hint mode and the overlays are computer-side by nature.

### Implementation Plan
_Not yet discussed._

### Prerequisites
- Is a mouse layer wanted? If so: which keys, entered how (layer key,
  combo), and does it fit the README's ground rules?
