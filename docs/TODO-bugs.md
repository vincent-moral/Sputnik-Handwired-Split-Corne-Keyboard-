# Bugs

Things that are wrong today. Reference an entry by its ID (`BUG-N`).

## BUG-4: A slip on the Low layer can switch the Bluetooth profile

**Priority:** Low — it happened once (2026-10-17) and one key press
(`BT_SEL 1`) fixes it. The user keeps the layout as is for now.

**Complexity:** Low — moving five keys to a new layer.

### Spec
- On 2026-10-17 the Sputnik showed as connected on the home PC, but no
  key typed. `BT_SEL 1` on the left half brought it back.
- Why it looked connected (ZMK `ble.c` at `4dd95d7`): `zmk_ble_prof_select`
  only changes which host gets the reports; the old host stays connected.
- Likely cause, not proven: on Low (left thumb), the left home row holds
  `BT_CLR` and `BT_SEL 0`–`4`, while Low's digits are on the right half.
  Touching a left home-row key while typing digits switches the profile.
  `BT_CLR` in the same row would erase the active profile's pairing.
- Idea (2026-10-17, not adopted): put the BT keys on their own layer,
  reached only while both Low and Raise are held (a ZMK conditional
  layer). This changes the README's Bluetooth exception, so it needs the
  user's approval. A smaller option: move only `BT_CLR` somewhere harder
  to reach.

- Happened again (user, 2026-10-18): "when I am confused, I press the
  BT keys by mistake". The user approved the layer idea (2026-10-19),
  which changes the README's Bluetooth exception.

### Implementation Plan
Approved 2026-10-19.
1. Keymap: a sixth layer, BT, with the BT keys where they are today
   (outer left home key, then `q s d f g`), opened by holding Low and
   Raise together (ZMK conditional layer: `if-layers` 1 and 2, checked
   in `zmk,conditional-layers.yaml` at `4dd95d7`); Low's BT keys become
   transparent like the rest of its left half. README ground rule,
   drawing.
2. Pushed with `FEAT-14`.
3. Verify: Low + a former BT key types its letter and keeps the
   connection; Low + Raise + BT key of the current profile works.

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

## BUG-6: The right half asks for USB keyboard support it can't have

**Priority:** Low — a build warning only; the firmware works.

**Complexity:** Low — likely one Kconfig block.

### Spec
- Every build of the right half warns (seen 2026-10-18, locally and in
  CI run `39041569923`): `ZMK_USB ... was assigned the value 'y' but got
  the value 'n'`.
- `config/boards/shields/corne_hw_right/Kconfig.defconfig` sets
  `ZMK_USB` to `y`, but the right half is the split peripheral: it sends
  its keys to the left half, never to a computer, so ZMK turns USB off.
- To check before changing it (R3): whether the right half still flashes
  and charges over USB without it, and whether the left half needs the
  line at all or gets it from the board.

### Implementation Plan
_Not yet discussed._

## BUG-7: Combos miss when typing fast

**Priority:** Medium — the user gets `er` instead of `é` when typing
fast (2026-10-18/19).

**Complexity:** Low — one value per combo, but a trade-off.

### Spec
- The six accent combos use a 50 ms `timeout-ms`: both keys must go
  down within it. Typing fast, the two presses drift further apart.
- Raise it to 70 ms. The cost: a fast roll on the same pair (`er`, `ze`,
  `az`, `xc`, `ui`, `io`, all common in French) is likelier to become
  the accent instead. A combo only fires when both keys are down
  together, so a roll that releases the first key first stays letters.
  Watch for that, and tune.

### Implementation Plan
Approved 2026-10-19.
1. **Done (2026-10-19):** keymap: `timeout-ms` 70 on the six combos.
   Checked in ZMK `combo.c` at `4dd95d7`: a key released while a combo
   is pending replays the presses as letters (`position_state_up`).
2. Pushed with `FEAT-14`.
3. Verify with the key-check page's French sentence, then a week of
   use: do combos still miss? Does `é` appear for `er`?

