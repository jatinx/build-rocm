# Build Script for ROCm - Work in progress

The idea is to have a script which builds ROCm from its public sources. Its work in progress and expect more additions to it.

## How to run

`python build.py -h`

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
