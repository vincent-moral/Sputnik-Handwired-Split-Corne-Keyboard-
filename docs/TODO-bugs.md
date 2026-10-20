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

