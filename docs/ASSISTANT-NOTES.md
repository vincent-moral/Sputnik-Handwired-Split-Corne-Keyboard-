# Notes for AI assistants

Lessons and context that outlive any handoff, kept in the repo rather
than in one assistant's private memory (moved here 2026-11-25). The
rules are in [`DEVELOPER-GUIDE.md`](DEVELOPER-GUIDE.md); this file only
adds what the guide doesn't say (R1: link, don't copy).

## The user's setup

- **Two machines, one keyboard:** COSMIC at home (this machine), niri +
  Dank Material Shell at work. A keymap change must work with both
  desktops' shortcuts. The work PC's configs aren't here: they'll come
  from the user's chezmoi repo (2026-11-25), but system settings such as
  the layout (`localectl status`) won't be in it.
- **Daily tools:** Vimium C (Firefox), kitty, LazyVim (mostly default
  configs), plus the window manager.
- **Everything is solved on the keyboard**, never in OS or app config,
  so it's plug and play on any AZERTY computer (user, 2026-10-17). Look
  for a firmware-side trick first (an app's built-in alternate binding,
  a keycode AZERTY types unshifted), test it, and only then track it in
  the backlog as unsolvable.
- **Times in Europe/Paris.** GitHub Actions and API timestamps are UTC:
  convert them, minding the DST switch on the last Sunday of October.

## Habits for this machine

- **zsh treats `=====` as a command** in an echo. Use `---`.
- **`git rebase --autosquash` needs `-i`** on git 2.43, which isn't
  available here. To squash a fixup into the last commit: `git commit
  --amend`; deeper: detached checkout, `cherry-pick -n`, `--amend`,
  cherry-pick the rest, `git branch -f main`.
- **No `node` on this machine:** the key-check page's JavaScript can't
  be syntax-checked before publishing. If the page shows nothing, look
  at its `CHECKS` block first.
- **The scratchpad is wiped between sessions:** the key-check page lives
  in `tools/`; read the artifact by URL if the file is ever behind.
- **A claude.ai session linked to the computer has no shell**
  (2026-11-18): give each write-back a new staged file name, then check
  the size on disk.
