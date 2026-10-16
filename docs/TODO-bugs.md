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
- Study (2026-10-16): fits the ground rules; it fixes a change made the
  same day and moves no key.

### Implementation Plan
Approved 2026-10-16.
1. **Done (2026-10-16):** add a hold-tap behavior to `config/corne_hw.keymap`: `hold-preferred`,
   `tapping-term-ms` 150, `&mo` on hold and `&kp` on tap. No
   `quick-tap-ms`: tapping Super and then holding for nav must give nav.
2. **Done (2026-10-16):** use it instead of `&lt 3 LGUI`.
3. **Done (2026-10-16):** README credits Arsenik for it (guide §4).
4. **Done (2026-10-16):** pushed and checked with `FEAT-6` (dev branch,
   then `main` at `7a40cc5`), as a separate commit.
5. Flash and verify: tapping the thumb alone opens COSMIC's launcher; a
   quick nav + arrow gives the arrow, never Super.

### Prerequisites
- None left.
