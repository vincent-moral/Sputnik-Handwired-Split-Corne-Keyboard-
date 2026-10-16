# Features

Capabilities to add that don't exist yet. Reference an entry by its ID (e.g. `FEAT-2`).

## FEAT-1: Keys for shortcuts with two modifiers

**Priority:** High — kitty (Ctrl+Shift for copy, paste, tabs, windows,
font size), niri and COSMIC (Super+Ctrl / Super+Shift to move windows)
use them daily, and none can be typed without breaking the same-hand rule.

**Complexity:** Medium — the ZMK side is simple (a hold-tap whose hold is
a modifier combination), but the right keys and combinations depend on
the niri bindings, which aren't known yet.

**Depends on** the niri config (see Prerequisites).

### Spec
- With home-row mods, a shortcut with two modifiers always makes one hand
  hold two keys at once.
- Proposed (2026-10-16): one key per hand that holds two modifiers at
  once, so a two-modifier shortcut becomes one held key plus the key on
  the other hand:
  - bottom-left `⇧` (position 24, redundant with home-row Shift) holds
    Ctrl+Shift;
  - Print Screen (position 35) prints on tap and holds Ctrl+Shift;
  - a Super+Ctrl and/or Super+Shift key placed the same way, once the
    niri bindings are known.
- Alternative from Arsenik: sticky modifiers (`FEAT-7`) solve the same
  problem without new keys.
- App side, outside this repo: in `~/.config/kitty/kitty.conf`,
  `map ctrl+c copy_or_interrupt` and `map ctrl+v paste_from_clipboard`
  remove the need for Ctrl+Shift for copy and paste.

### Implementation Plan
_Not yet discussed._

### Prerequisites
- The user's niri `config.kdl` and any custom Dank Material Shell
  keybindings from the work PC.

## FEAT-2: Plain `^` for vim and regexes

**Priority:** Medium — `^` (start of line in vim, anchor in regexes) is
only reachable as the dead key from the `i+o` combo, which waits for a
second key.

**Complexity:** Low — one binding.

**Quick win:** yes, one key on a free slot of the nav layer.

### Spec
- On AZERTY, AltGr+9 (`RA(N9)`) types a non-dead `^`.
- Proposed (2026-10-16): put it on the nav layer, next to Home and End,
  mirroring vim's `^` and `$` (line start and end). The dead key stays on
  the combo for ê, î, ô.

### Implementation Plan
_Not yet discussed._

## FEAT-3: LazyVim Ctrl+/ (toggle terminal) on AZERTY

**Priority:** Low — `/` needs Shift on AZERTY, so Ctrl+/ is a
three-key chord.

**Complexity:** Low — a mapping in `~/.config/nvim/lua/config/keymaps.lua`,
outside this repo.

### Spec
- Remap the terminal toggle to a key that doesn't need Shift. Which one
  is _not yet discussed_.

### Implementation Plan
_Not yet discussed._

## FEAT-4: Workspace switching by number on niri and COSMIC

**Priority:** Low until confirmed — the digits on the low layer are
keypad keys, so Super+1…9 bound to number-row keys probably won't match,
and Super on the left pinky plus the low layer on the left thumb breaks
the same-hand rule anyway.

**Complexity:** _Not yet discussed._

**Depends on** the niri config (`FEAT-1`'s Prerequisites).

### Spec
- Unconfirmed (2026-10-16): whether Super+keypad digit triggers niri's
  and COSMIC's workspace shortcuts on an AZERTY layout. Super+U/I and
  Super+PgUp/PgDn are the alternatives.

### Implementation Plan
_Not yet discussed._

### Prerequisites
- Does the user switch workspaces by number?

## FEAT-5: Generate the README's layer diagrams from the keymap

**Priority:** Low — the hand-drawn diagrams duplicate the keymap (R1)
and drift as soon as one is edited without the other, which every
keymap-editor commit does. The keymap-editor's own view is QWERTY only,
so today the README is the only place showing what AZERTY types.

**Complexity:** Medium — keymap-drawer parses ZMK keymaps, but its
legends show QWERTY keycodes: it needs a mapping to what AZERTY types.

### Spec
- Generate SVG diagrams with a pinned keymap-drawer, ideally in CI, and
  embed them in the README instead of the text diagrams.

### Implementation Plan
_Not yet discussed._

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
4. The user opens and saves the keymap in keymap-editor: check that the
   behaviors survive.
5. Push to a `dev` branch, read the run's jobs and annotations, then
   fast-forward `main`.
6. Flash and verify: fast rolls (`le`, `la`, `sd`, `de`, `fr`) give
   letters; `k`+`c` copies; a capital right after a space works; Shift +
   nav + arrow selects; tap-then-hold `j` repeats.
7. Tune the timings after a week of daily use.

### Prerequisites
- Plan approved 2026-10-16. Holding `j`/`k`: tap-then-hold for now;
  hjkl arrows on the nav layer are deferred until the user has more
  experience with arrows on this keyboard.

## FEAT-7: Sticky modifiers and sticky layers

**Priority:** Medium — tapping a modifier or layer key, then the key,
turns every chord into a sequence: the purest form of the same-hand rule.

**Complexity:** Medium — ZMK's `&sk` and `&sl` exist; the work is
deciding which keys become sticky and how they combine with the holds.

**From Arsenik** (guide §4): sticky Shift and Sym on the thumbs,
and Callum-style one-shot mods on a layer.

### Spec
- Alternative to `FEAT-1`'s combined-modifier keys: Ctrl+Shift+C becomes
  tap Ctrl, tap Shift, tap C; niri and COSMIC's Super+Shift+… the same.
- A sticky raise key would make right-hand symbols reachable without
  breaking the same-hand rule (tap raise, then any symbol), which gives
  room for all symbols on one layer (`FEAT-10`).
- ZMK defaults (`4dd95d7`): sticky keys release after 1000 ms;
  Ækeynox adds `quick-release` to `&sk` to avoid false positives.

### Implementation Plan
_Not yet discussed._

### Prerequisites
- Study with the user: does it fit the README's ground rules?

## FEAT-8: One accent key (1dk) instead of the accent combos

**Priority:** Medium — capital accented letters (É, À, Ç, È) can't be
typed at all today: Shift plus an accent combo types a digit. This gap
exists whether or not 1dk is adopted.

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

### Implementation Plan
_Not yet discussed._

### Prerequisites
- Study with the user: does it fit the README's ground rules?

## FEAT-10: Study Arsenik's symbols layer for the raise layer

**Priority:** Low — the raise layer has no muscle memory yet (the user
knows the base and number layers well, as of 2026-10-16), so it can still
be redesigned freely.

**Complexity:** Medium — the layer uses both hands, which needs sticky
raise (`FEAT-7`) under the same-hand rule.

**From Arsenik** (guide §4): its symbols layer, taken from
Ergo-L, with AZERTY keycodes in Ækeynox's `aliases/azerty.h`.

### Spec
- All 30 programming symbols on one layer, none needing Shift, the most
  frequent (`{ ( ) } =`) on the left home row, common sequences without
  same-finger bigrams, designed with vim in mind.
- Would replace today's raise layer and the symbols around the numpad on
  the low layer.

### Implementation Plan
_Not yet discussed._

### Prerequisites
- Study with the user: does it fit the README's ground rules?
