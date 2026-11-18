---
name: handoff
description: "Write or update docs/HANDOFF.md so a fresh session can resume the work in flight. Use before a context compaction, /clear, or the end of a work session, or when the user asks for a handoff."
---

# Write the handoff

The shape is defined in `docs/DEVELOPER-GUIDE.md` §1 "Handoffs"; read it
first. This skill is the procedure, not the rules.

1. **Gather facts, don't recall them.** Run `git status`, `git log
   --oneline origin/main..HEAD` (unpushed commits), `git log --oneline
   -15`, `git branch -a` (is a `dev` branch waiting?) and `gh run list
   --limit 3`. Read the open entries in `docs/TODO-bugs.md` and
   `docs/TODO-features.md`.
2. **Write the five sections, in order:**
   - **Goal:** one or two sentences on what the work is for.
   - **Problems we're solving:** backlog IDs with one line each on why
     they matter and where they stand. Link to the entry; don't restate
     its plan (R1).
   - **Main files:** the paths changed or checked this session.
   - **What failed:** every dead end, wrong assumption, failed command
     and mistake from this session (including your own), each with what
     to do instead. Be candid; this is the section that saves the next
     session the most time. It holds the **current work's** lessons
     only: when updating an older handoff, promote what will still
     matter (step 4) and drop the rest, which git history keeps.
   - **Plan:** ordered next steps, each with how to verify it (exact
     read-only commands, or what to type on the keyboard and expect).
   Then add "Waiting on the user" (dumps, keyboard tests, reviews with
   their date), "In progress" if a build is running or a firmware is
   flashed but not yet checked, the working agreements (keep the
   existing ones) and a ready-to-paste first prompt that names the first
   check and repeats "don't push without asking".
3. **Dates and times:** absolute dates; times in Europe/Paris, noting
   when a log (GitHub Actions) is in UTC.
4. **Promote lasting lessons.** For each "What failed" item that will
   still matter after the handoff is deleted, propose where it belongs:
   a rule in the guide, a backlog entry, `docs/RESOLVED.md`, a comment
   in the keymap or a tool, a repo skill, or the assistant's memory (an
   assistant habit, such as shell quoting). Ask before adding a rule.
5. **No secrets** (an ApeKey or any token), not even partial values.
6. Commit as `docs: handoff <date>` with "Effect on push: docs only".
   Unpushed commits are listed in the handoff; don't push without
   approval.

If every item is closed, delete `docs/HANDOFF.md` instead.
