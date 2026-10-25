# Bugs

Things that are wrong today. Reference an entry by its ID (`BUG-N`).

## BUG-5: AltGr stayed held on the PC, cause unknown

**Priority:** Low — seen once (2026-10-17), it cleared by itself.

**Complexity:** Unknown until the cause is known.

### Spec
- On 2026-10-17, every keyboard on the home PC (the Sputnik and the
  Corsair) typed as if AltGr were held. COSMIC keeps one modifier state
  for all keyboards, so one keyboard's lost key release affects them all.
- The journal shows the Sputnik reconnecting at 19:33:28, in the same
  second as a failed lock-screen password, and again at 19:52:07.
- Suspect: AltGr (right thumb, `&kp RALT`) held while the Bluetooth link
  or the link between the halves dropped, so its release never reached
  the PC. Not a profile switch (`BUG-4`): ZMK releases every key before
  switching (`update_current_endpoint` in `endpoints.c` at `4dd95d7`).
- If it happens again: tap the Sputnik's AltGr first, then the Corsair's,
  and note which one clears it and whether the Sputnik had just reconnected
  (`journalctl -b | grep -i clavier`).

### Implementation Plan
_Not yet discussed._

## BUG-8: `` ` `` is a dead key on the work PC

**Priority:** Medium — breaks plug and play: the same key types `` ` `` at
home and waits for a second key at work (seen 2026-10-20).

**Complexity:** _Not yet discussed._

### Spec
- Raise's `` ` `` sends AltGr+7 (`RA(N7)`). On the home PC's xkb `fr`
  (basic) that is a plain `grave`; on the work PC (niri) it arrives as a
  dead key, so `` ` `` needs another key after it.
- Other symbols may differ the same way (`~` is AltGr+2): check them on
  the work PC.

### Implementation Plan
_Not yet discussed._

### Prerequisites
- The work PC's layout: niri's `xkb` block is empty there (read
  2026-10-20), so it comes from `org.freedesktop.locale1`:
  `localectl status` on the work PC (the user brings it on 2026-10-22).

## BUG-9: A fast tap of Low, then a letter, misses the accent

**Priority:** Medium — the user types a plain letter instead of the
accent when going fast (reported 2026-10-25, after several days of use).

**Complexity:** Low — one flavor in one behavior.

### Spec
- Low and Raise share `ltsl`, a hold-tap in hold-preferred mode: as soon
  as another key goes down while the thumb is still down, it is the
  hold. Typing fast, the letter goes down a few ms before the thumb is
  up: Low's layer, where the left letters are `&trans` (plain `e`) and
  the right side is the numpad (Low + `i` gives `8`, not `î`). The 1.5 s
  sticky timeout is unrelated: it only matters when slow, and Accents and
  Mods already share it.
- Fix: the balanced flavor (ZMK `hold-tap.mdx` at `4dd95d7`): the hold
  only if the other key is released first, or the thumb stays down past
  150 ms. A roll that lets go of the thumb first is the tap.
- Cost, on Low only: thumb down, a digit down, the thumb up within
  150 ms before the digit gives the Accents key at that position. On
  Raise the tap opens the same layer as the hold, so a roll types the
  same symbol either way.
- AltGr (`mtsl`) stays hold-preferred (user, 2026-10-25): it is never
  held by hand.
- This goes against `BUG-3`'s lesson (hold-preferred so a layer wins in
  fast rolls) for Low and Raise: that was the Nav thumb, which is a plain
  `&mo` now.

### Implementation Plan
Approved 2026-10-25.
1. **Done (2026-10-25):** keymap: `ltsl` balanced, 150 ms kept; the
   comments, the README notes (Accents, Raise, credits), and the
   key-check page (roll checks for Low and Raise, digits with Low held).
2. Local build **done (2026-10-25)**: only the left `.uf2` changed (the
   right one is byte-identical: the keymap runs on the left). Then push
   to `dev`, then `main`.
3. The user flashes the left half and checks: fast rolls give accents
   and symbols, digits typed with Low held still work. Then close.

