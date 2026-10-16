# Bugs

Things that are wrong today. Reference an entry by its ID (e.g. `BUG-3`).

## BUG-3: A quick arrow on the nav layer can type Super + a letter

**Priority:** Medium — the left outer thumb (tap Super, hold nav, added
2026-10-16) uses ZMK's default `&lt`: tap-preferred, 200 ms (checked in
ZMK `4dd95d7`). Holding it, pressing an arrow and releasing the thumb
within 200 ms sends a Super tap (opens COSMIC's launcher) and the base
layer's letter instead of the arrow.

**Complexity:** Low — one custom hold-tap behavior.

**From Arsenik** (guide §4): thumb keys that combine
a layer and a tap are hold-preferred with a short term (150 ms), so the
layer is immediate and the tap only happens when the thumb is tapped alone.

### Spec
- Replace `&lt 3 LGUI` with a hold-preferred layer-tap.
- Whether the user has hit it yet is unknown: the keymap isn't flashed.

### Implementation Plan
_Not yet discussed._

### Prerequisites
- Study with the user: does it fit the README's ground rules?
