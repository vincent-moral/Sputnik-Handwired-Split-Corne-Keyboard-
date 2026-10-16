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
