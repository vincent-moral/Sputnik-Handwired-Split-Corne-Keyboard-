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

### Implementation Plan
_Not yet discussed._

### Prerequisites
- The user's niri `config.kdl` and any custom Dank Material Shell
  keybindings from the work PC.
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

## FEAT-10: Study Arsenik's symbols layer for the raise layer

**Priority:** Low — the raise layer has no muscle memory yet (the user
knows the base and number layers well, as of 2026-10-16), so it can still
be redesigned freely.

**Complexity:** Medium — the layer uses both hands, which needs a sticky
key under the same-hand rule: the AltGr thumb's tap, since Raise's tap
is `FEAT-7`'s Mods layer.

**From Arsenik** (guide §4): its symbols layer, taken from
Ergo-L, with AZERTY keycodes in Ækeynox's `aliases/azerty.h`.

### Spec
- All 30 programming symbols on one layer, none needing Shift, the most
  frequent (`{ ( ) } =`) on the left home row, common sequences without
  same-finger bigrams, designed with vim in mind.
- Would replace today's raise layer and the symbols around the numpad on
  the low layer.
- Source: Ækeynox `include/aekeynox/selenium.keymap` (`symbols_layer`) at
  `3cadeed` (2026-10-08). Their default opens it with the right outer
  thumb (here AltGr), as a sticky layer in one variant; on the layer the
  left thumbs are a sticky Num key, Space and Enter.
- The layer, as typed on AZERTY (3×10, outer columns not part of it):

  ```
  ^ < > $ %   @ & * ' `
  { ( ) } =   \ + - / "
  ~ [ ] _ #   | ! ; : ?
  ```

  Keycodes from Ækeynox's `aliases/azerty.h`, checked against this
  Linux's xkb `fr` (2026-10-18): `^` `` ` `` `~` are plain with AltGr
  (`RA(N9)`, `RA(N7)`, `RA(N2)`, as used today); `*` is the unshifted
  key next to Enter (`BSLH`, new here), not the keypad `*`, so vim's
  `*` search works.
- Comparison with today (2026-10-18). Both type all 30 symbols:
  - Today they're spread over four places: Raise (17, left hand), Low
    around the numpad (`{ } & $ % ~ *`, right hand), the AZERTY base
    (`' , ; : !`, plus Shift for `. / ?`), and Nav for the plain `^`
    (the `i`+`o` combo stays the dead key). Every layer keeps its keys
    on the hand opposite its thumb.
  - Arsenik puts them on one layer, none needing Shift, brackets grouped
    on the left (`{ ( ) }` home row, `[ ]` below), designed for code and
    vim.
  - Gains: one place for every symbol, `/` and `?` without Shift, Low
    left with numbers and Bluetooth only.
  - Costs: half the layer is on the same hand as the thumb that holds
    it, so those keys need a sticky tap, and Raise's tap is the Mods
    layer (`FEAT-7`). The Raise and Low symbols move (little muscle
    memory yet). The base punctuation is unchanged either way.

- The sticky key (user's choice, 2026-10-18): the AltGr thumb
  (position 41), Arsenik's own place. Tap: sticky Symbols for one key;
  hold: AltGr as today, as soon as another key is pressed (the nav
  thumb's split, `BUG-3`). The user doesn't type with AltGr by hand.
- Raise's hold becomes the Arsenik layer: its left half follows the
  same-hand rule held; the sticky tap reaches both halves. Raise's tap
  stays the Mods layer (`FEAT-7`).

### Implementation Plan
Approved 2026-10-18.
1. **Done (2026-10-18):** `config/corne_hw.keymap`:
   - the raise layer becomes the 3×10 above (columns 1–10), keeping its
     thumbs; outer columns transparent except Ctrl (12) and ⌫ (11),
     which the user placed there;
   - a hold-tap `mtsl` (hold-preferred, 150 ms,
     `bindings = <&kp>, <&sl>`) on position 41 of every layer as
     `&mtsl RALT 2`.
2. **Done (2026-10-18):** Low keeps its symbols (`{ } & $ % ~`) while the new layer is learned.
3. **Done (2026-10-18):** drawing: legends for `BSLH` (`*`), `/`, `?`
   and the AltGr thumb; `pixi run draw`.
4. **Done (2026-10-18):** README: the raise notes, a "how and when" note (hold Raise for the
   left half, tap AltGr for any one symbol), and the Arsenik credit.
5. **Done (2026-10-18):** local build in CI's image OK; pushed to
   `dev`, all five jobs green (only the Ubuntu 26 notice), warnings and
   sizes identical to the local build, no redraw commit; `main`
   fast-forwarded to `0f891c9`.
6. **Done (2026-10-18):** flashed and verified with the key-check page:
   all 30 symbols, both ways; AltGr+e gives €; the AltGr tap lapses
   after 1 s; Raise's tap still opens Mods.
7. **Done (2026-10-19):** brought forward (user, 2026-10-19: they reach for the duplicates and
   want no habit on them): remove Low's `{ } & $ % ~` and the keypad
   `*`, as `&none` so nothing is typed. Popular numpad layers rarely
   hold `*` (Miryoku: `= - . /`; Arsenik: `/ - , .`), and Raise has
   `+ - * /`. Pushed with `FEAT-14` (2026-10-19).


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

## FEAT-14: Each sticky tap on the thumb that matches it

**Priority:** High — after a day of use (2026-10-18) the user mixes up
the two sticky taps, and is sometimes too slow for them.

**Complexity:** Low — two thumb bindings and two custom sticky
behaviors.

### Spec
- Today Raise's tap is the Mods layer (`FEAT-7`) and AltGr's tap is
  sticky Symbols (`FEAT-10`): neighbouring keys, nothing tying each tap
  to its key.
- Swap them (user's choice, 2026-10-19), so each thumb does one kind of
  thing: **Raise** holds symbols and its tap gives one sticky symbol;
  **AltGr** holds AltGr and its tap gives one sticky modifier.
- Sticky keys wait 1.5 s instead of ZMK's 1 s (user's choice,
  2026-10-19), for both the layers and the modifiers. Custom copies of
  `&sl` and `&sk` with `release-after-ms` 1500, keeping their defaults
  (`quick-release` on the layer, `ignore-modifiers` on the modifiers):
  a behavior override outside the root node might not survive the
  keymap-editor, the `behaviors` node does (tested 2026-10-16).

### Implementation Plan
Approved 2026-10-19.
1. **Done (2026-10-19):** keymap: `&ltsl 2 2` on Raise, `&mtsl RALT 4` on AltGr; `ssl`/`ssk`
   behaviors at 1500 ms used by both and by the Mods layer; drawing,
   README, the key-check page.
2. **Done (2026-10-19):** local build OK; pushed to `dev` with the other
   day-one changes, all five jobs green (only the Ubuntu 26 notice),
   warnings and sizes identical to the local build, no redraw commit;
   `main` fast-forwarded to `c1c6248`.
3. The user flashes on 2026-10-20 and checks with the key-check page.

## FEAT-15: The nav thumb without Super

**Priority:** Medium — the user wants no muscle memory on a redundant
Super (2026-10-19).

**Complexity:** Low — one binding.

### Spec
- The left outer thumb is Super on a tap and Nav when held (`BUG-3`).
  Super is also on the home row (`q`, `m`), so the thumb's tap is a
  second way to do the same thing.
- The user taps Super alone for COSMIC's launcher; niri uses
  Super+Space, which the user wants everywhere in the long run (DMS on
  the personal PC one day).
- The thumb becomes plain `&mo 3`: Nav comes at once, with no
  tap/hold decision. Super+Space: hold `m`, tap Space (other hand).
  Super alone on COSMIC: hold `m` past 280 ms and release it, which
  sends Super alone (the home-row mod's hold, no other key) — to verify.

### Implementation Plan
Approved 2026-10-19.
1. **Done (2026-10-19):** keymap: `&mo 3` on position 36 of the base layer; drop the unused
   `lthp`; README (nav, launcher note), drawing.
2. **Done (2026-10-19):** pushed with `FEAT-14`.
3. Verify: nav arrows come at once; Super+Space on niri; holding `m`
   alone opens COSMIC's launcher.

## FEAT-16: A sticky Accents key instead of the combos

**Priority:** Low for now — to decide after a week with `BUG-7`'s 70 ms
combos (around 2026-10-27). The user thinks it may beat the combos.

**Complexity:** Medium — a sticky layer and a few macros are simple; the
key to put it on is not (every thumb is taken, 2026-10-19).

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
- Capitals (É, À…): AZERTY has no key for them, with combos or ★; a
  separate question.
- Would replace the six combos, or live beside them while learning.

### Implementation Plan
_Not yet discussed._

### Prerequisites
- A week with the 70 ms combos: are they good enough?
- Which key ★ goes on.

