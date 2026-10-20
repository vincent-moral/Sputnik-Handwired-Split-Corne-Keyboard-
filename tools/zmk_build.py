"""Build the firmware locally, the way GitHub Actions does (FEAT-17).

A check before pushing firmware to `dev`, never firmware to flash: the
keyboard only gets what GitHub builds. Mirrors ZMK's
build-user-config.yml at the commit pinned in config/west.yml: same
container image (pinned by digest, R2), every target in build.yaml, then
prints each target's warnings and sizes to compare with the CI log.

Needs podman from the system (rootless podman relies on setuid helpers a
pixi package can't provide). The ZMK and Zephyr download (a few minutes
the first time) stays in .zmk/, which git ignores.

Run with `pixi run build`.
"""

import os
import re
import shutil
import subprocess
import sys

import yaml

# What CI pulled for zmkfirmware/zmk-build-arm:stable (checked 2026-10-18).
IMAGE = ("docker.io/zmkfirmware/zmk-build-arm@sha256:"
         "edb1c953438c6f720ddb79c3762f3972013b7fbbaf4fff3592fc869983e7afc5")
WORKSPACE = ".zmk"


def targets():
    for t in yaml.safe_load(open("build.yaml"))["include"]:
        name = t["shield"] + (f"-{t['snippet']}" if t.get("snippet") else "")
        args = ["-b", t["board"]] + (["-S", t["snippet"]] if t.get("snippet") else [])
        yield name, t["shield"], args


def main():
    if not shutil.which("podman"):
        sys.exit("podman not found: install it from the system's packages.")
    os.makedirs(WORKSPACE, exist_ok=True)
    # A fresh copy of config/ each time, so the build sees the working tree.
    shutil.rmtree(os.path.join(WORKSPACE, "config"), ignore_errors=True)
    shutil.copytree("config", os.path.join(WORKSPACE, "config"))
    builds = "\n".join(
        f'build {name} {shield} {" ".join(args)}' for name, shield, args in targets())
    script = f"""set -euo pipefail
[ -d .west ] || west init -l config
west update --fetch-opt=--filter=tree:0 >/dev/null 2>&1
west zephyr-export >/dev/null
mkdir -p out
build() {{
  local name=$1 shield=$2; shift 2
  if west build -p -s zmk/app -d "build/$name" "$@" -- -DZMK_CONFIG=/ws/config \\
       -DSHIELD="$shield" > "build-$name.log" 2>&1; then
    cp "build/$name/zephyr/zmk.uf2" "out/$name.uf2"; echo "$name: OK"
  else
    echo "$name: FAILED"; tail -40 "build-$name.log"; failed=1
  fi
}}
failed=0
{builds}
exit $failed
"""
    ws = os.path.abspath(WORKSPACE)
    run = subprocess.run(["podman", "run", "--rm", "--userns=keep-id", "-v", f"{ws}:/ws", "-w", "/ws",
                          IMAGE, "bash", "-c", script])
    # The lines worth comparing with the CI log.
    wanted = re.compile(r"^(warning|CMake Dep|.*warning:|.*error:)|FLASH:|RAM:")
    for name, _, _ in targets():
        log = os.path.join(WORKSPACE, f"build-{name}.log")
        if os.path.exists(log):
            print(f"== {name}")
            for line in sorted(set(l.rstrip() for l in open(log) if wanted.search(l))):
                print(line)
    sys.exit(run.returncode)


if __name__ == "__main__":
    main()
