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
- Pin target (2026-10-16): `4dd95d7` (ZMK `main` since 2026-10-09), the
  commit today's builds already used, so pinning changes nothing in the
  firmware. The latest release, `v0.3.0` (2025-08-01), is older than
  that and would be a downgrade.
- Known gap: ZMK's reusable workflow runs in the
  `zmkfirmware/zmk-build-arm:stable` image, a floating tag it doesn't let
  callers override. Pinning it would mean copying the whole workflow
  into this repo, not worth it for one toolchain image (accepted
  2026-10-16).

### Implementation Plan
1. **Done (2026-10-16):** pin `config/west.yml` and
   `.github/workflows/build.yml` to `4dd95d7`, with a comment that both
   must move together.
2. Push, then check that CI builds green on the pinned commit.
3. Close: nothing to flash, the firmware is the same as the
   `0acb18b` build.

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
- Confirmed 2026-10-16: the docs-only push of `5df66fb` started a build.
- Fix: `paths-ignore` for `**.md` and `docs/**`. Manual builds stay
  possible through `workflow_dispatch`.

### Implementation Plan
1. **Done (2026-10-16):** replace `paths-before-commit` with
   `paths-ignore`.
2. Push (the push itself changes the workflow, so it builds).
3. Verify with the next docs-only push: no run must start (R3).
