---
name: key-check
description: "Rewrite tools/key-check.html's checklist for a new firmware and republish it as the pinned \"Sputnik Key Check\" artifact, then record the user's results. Use after a firmware change is built, before the user flashes or tests it."
---

# Prepare the key check

Rules: `docs/DEVELOPER-GUIDE.md` §1 step 5. The page is
`tools/key-check.html`, published at
https://claude.ai/artifact/Lykm8JfAtP6KVqetzvraFx (pinned). The repo
file is the source; the publish adds its own document wrapper.

1. **Sync the page with the keymap:** `LAYERS` is a hand copy of
   `config/corne_hw.keymap` as typed on AZERTY. Update every changed key
   (and `ACCENTS` if accents moved).
2. **Rewrite `CHECKS`** for this firmware: one check per changed
   behavior, plus regressions it could break (Bluetooth layer, the
   other thumb, the tap lapse). Each check has `g` (backlog ID), a
   unique `id`, `title`, `layer`, `keys` (positions), `steps`, `how`,
   and `ok` when the page can tell by itself from the key event;
   otherwise it's the user's call. Never tell the user to tap BT clr.
3. **Bump `RES`** (e.g. `res-MMDD`) so old results don't carry over,
   and update the report header in `renderReport` (date and IDs).
4. **Publish** with the Artifact tool from `tools/key-check.html` to the
   URL above (read it first if this session hasn't). Commit the page as
   `chore(<ID>): key check for <what>`, "Effect on push: docs only"
   (`tools/**` starts no build).
5. **Results:** the user pastes the report. Record in the entry only
   what it says; a check they didn't report is "not reported", not
   passed. Then `close-entry` if everything works.
