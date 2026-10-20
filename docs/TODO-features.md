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
4. Around 2026-11-06: is it used? If not, remove it rather than keep
   unused keys.

## FEAT-13: Move the shield out of the deprecated `config/boards` folder

**Priority:** Low — a deprecation warning only (2026-10-18); it becomes
urgent if a ZMK upgrade drops `config/boards`.

**Complexity:** Medium — files move into a Zephyr module, and the build,
the keymap-editor and the keymap drawing all read paths in `config/`.

### Spec
- Every build warns: "The `config/boards` folder is deprecated. Please
  use a module instead." (ZMK `4dd95d7`, CI and local builds alike).
- ZMK wants the shield (`corne_hw_left`, `corne_hw_right`) shipped as a
  module, with the keymap and `.conf` staying in `config/`.

### Implementation Plan
_Not yet discussed._

## FEAT-16: A sticky Accents key instead of the combos

**Priority:** High — the 70 ms combos (`BUG-7`) fire on fast rolls, which
bothered the user most on 2026-10-20; they chose this instead.

**Complexity:** Medium — a sticky layer, two one-parameter macros, and
the combos removed.

**From Lafayette** ([qwerty-lafayette.org](https://qwerty-lafayette.org/)),
whose single dead key ★ types every French accent: the key pressed after
★ chooses the accent. Lafayette itself is an OS layout (installed per
computer, QWERTY letters), so only the idea fits the ground rules.

### Spec
- Tap ★, then a key: a one-shot Accents layer sending AZERTY keycodes,
  so nothing changes on the computer. No simultaneous press, so no combo
  timing (`BUG-7`), and no same-hand chord at all.
- Proposed mapping (2026-10-19), most frequent accent on the easiest key:
  ★ `e` é, ★ `z` (left of `e`) è, ★ `d` (under `e`) ê; ★ `a` à, ★ `q` â;
  ★ `u` ù, ★ `j` û; ★ `i` î, ★ `k` ï; ★ `o` ô, ★ `l` ö; ★ `c` ç.
  Circumflexes send AZERTY's `^` dead key then the vowel, as the `i`+`o`
  combo does by hand.
- Capitals (É, À…) and œ: AZERTY has no key for them; left out for now
  (user, 2026-10-20).
- ë on ★ `s` and ü on ★ `h` (user, 2026-10-20), with the `¨` dead key
  (Shift + the `^` dead key on AZERTY).
- ★ is **Low's tap** (user, 2026-10-20; to move if it feels wrong): the
  same tap/hold split as Raise, so every layer thumb holds its layer and
  taps one key from it. Low comes as soon as another key is pressed.
- **All six combos go** (user, 2026-10-20), `i`+`o` (`^` dead key)
  included: ★ covers the circumflex vowels and Raise has the plain `^`.

### Implementation Plan
Approved 2026-10-20.
1. **Done (2026-10-20):** keymap: `&ltsl 1 6` on Low; a seventh layer, Accents, with the
   mapping above (`&kp` for é è à ù ç, macros `circ`/`trema` for the
   dead-key vowels, checked in `zmk,behavior-macro-one-param.yaml` at
   `4dd95d7`); the combos removed. Drawing, cheatsheet pages, README
   (ground rule, layer note, "how and when"), the key-check page.
2. **Done (2026-10-20):** local build OK; pushed to `dev`, all five jobs
   green (only the Ubuntu 26 notice), warnings and sizes identical to the
   local build, no redraw commit; `main` fast-forwarded to `a657bc9`.
3. The user flashes and checks every accent and that fast rolls stay
   letters; then close `BUG-7` and this entry.

## FEAT-17: Keep the local build and the drawing audit in the repo

**Priority:** Medium — both scripts live in Claude's scratchpad, which was
wiped three times between 2026-10-18 and 2026-10-20; each time they had to
be rewritten before a push.

**Complexity:** Low — two scripts and two pixi tasks; CI for the audit.

### Spec
- **Local build:** builds both halves in ZMK's CI image
  (`zmkfirmware/zmk-build-arm`, pinned by digest) with podman, mirroring
  `build-user-config.yml` at `4dd95d7`, and prints warnings and sizes to
  compare with CI. A pre-push check, never firmware to flash (the user
  flashes only what GitHub builds). podman is a system tool, not from pixi.
- **Drawing audit:** for every binding, works out what xkb `fr` (basic)
  types, accent macros included, and compares it with the drawing's
  legend; 76 legends, 0 mismatches on 2026-10-20. Worth running in the
  draw workflow, so a wrong legend fails CI instead of reaching the README.
- The audit reads `/usr/share/X11/xkb/symbols`: in CI that needs the
  `xkb-data` package, or a copy of the `fr` file pinned in the repo (R2).

### Implementation Plan
_Not yet discussed._

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

