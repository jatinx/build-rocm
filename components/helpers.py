import json
from git import Repo
import os
import shutil


def open_json_file(file_name):
    f = open(file_name, 'r')
    data = json.load(f)
    f.close()
    return data


def git_checkout(url, rbranch, path):
    repo = Repo.clone_from(url, path, branch=rbranch)
    return repo


def dump_json_to_file(input, file):
    op = json.dumps(input, indent=4)
    f = open(file, 'w')
    f.write(op)
    f.close()


def delete_dir(dir):
    try:
        shutil.rmtree(dir)
    except:
        print('Not deleting dir: ', dir)


def delete_file(file):
    try:
        os.remove(file)
    except:
        print('Cant delete file: ', file)


def create_dir(dir):
    os.makedirs(dir)


def read_from_file(file_name):
    with open(file_name, 'rb') as file:
        data = file.read()
    return data


def write_to_file(str, file_name):
    with open(file_name, 'wb') as file:
        file.write(str)
