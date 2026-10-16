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
