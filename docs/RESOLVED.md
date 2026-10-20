# Resolved

Closed entries whose resolution taught something worth keeping. The
lesson, not a how-to; the change itself is in git.

## BUG-1: ZMK and its build workflow floated on `main`

**Closed:** 2026-10-16

`config/west.yml` and `.github/workflows/build.yml` both followed ZMK's
`main`, so an upstream change could alter the firmware between two builds
of the same keymap. Both are now pinned to the same commit (`4dd95d7`)
and must be upgraded together, in a commit of their own, with ZMK's
changes read.

Two things that weren't obvious:

- ZMK's latest release (`v0.3.0`, 2025-08-01) is far behind `main`:
  "pin to the latest release" would have been a downgrade. Pin to a
  commit, and compare dates before choosing a tag.
- ZMK's reusable workflow builds inside the
  `zmkfirmware/zmk-build-arm:stable` image, a floating tag callers can't
  override, on `ubuntu-latest` runners (moving to Ubuntu 26 from
  2026-10-19, per the CI notice). Accepted as a gap: pinning either means
  copying the whole workflow into this repo. If a build ever breaks or changes with no
  commit here, suspect that image first.

## BUG-2: The build workflow's path filter wasn't a real GitHub Actions key

**Closed:** 2026-10-16

`.github/workflows/build.yml` filtered pushes with `paths-before-commit`,
which GitHub Actions doesn't know. It didn't reject the workflow: it
silently ignored the key, so every push built firmware, docs-only ones
included. Replaced with `paths-ignore` for `**.md` and `docs/**`; the
docs-only push of `b83f135` started no run.

The lesson: a workflow that runs doesn't prove its filters work. Check
the behavior with a push that should be skipped (R3).

## BUG-3: A quick arrow on the nav layer could type Super + a letter

**Closed:** 2026-10-16

The left outer thumb (tap Super, hold nav) used ZMK's `&lt`, which is
tap-preferred with a 200 ms term: thumb + arrow released within 200 ms
gave Super and a letter. It is now a custom hold-tap (`lthp`):
hold-preferred, 150 ms, no `quick-tap-ms`, following Arsenik. Verified
on the keyboard: a quick nav + arrow gives the arrow, and a tap alone
opens COSMIC's launcher.

The lesson: `&lt` suits keys that are mostly tapped. A thumb whose
layer is used in fast rolls needs hold-preferred, so the layer wins as
soon as another key is pressed.

## FEAT-12: A readable Bluetooth name

**Closed:** 2026-10-16

`CONFIG_ZMK_KEYBOARD_NAME="Clavier Vincent"` in `config/corne_hw.conf`
names the keyboard over Bluetooth and USB (`lsusb`), verified on both.

Two things that weren't obvious:

- ZMK caps the name at 16 characters (`BT_DEVICE_NAME_MAX`) so it fits
  in the advertising data: the first choice, "Clavier de Vincent", had 18.
- ZMK keeps the name in its settings, so a new firmware alone doesn't
  apply it: flash `settings_reset` first, which also deletes every
  Bluetooth pairing.

## FEAT-5: Generate the README's layer diagrams from the keymap

**Closed:** 2026-10-17

The README's hand-drawn diagrams are replaced by a drawing generated
with keymap-drawer (`pixi run draw`), which a GitHub Actions workflow
(`draw.yml`) redraws and commits after every keymap push. The same run
attaches a printable A4 `cheatsheet.pdf`. Verified: the README reads
well in GitHub's light and dark themes; a keymap-editor save on a test
branch was followed 12 s later by a "redraw the keymap" commit showing
the change, with no firmware build for that commit.

Things that weren't obvious:

- The drawing found drift on its first run: the hand-drawn low and raise
  diagrams were already wrong. Hand-kept copies of the keymap drift
  even when everyone means to update them (R1).
- keymap-drawer isn't on conda-forge; pixi pins its PyPI release in
  `pixi.lock` all the same, and CI installs from that lockfile, so local
  and CI drawings are byte-identical.
- keymap-drawer draws QWERTY keycode names: the AZERTY legends come
  from `keymap_drawer.config.yaml`, so a new keycode needs an entry
  there or it shows up under its raw name.
- Commits pushed with `GITHUB_TOKEN` start no other workflow, so the
  bot's drawing commit never rebuilds the firmware.
- ImageMagick 6 ignores the SVG's CSS (keys come out as black boxes), so
  inline previews in kitty/neovim through it don't work; librsvg renders
  it correctly, and `:MarkdownPreview` shows it in the browser.
- The editor test confirmed `FEAT-11`: the first save laid the keymap
  out as a grid, with only the edited key changed.

## FEAT-3: LazyVim Ctrl+/ (toggle terminal) on AZERTY

**Closed:** 2026-10-17

Nav + bottom right (`&kp LC(N8)`) toggles LazyVim's terminal, from
normal mode and from inside the terminal. Verified on the keyboard.

Things that weren't obvious:

- Ctrl+/ can't be sent from an AZERTY keyboard at all: `/` is Shift+`:`,
  and kitty's keyboard protocol hands neovim `<C-S-:>`, not `<C-/>`.
- LazyVim also maps the legacy alias `<C-_>`, and `_` is unshifted `8`
  on AZERTY, so Ctrl+`8` reaches it as `<C-_>`. Look for an app's
  alternate binding before calling a shortcut impossible.
- It set the rule now in the README: everything lives on the keyboard,
  nothing in app or OS config; shortcuts it can't handle get tracked.

## FEAT-7: Sticky modifiers and sticky layers

**Closed:** 2026-10-18, together with `FEAT-1` (keys holding two
modifiers at once), which it replaces.

Tapping Raise opens a one-shot Mods layer of sticky modifiers; holding
Raise is unchanged. Verified on the keyboard with a key-test page:
Ctrl+Shift+S both ways, a modifier lapsing after 1 s, Raise still held
for symbols, and kitty's Ctrl+Shift+T.

Things that weren't obvious:

- A layer of sticky modifiers that stays open while you stack them
  makes its own keys untypeable: with the modifiers on the home row,
  Ctrl+S would have been impossible (the user's question). ZMK's default
  `&sl` closes on the first key, modifiers included, which is what's
  wanted; each extra modifier takes one more Raise tap.
- Mixing styles is the short path: one sticky modifier, then the other
  as a home-row mod, as for a capital.
- The compiler isn't on conda-forge, so pixi can't build ZMK, but CI's
  own image (`zmkfirmware/zmk-build-arm`, pinned by digest) runs under
  podman; the local build matched CI's warnings and firmware sizes to
  the byte. Its warnings became `BUG-6` and `FEAT-13`.
- Five layers no longer fit one A4 page: the cheatsheet is two pages.

## FEAT-10: Arsenik's symbols layer for the raise layer

**Closed:** 2026-10-20

Raise holds all 30 programming symbols (Arsenik's layer, from Ergo-L),
none needing Shift; its tap gives one symbol from either hand (since
`FEAT-14`). Low's duplicate symbols were removed. Verified on the
keyboard with the key-check page.

Things that weren't obvious:

- Ækeynox picks AZERTY keycodes per OS: on this Linux `` ` `` and `~`
  are plain with AltGr, but the user's work PC types `` ` `` as a dead key
  (2026-10-20, `BUG-8`). Check symbols on every computer, not one.
- `*` comes from the key next to Enter (`BSLH`), not the keypad: vim's
  `*` search needs the real character.
- Keeping duplicates "while learning" backfired: the user kept reaching
  for the old ones, and asked for them gone after one day.

## FEAT-14: Each sticky tap on the thumb that matches it

**Closed:** 2026-10-20

Raise is symbols, held or tapped; AltGr is modifiers, held or tapped.
Sticky keys wait 1.5 s. Verified on the keyboard.

Things that weren't obvious:

- Two sticky taps on neighbouring thumbs got mixed up within a day. One
  kind of thing per thumb, whether tapped or held, fixed it.
- The `&sl`/`&sk` timeout is changed with copies (`ssl`, `ssk`) in the
  `behaviors` node rather than overrides outside the root node, which
  the keymap-editor might not keep.
- A `raw_binding_map` entry in `keymap_drawer.config.yaml` replaces the
  parsed binding: the layers those thumbs open lost their red "opens the
  layer" mark until 2026-10-20. The draw task now adds the "sticky"
  label after parsing instead.

## FEAT-15: The nav thumb without Super

**Closed:** 2026-10-20

The left outer thumb is plain Nav, instantly; Super is only on the home
row. Verified: Super+Space opens niri's launcher (hold `m`, tap Space),
and `m` held alone sends Super alone, which COSMIC's launcher wants.

## BUG-4: A slip on the Low layer could switch the Bluetooth profile

**Closed:** 2026-10-20

The BT keys live on a layer that only opens while Low and Raise are both
held (a ZMK conditional layer). Verified: Low alone keeps the connection;
Low + Raise switch profiles.

Things that weren't obvious:

- After a profile switch, ZMK stays connected to the old host but stops
  sending it keys (`zmk_ble_prof_select` in `ble.c` at `4dd95d7`): the PC
  showed the keyboard as connected while nothing typed.
- An accepted exception to the same-hand rule (Bluetooth on Low) still
  cost two accidents in three days. Moving it behind both thumbs keeps
  the keys where they were.

