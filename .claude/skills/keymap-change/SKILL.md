---
name: keymap-change
description: "Make a change to the keymap or the shield (config/corne_hw.keymap, .conf, boards/shields/corne_hw/) as one ready-to-push commit: ground-rule check, drawing, audit, README note, local build. Use for any change that alters the firmware."
---

# Change the keymap

Rules: `docs/DEVELOPER-GUIDE.md` §1 steps 1-2, R1-R4, and the ground
rules in `README.md#layout-ground-rules`.

1. **Start from the remote.** `git pull`: the keymap-editor commits
   straight to `main`.
2. **Backlog first.** The entry has a Spec and an Implementation Plan
   the user agreed to. Keep the user's decisions: a key they placed or
   an accepted exception only moves if they said so.
3. **Check the ground rules** for every changed key: home-row mods kept;
   no two keys pressed at once with the same hand (except Bluetooth);
   the character AZERTY actually types for the QWERTY keycode sent
   (dead keys, keypad vs number-row digits: R3). For a ZMK behavior,
   confirm it in the ZMK source or docs at the pinned revision
   (`config/west.yml`), not from memory.
4. **Edit**, keeping the keymap-editor's grid format (one row per line,
   laid out from `config/corne_hw.json`). Comments say why (R4). A new
   keycode needs its AZERTY legend in `keymap_drawer.config.yaml`.
5. **Docs in the same commit:** `pixi run audit` (redraws, then checks
   every legend), commit the `keymap-drawer/` files; a "how and when to
   use it" note under the layer in `README.md`; fix any README text or
   comment the change contradicts; an Arsenik credit if the idea came
   from there (guide §4).
6. **Build locally:** `pixi run build` (podman). Every target must
   build; read the warnings. For a refactor that shouldn't change the
   firmware, compare the `.uf2` sha256 with a build of the previous
   commit. Never flash these `.uf2` files.
   - `tools/zmk_build.py` prints the warnings after all the sizes, not
     per target. Before calling a warning new or explaining it, build
     the previous commit's keymap and compare: `git checkout <commit> --
     config/`, `pixi run build`, `git checkout HEAD -- config/` (the
     build copies the working tree's `config/`). Same warnings: not
     from this change.
7. **Commit** as `feat|fix(<ID>): what` with the why and "Effect on
   push: CI builds new firmware; nothing changes until flashed". Mark
   the plan step **Done (date)**. Stop and ask before pushing; pushing
   is `ship-firmware`.
