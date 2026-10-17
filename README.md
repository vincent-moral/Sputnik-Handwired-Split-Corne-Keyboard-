# Sputnik Handwired Split Corne – ZMK config

ZMK firmware configuration for a handwired 42-key split Corne (nice!nano, BLE).
The keymap lives in [`config/corne_hw.keymap`](config/corne_hw.keymap).

## Building and flashing

Every push to GitHub triggers the [build workflow](.github/workflows/build.yml).
Download the firmware artifacts from the Actions run and flash both halves
(`corne_hw_left`, `corne_hw_right`). `settings_reset` clears pairing/settings if needed.

The keymap is only changed through this repository: no ZMK Studio edits.

## Layout ground rules

- **The OS layout is French AZERTY.** The keymap sends QWERTY keycodes, so the
  bindings read differently from what is typed (`&kp Q` types `a`, `&kp N4` types `'`,
  `&kp RA(N0)` types `@`, …). The drawing below shows what is *typed*.
- **Home row modifiers**: GUI / Alt / Ctrl / Shift on `q s d f` and `j k l m`.
  The firmware enforces the same-hand rule for them: a home-row key only
  becomes a modifier when the next key is on the other hand or a thumb, or
  when held past 280 ms. To repeat a home-row letter (e.g. `j` in vim), tap
  it, then hold it.
- **Everything lives on the keyboard**, so it works plug and play on any
  machine with an AZERTY layout: no OS or app configuration is needed.
  A shortcut the keyboard can't produce on its own is tracked in the
  backlog, until there are enough of them to choose one strategy for all.
- **Never press two keys at the same time with the same hand.** Layers are held
  with a thumb, and their keys sit on the opposite hand. Accepted exceptions:
  - Bluetooth management on the low layer.
  - Modifier + arrow on the nav layer (selection, word jumps).
- **Accented letters come from combos** on the base layer: press both keys
  together. The drawing shows each combo as a small key between its two
  keys (à, è, é, ç, ù, and `^`, the dead key for ê, î, ô).

## Layers

![The four layers, as typed on the AZERTY OS](keymap-drawer/corne_hw.svg)

The drawing is generated from the keymap: GitHub Actions
redraws it after every keymap change, and `pixi run draw` does the same
locally. Never edit it by hand. To print it: each run of the "Draw
keymap" workflow on GitHub has `cheatsheet.pdf` (A4) to download, and
`pixi run cheatsheet` writes the same file to `keymap-drawer/` (not
committed). Each key shows what the AZERTY OS types;
a small legend below is the modifier or layer when held, and a red key is
the thumb holding that layer.

Layers are held with a thumb, their keys on the other hand:

- **Low** (left thumb): Bluetooth on the left; a numpad on the right. The
  digits are keypad keys: NumLock must be on (`NumLk` toggles it). `*` is
  the keypad `*` and works regardless of NumLock.
- **Raise** (right thumb): symbols on the left.
- **Nav** (left outer thumb, which is Super on a tap): arrows and edit
  shortcuts on the right. `kitty` Copy / Paste are kitty's Ctrl+Shift+C /
  V. `plain ^` types right away (AltGr+9), for vim and regexes; the
  `i + o` combo stays the dead key.

### Nav: how and when to use it

Added 2026-10-16, still a habit to build:

- **Edit shortcuts without a chord:** hold nav, tap one key. Use them
  instead of `k` + a letter for undo, cut, copy, paste and redo
  (Ctrl+Shift+Z), mostly while already on nav.
- **Select then copy in one go:** hold nav, hold `f` (Shift), move with the
  arrows, let go of `f`, tap `Copy` (or `Cut`), all without leaving nav.
- **In kitty, use `kitty` Copy / Paste**, never the plain ones: plain Ctrl+C
  stops the running program and Ctrl+V doesn't paste. They replace
  Ctrl+Shift+C/V, which the same-hand rule makes impossible otherwise
  (Ctrl and Shift are both right-hand home-row mods).
- **LazyVim's terminal: `nvim` Term** (added 2026-10-17) opens it from
  normal mode and hides it from inside. It replaces Ctrl+/, which needs
  Shift on AZERTY: the key sends Ctrl+`_`, LazyVim's built-in alias.

## Credits

- [Arsenik](https://github.com/OneDeadKey/arsenik) and its split variant
  [Selenium](https://onedeadkey.github.io/selenium/), through their ZMK
  implementation [Ækeynox](https://github.com/OneDeadKey/zmk-config-aekeynox):
  the advice behind the home-row mod timing, and the timing of the nav thumb
  key (layer as soon as another key is pressed, Super only on a quick tap),
  and the single-key edit shortcuts on the nav layer.
- [keymap-drawer](https://github.com/caksoylar/keymap-drawer), which draws
  the layers.
- ZMK's [timeless home-row mods](https://zmk.dev/docs/keymaps/behaviors/hold-tap)
  example, which the home-row mod settings follow.
