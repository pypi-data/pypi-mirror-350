# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os
from urllib.request import urlopen
import pathlib

def get_repos():
    user_root = os.path.expanduser("~")
    repos_lists_path = os.path.join(user_root, ".conduitpkg", "list.json")
    with open(repos_lists_path, "r") as f:
        repos_lists = json.load(f)
    return repos_lists

def get_local_repos():
    repos_lists_path = os.path.join(".conduitpkg", "list.json")
    with open(repos_lists_path, "r") as f:
        repos_lists = json.load(f)
    return repos_lists

def is_in_repo(repo_url, name):
    data = get_pkg_list(repo_url)
    if name in data.keys():
        return True
    return False

def get_pkg_list(repo_url):
    with urlopen(repo_url) as request:
        response = request.read().decode("utf-8")
    data = json.loads(response)
    return data