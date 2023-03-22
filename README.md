# Build Script for HIP

This script builds ROCm from scratch. It assumes that you have driver intalled and builds contents on top.

## How to run

`python build.py`

## Prereq

Make sure amdgpu driver is installed.

pip packages:

- `alive_progress`
- `gitpython`
- `argparse`

## Options

- `--help` : show help
- `--build-dir` : directory where build is kept. Default is `build/` inside same folder.
- `--install-dir` : where build components are installed. Default is `install/` inside same folder.
- `--git-dir` : where git checkout stuff is kept
- `--clean-all` : deletes build directory and git checkout stuff
- `--clean-build` : delete build dir
- `--clean-git` : delete git dir
- `--uninstall` : delete install dir
- `--show-status` : show status
