---
name: ship-firmware
description: "Push a firmware change through dev, check the GitHub Actions build, then fast-forward main and delete dev. Use once the user has approved pushing a commit that changes the firmware."
---

# Ship a firmware change

Rules: `docs/DEVELOPER-GUIDE.md` §1 steps 3-4. Each push needs the
user's explicit approval: the push to `dev` and the fast-forward of
`main` are two separate approvals unless they gave both at once.

1. **Before pushing:** `pixi run build` passed on this exact commit,
   `git status` is clean, and `git fetch` shows `main` hasn't moved. If
   it has (a keymap-editor commit), rebase onto `origin/main`, rebuild
   locally, and say so.
2. **Push to `dev`:** `git push origin HEAD:dev` (after approval).
3. **Watch the build:** `gh run list --branch dev --limit 3`, then
   `gh run watch <id> --exit-status`. Read every job's result and every
   annotation (check-runs API), not just the overall colour. Check
   whether the draw workflow added a "redraw the keymap" commit on
   `dev`. Times in the API are UTC: report them in Europe/Paris.
4. **Report** to the user: green or not, warnings, and which `.uf2`
   artifact to flash. "Green" only proves it compiles.
5. **Fast-forward `main`** (after approval): `git push origin
   origin/dev:main` (includes a redraw commit if there is one), then
   `git push origin --delete dev`, `git pull`. Never merge; never
   fast-forward an untested rebase.
6. **Verification is next:** the entry stays open until the user checks
   the firmware on the keyboard (`key-check`).
