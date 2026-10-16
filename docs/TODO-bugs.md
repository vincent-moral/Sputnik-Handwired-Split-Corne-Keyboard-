# Bugs

Things that are wrong today. Reference an entry by its ID (e.g. `BUG-2`).

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
