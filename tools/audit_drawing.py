"""Check the README's drawing against what the keyboard really types (FEAT-17).

For every binding in config/corne_hw.keymap, work out what the AZERTY OS
types (xkb `fr` basic, from the pixi-pinned xkeyboard-config) and compare
it with the legend in keymap-drawer/corne_hw.yaml. Also check that every
layer but Base marks the thumb that opens it (lost once, 2026-10-19).

Run with `pixi run audit`; exits 1 and lists every mismatch.
"""

import os
import re
import sys
import unicodedata

import yaml

XKB = os.path.join(os.environ.get("CONDA_PREFIX", "/usr"), "share/X11/xkb/symbols")
KEYMAP = "config/corne_hw.keymap"
DRAWING = "keymap-drawer/corne_hw.yaml"


def xkb_section(path, name):
    text = open(os.path.join(XKB, path)).read()
    m = re.search(r'xkb_symbols "%s" \{(.*?)\n\};' % name, text, re.S)
    return m.group(1) if m else text


# Later files override earlier ones, as fr(basic) includes latin, then pc.
LEVELS = {}
for path, name in [("pc", "pc105"), ("latin", "basic"), ("fr", "basic")]:
    for key, levels in re.findall(r"key <(\w+)>\s*\{\s*\[([^\]]*)\]", xkb_section(path, name)):
        LEVELS[key] = [lv.strip() for lv in levels.split(",")]

KEYSYMS = {
    "ampersand": "&", "eacute": "é", "quotedbl": '"', "apostrophe": "'", "parenleft": "(",
    "minus": "-", "egrave": "è", "underscore": "_", "ccedilla": "ç", "agrave": "à",
    "parenright": ")", "equal": "=", "plus": "+", "asciitilde": "~", "numbersign": "#",
    "braceleft": "{", "bracketleft": "[", "bar": "|", "grave": "`", "backslash": "\\",
    "asciicircum": "^", "at": "@", "bracketright": "]", "braceright": "}", "dollar": "$",
    "ugrave": "ù", "percent": "%", "asterisk": "*", "comma": ",", "question": "?",
    "semicolon": ";", "period": ".", "colon": ":", "slash": "/", "exclam": "!",
    "less": "<", "greater": ">", "EuroSign": "€",
}
COMBINING = {"dead_circumflex": "̂", "dead_diaeresis": "̈"}

# ZMK keycode -> xkb key name (the QWERTY position it sits on).
XKB_KEY = {"BSLH": "BKSL", "NUBS": "LSGT"}
for row, names in [("AE", "N1 N2 N3 N4 N5 N6 N7 N8 N9 N0 MINUS EQUAL"),
                   ("AD", "Q W E R T Y U I O P LBKT RBKT"),
                   ("AC", "A S D F G H J K L SEMI SQT"),
                   ("AB", "Z X C V B N M COMMA DOT FSLH")]:
    for i, name in enumerate(names.split()):
        XKB_KEY[name] = "%s%02d" % (row, i + 1)


def types(keycode):
    """What `&kp keycode` types; None if it isn't a printing key."""
    mods = set()
    while m := re.match(r"(LS|RS|RA|LC|RC|LA|LG)\((.*)\)$", keycode):
        mods.add(m.group(1))
        keycode = m.group(2)
    if keycode not in XKB_KEY or mods - {"LS", "RS", "RA"}:
        return None
    levels = LEVELS[XKB_KEY[keycode]]
    level = (2 if "RA" in mods else 0) + (1 if mods & {"LS", "RS"} else 0)
    return KEYSYMS.get(levels[level], levels[level])


def dead_then(dead_keycode, vowel_keycode):
    """A dead key, then a vowel: the composed letter."""
    return unicodedata.normalize("NFC", types(vowel_keycode) + COMBINING[types(dead_keycode)])


# The Accents layer's macros (FEAT-16): which dead key each one sends first.
MACROS = {"circ": "LBKT", "trema": "LS(LBKT)"}


def expected(binding):
    if m := re.match(r"&kp (\S+)$", binding):
        return types(m.group(1))
    if m := re.match(r"&(hml|hmr|hsl|hsr) \w+ (\S+)$", binding):
        return types(m.group(2))
    if m := re.match(r"&(\w+) (\S+)$", binding):
        if m.group(1) in MACROS:
            return dead_then(MACROS[m.group(1)], m.group(2))
    return None


def main():
    keymap = open(KEYMAP).read()
    layers = re.findall(r"\w+_layer \{\n(?:.*?\n)*?\s*bindings = <\n(.*?)\n\s*>;", keymap)
    drawn = yaml.safe_load(open(DRAWING))["layers"]
    problems, checked = [], 0
    if len(layers) != len(drawn):
        problems.append(f"{len(layers)} layers in the keymap, {len(drawn)} in the drawing")
    for bindings, (name, legends) in zip(layers, drawn.items()):
        for pos, (binding, legend) in enumerate(zip(bindings.split("  "), legends)):
            want = expected(binding)
            if want is None:
                continue
            checked += 1
            got = legend if isinstance(legend, str) else legend.get("t", "")
            # Letters are drawn as capitals on purpose.
            if str(got).lower() != want.lower():
                problems.append(f"{name} {pos}: {binding} types {want!r}, drawn {got!r}")
        if name != "Base" and not any(isinstance(k, dict) and k.get("type") == "held" for k in legends):
            problems.append(f"{name}: no thumb marked as opening the layer")
    for p in problems:
        print(p)
    print(f"{checked} legends checked against xkb fr(basic), {len(drawn)} layers: "
          f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
