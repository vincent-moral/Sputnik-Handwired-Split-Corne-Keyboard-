# Bugs

Things that are wrong today. Reference an entry by its ID (e.g. `BUG-1`).

## BUG-1: ZMK and its build workflow float on `main`

**Priority:** Medium — any upstream ZMK change lands in the next build
without a commit here: the same keymap can build differently, or stop
building, from one push to the next (R2).

**Complexity:** Low — pin two references, but the target version needs
choosing and a test build.

### Spec
- `config/west.yml` has `revision: main` for ZMK.
- `.github/workflows/build.yml` uses
  `zmkfirmware/zmk/.github/workflows/build-user-config.yml@main`.
- Both should point to the same release tag or commit SHA, and upgrades
  become their own commit with release notes read.

### Implementation Plan
_Not yet discussed._

## BUG-2: The build workflow's path filter isn't a real GitHub Actions key

**Priority:** Low — every push builds firmware, including docs-only
pushes, which wastes a run and makes "did my keymap build?" harder to
read.

**Complexity:** Low — replace one key.

**Quick win:** yes.

### Spec
- `.github/workflows/build.yml` filters `push` with `paths-before-commit`,
  which GitHub Actions doesn't know (`paths` and `paths-ignore` are the
  real keys). As of 2026-10-16 runs start on every push, so it appears
  to be ignored.
- Fix: `paths-ignore` for `**.md` and `docs/**`. Verify after pushing
  that a docs-only push starts no run (R3).

### Implementation Plan
_Not yet discussed._
