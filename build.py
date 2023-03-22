#!/usr/bin/env python

from components import helpers
import os
from alive_progress import alive_bar
import subprocess
import argparse
import pickle

component_file = 'components.json'
component_file_og = '.components.og.json'

current_path = os.getcwd()
repos_dump_file = current_path + '/.repos.dump'


def delete_git_repo(git_dir):
    with alive_bar(2, title="Directory clean", dual_line=True) as bar:
        bar.text = 'Deleting: ' + git_dir
        bar()
        helpers.delete_dir(git_dir)
        bar.text = 'Creating: ' + git_dir
        bar()
        helpers.create_dir(git_dir)
        return git_dir


def clone_repo(git_dir):
    git_dir = delete_git_repo(git_dir)
    components = helpers.open_json_file(component_file)
    repos = []
    with alive_bar(len(components['components']), title='Download repo', dual_line=True) as bar:
        for c in components['components']:
            bar.text = 'Downloading ' + \
                c['name'] + ' from: ' + c['url'] + ' branch: ' + c['branch']
            checkout_path = ''
            if 'path' not in c:
                c['path'] = git_dir + c['name']
            checkout_path = c['path']
            repo = helpers.git_checkout(c['url'], c['branch'],
                                        checkout_path)
            repos.append(repo)
            bar()
    helpers.dump_json_to_file(components, component_file)
    helpers.delete_file(repos_dump_file)
    with open(repos_dump_file, "wb") as outfile:
        pickle.dump(repos, outfile)


def cmake_command(path, build_path, install, options=''):
    cmake_str = 'cmake -B' + build_path + ' -S' + path + ' -DCMAKE_INSTALL_PREFIX=' + \
        install + ' -DCMAKE_BUILD_TYPE=Debug -G Ninja ' + options
    return cmake_str


def update_repos():
    repos = []
    with open(repos_dump_file, "rb") as infile:
        repos = pickle.load(infile)
    with alive_bar(len(repos), title='Update repos', dual_line=True) as bar:
        for repo in repos:
            bar.text = 'Pulling ' + repo.working_dir
            for remote in repo.remotes:
                remote.pull()
            bar()


def build_hip(build_dir, install_dir, verbose=False):
    # To build hip we need 2 things
    # 1. Path to headers
    # 2. Path to rocclr/opencl - taken care by default naming scheme
    components = helpers.open_json_file(component_file)
    hip = ''
    hipamd = ''
    for c in components['components']:
        if c['name'] == 'hip':
            hip = c['path']
        if c['name'] == 'hipamd':
            hipamd = c['path']

    cmake_str = cmake_command(
        hipamd, build_dir, install_dir, '-DHIP_COMMON_DIR=' + hip + ' -DHIP_CATCH_TESTS=1')
    if verbose:
        print('CMake command: ', cmake_str)
    subprocess.check_call(cmake_str, shell=True)
    subprocess.check_call('cmake --build .', shell=True, cwd=build_dir)
    subprocess.check_call('cmake --install .', shell=True, cwd=build_dir)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Build ROCm components on local machine')
    argparser.add_argument('--build-dir', type=str, help='add build location')
    argparser.add_argument('--install-dir', type=str,
                           help='add install location')
    argparser.add_argument('--git-dir', type=str,
                           help='add git download location')
    argparser.add_argument('--clean', action='store_true',
                           help='delete build and git locations')
    argparser.add_argument('--clean-build', action='store_true',
                           help='delete build location')
    argparser.add_argument(
        '--clean-git', action='store_true', help='delete git location')
    argparser.add_argument(
        '--uninstall', action='store_true', help='uninstall stuff')
    argparser.add_argument('--show-status', action='store_true',
                           help='show current status')
    argparser.add_argument('--no-download', action='store_true',
                           help='skip download, i.e. download already done')
    argparser.add_argument('--no-download-fetch', action='store_true',
                           help='skip download, i.e. download already done, just fetch latest')
    argparser.add_argument('--no-build', action='store_true',
                           help='skip the build steps')
    argparser.add_argument('--reset', action='store_true',
                           help='reset components.json')
    argparser.add_argument('--verbose', action='store_true',
                           help='print debug info')

    args = argparser.parse_args()

    clean_build = False
    clean_git = False
    build_dir = current_path + '/build/'
    install_dir = current_path + '/install/'
    git_dir = current_path + '/git/'
    uninstall = False
    show_status = False
    verbose = False
    download = True
    build = True
    update = False
    reset = False

    if args.clean == True:
        clean_build = True
        clean_git = True
        reset = True

    if args.clean_git == True:
        clean_git = True

    if args.clean_build == True:
        clean_build = True

    if args.uninstall == True:
        uninstall = True

    if args.build_dir != None:
        build_dir = args.build_dir

    if args.git_dir != None:
        git_dir = args.git_dir

    if args.install_dir != None:
        install_dir = args.install_dir

    if args.verbose == True:
        verbose = True

    if args.no_download == True:
        download = False

    if args.no_download_fetch == True:
        download = False
        update = True

    if args.no_build == True:
        build = False

    if args.reset == True:
        reset = True

    if verbose:
        print('Build Dir: ', build_dir)
        print('Git Dir: ', git_dir)
        print('Install Dir: ', install_dir)
        print('Clean Build: ', clean_build)
        print('Clean Git: ', clean_git)
        print('Uninstall: ', uninstall)
        print('Download sources: ', download)
        print('Build sources: ', build)
        print('Reset: ', reset)

    if reset:
        helpers.delete_file(component_file)
        c_str = helpers.read_from_file(component_file_og)
        helpers.write_to_file(c_str, component_file)

    if download:
        c_str = helpers.read_from_file(component_file_og)
        helpers.write_to_file(c_str, component_file)
        clone_repo(git_dir)
    elif update:
        update_repos()

    if build:
        build_hip(build_dir, install_dir, verbose)
