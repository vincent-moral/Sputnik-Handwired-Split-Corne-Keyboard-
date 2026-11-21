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
- `~/.config/niri/dms/binds.kdl` from the work PC (the user brings it on
  2026-10-22).
- Does the user switch workspaces by number?

## FEAT-6: Home-row mods that only trigger with the other hand

**Priority:** High — the home-row mods use ZMK's default `&mt`
(hold-preferred, 200 ms, checked in ZMK `4dd95d7` on 2026-10-16): any key
pressed while a home-row key is still down makes it a modifier, so a fast
roll like `f`→`r` types `R` and `d`→`e` sends Ctrl+E.

**Complexity:** Medium — one custom hold-tap behavior, but its timings
need tuning by daily use.

**From Arsenik** (guide §4): its FAQ recommends, for ZMK, the
`balanced` flavor plus positional hold-tap.

### Spec
- A custom hold-tap for the eight home-row mods:
  - `hold-trigger-key-positions`: the other hand's keys and the thumbs,
    so a same-hand key always resolves as a tap. This is the same-hand
    rule enforced by the firmware.
  - `balanced` or `tap-preferred` flavor instead of `hold-preferred`, so
    rolls across hands stay letters.
  - Candidates to evaluate: `require-prior-idle-ms` (letters while typing
    fast), `quick-tap-ms` (key repeat), `hold-trigger-on-release`.
  - Arsenik's own default is tap-preferred with a 300 ms term.
- Study (2026-10-16): fits the ground rules. It enforces the same-hand
  rule and moves no key. The thumbs count as triggers, which keeps the
  nav-layer exception (Shift on `f` + nav + arrow) working. A same-hand
  modifier is still possible on purpose, by holding past the tapping term.
- The user confirmed misfires (2026-10-16): Alt sometimes fires instead
  of the letter. Alt is on the ring fingers (`s`, `l`), which release
  late in rolls like `l`→`e`.
- Shift stays instant (user's choice, 2026-10-16): no
  `require-prior-idle-ms` on the Shift keys, so a capital right after a
  quick space still works.
- The user holds `j`/`k` to scroll in vim and Vimium. Both are home-row
  mods (Shift, Ctrl), so a long press is a modifier, today and after this
  change. `quick-tap-ms` makes tap-then-hold repeat; hjkl arrows on the
  nav layer are the other option (see Prerequisites).

### Implementation Plan
Approved 2026-10-16.
1. **Done (2026-10-16):** add four hold-tap behaviors to `config/corne_hw.keymap`, following
   ZMK's "timeless home-row mods" example: `balanced`,
   `tapping-term-ms` 280, `quick-tap-ms` 175, `hold-trigger-on-release`,
   `hold-trigger-key-positions` = the other hand's 18 keys plus all six
   thumbs (36–41).
   - `hml` / `hmr` (GUI, Alt, Ctrl): with `require-prior-idle-ms` 150.
   - `hsl` / `hsr` (Shift): without it.
2. **Done (2026-10-16):** use them for the eight home-row keys instead
   of `&mt`.
3. **Done (2026-10-16):** README: say the firmware enforces the same-hand rule, and credit
   Arsenik and ZMK's timeless home-row mods (guide §4).
4. **Done (2026-10-16):** the user opens and saves the keymap in
   keymap-editor: the behaviors survive. Opening: the editor shows the
   home-row keys as `&hml`/`&hmr`/`&hsl`/`&hsr` and the nav thumb as
   `&lthp` (its warning, no row/col in the layout file, fixed 2026-10-16). Saving: on a throwaway
   `editor-test` branch the user changed one key (position 31, `M` to
   `A`); the editor's commit `5a059ab` changed only that binding, and
   left behaviors, combos and comments byte-identical. Branch deleted.
5. **Done (2026-10-16):** pushed to `dev`; all five jobs green, the only
   annotation the known Ubuntu 26 runner notice (full logs need a `gh`
   login); `main` fast-forwarded to `7a40cc5`.
6. **Done (2026-10-16):** flashed (`8f5aa23`) and verified: fast rolls
   (`le`, `la`, `sd`, `de`, `fr`) give letters; `k`+`c` copies; a
   capital right after a space works; Shift + nav + arrow selects;
   tap-then-hold `j` repeats, but only when the second press is fast.
7. Tune the timings after a week of daily use. Candidate: the
   tap-then-hold window is short because ZMK counts `quick-tap-ms` (175)
   from the first tap's *press* (`behavior_hold_tap.c` at `4dd95d7`); if
   it stays awkward, raise it to about 250 on `hmr`/`hsr`.

   - Reported 2026-11-01: typing fast, a capital often comes out as two
     letters, e.g. `fi` for `I` (Shift on `f`). With `balanced` and
     `hold-trigger-on-release`, Shift needs `i` to be released while `f`
     is still down, or `f` held past 280 ms; letting go of `f` first
     makes it the tap. The fast roll `f`→`i` (afin, fin, profiter)
     looks the same by key order, so only how long `f` was held before
     `i` can tell them apart: a shorter `tapping-term-ms` on
     `hsl`/`hsr` is the candidate.
8. **Done (2026-11-21):** `tapping-term-ms` 280 → 200 on `hsl`/`hsr`
   only. The user misses many capitals and chose to tune by feel rather
   than measure ([`FEAT-19`](RESOLVED.md#feat-19-study-measuring-typing-per-key-and-the-firmwares-decisions)
   dropped). Balanced flavor checked in
   `behavior_hold_tap.c` at `4dd95d7`: releasing `f` first is a tap,
   unless the timer fired first (hold). The trade-off: a slow roll with
   `f` or `j` held over 200 ms now gives a capital.
9. Flash, then a few days of daily use: capitals reliable, and no
   stray capitals in rolls like `afin`, `fin`, `je`. Too many stray
   capitals → back up (e.g. 230); capitals still missed → down (e.g.
   170). Then close the entry, or keep it for the `quick-tap-ms`
   question in step 7.

### Prerequisites
- Plan approved 2026-10-16. Holding `j`/`k`: tap-then-hold for now;
  hjkl arrows on the nav layer are deferred until the user has more
  experience with arrows on this keyboard.

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

## FEAT-9: Single-key shortcuts on the nav layer

**Priority:** Low — undo, cut, copy, paste (and kitty's Ctrl+Shift+C /
Ctrl+Shift+V) as single keys need no chord at all.

**Complexity:** Low — a few bindings on the nav layer's free right-hand
slots.

**From Arsenik** (guide §4): its nav layer has them on ZXCV.

### Spec
- On AZERTY the keyboard sends QWERTY positions: undo is `LC(W)`, select
  all `LC(Q)` (Ækeynox's AZERTY aliases).
- The nav layer is held by the left thumb, so under the same-hand rule
  they go on the right hand.

- Study (2026-10-16): fits the ground rules (nav thumb on the left, the
  shortcuts on the right). The real gain is kitty's Ctrl+Shift+C/V,
  impossible today since Ctrl (`k`) and Shift (`j`) are both right-hand
  home-row mods; plain undo/copy/paste already work as `k` + a letter.
- Layout (proposed, the user liked it 2026-10-16): undo, cut, copy,
  paste, redo (Ctrl+Shift+Z) on the bottom row (`n , ; : !`); kitty copy
  and paste on the two free home-row slots (`m`, `'`).
- New habit for the user: the README says how and when to use it.

### Implementation Plan
Approved 2026-10-16.
1. **Done (2026-10-16):** bindings on the nav layer: `LC(W)`, `LC(X)`,
   `LC(C)`, `LC(V)`, `LC(LS(W))` at 30–34, `LC(LS(C))`, `LC(LS(V))` at
   22–23; README diagram plus a "how and when" note; README credits
   Arsenik (guide §4).
2. **Done (2026-10-16):** pushed to `dev`, all five jobs green (only the
   Ubuntu 26 runner notice), `main` fast-forwarded to `4109eae`.
3. **Done (2026-10-16):** flashed the left half and verified in COSMIC
   Text Editor (select on nav then copy, paste, undo, redo, cut) and in
   kitty (nav + `m` copies, nav + `'` pastes, nav + `;` stops `sleep`).
4. **Done (2026-11-21):** reviewed: the user doesn't use them and chose
   to remove all seven (the bottom row and kitty's two). Bindings,
   legends, README note and Arsenik credit removed; kitty's
   Ctrl+Shift+C/V stay reachable through the Mods layer (one-shot Ctrl,
   then Shift).
5. Push (`ship-firmware`), flash, and check on the keyboard that nav +
   `n , ; : ! m '` now type nothing new (the base letters pass through,
   as before `FEAT-9`). Then `close-entry`.

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
6. **keymap-editor test**, as in `FEAT-6` step 4: on a throwaway
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
