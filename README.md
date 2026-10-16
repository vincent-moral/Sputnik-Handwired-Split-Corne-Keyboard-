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
  `&kp RA(N0)` types `@`, …). The diagrams below show what is *typed*.
- **Home row modifiers**: GUI / Alt / Ctrl / Shift on `q s d f` and `j k l m`.
  The firmware enforces the same-hand rule for them: a home-row key only
  becomes a modifier when the next key is on the other hand or a thumb, or
  when held past 280 ms. To repeat a home-row letter (e.g. `j` in vim), tap
  it, then hold it.
- **Never press two keys at the same time with the same hand.** Layers are held
  with a thumb, and their keys sit on the opposite hand. Accepted exceptions:
  - Bluetooth management on the low layer.
  - Modifier + arrow on the nav layer (selection, word jumps).
- **Accented letters come from combos** on the base layer (press both keys together):

  | Keys  | Output |
  |-------|--------|
  | a + z | à      |
  | z + e | è      |
  | e + r | é      |
  | x + c | ç      |
  | u + i | ù      |
  | i + o | ^ (dead key) |

## Layers

### Base

```
 tab   a    z    e    r    t   |  y    u    i    o    p   bspc
 esc   q⌘   s⌥   d⌃   f⇧   g   |  h    j⇧   k⌃   l⌥   m⌘   '
 ⇧     w    x    c    v    b   |  n    ,    ;    :    !   prtsc
          gui/NAV  LOW  space  |  ret  RAISE  altgr
```

The left outer thumb is GUI on tap and the nav layer on hold.

### Raise (hold right thumb, left hand)

```
 `     "    '    =    (    )
 ctrl  @    [    ]    <    >
 \     #    _    +    -    |
```

### Low (hold left thumb, right hand)

```
 BT clr  BT0  BT1  BT2  BT3  BT4  |  num  7  8  9  *  bspc
                                  |   {   4  5  6  }   $
 ⇧                                |   &   1  2  3  %   ~
                                  |       0
```

The digits are keypad keys: NumLock must be on (`num` toggles it).
`*` is the keypad `*` and works regardless of NumLock.

### Nav (hold left outer thumb, right hand)

```
 pgup  home  ↑    end   ^   del
 pgdn  ←     ↓    →     ·   ·
```

`^` here types right away (AltGr+9), for vim and regexes; the `i + o`
combo stays the dead key for ê, î, ô.

## Credits

- [Arsenik](https://github.com/OneDeadKey/arsenik) and its split variant
  [Selenium](https://onedeadkey.github.io/selenium/), through their ZMK
  implementation [Ækeynox](https://github.com/OneDeadKey/zmk-config-aekeynox):
  the advice behind the home-row mod timing, and the timing of the nav thumb
  key (layer as soon as another key is pressed, Super only on a quick tap).
- ZMK's [timeless home-row mods](https://zmk.dev/docs/keymaps/behaviors/hold-tap)
  example, which the home-row mod settings follow.
