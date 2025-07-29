# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from . import install_pkg as install
import json
import os

def resolve(name):
    current = os.getcwd()
    user_root = os.path.expanduser("~")
    try:
        pkg_root = os.path.join(user_root, ".conduitpkg", name)
    except Exception:
        print(f"[!] Error, package {name} not installed [!]")
        return
    os.chdir(pkg_root)

    with open("package.json", "r") as f:
        dependencies = json.load(f)["dependencies"]

    for i in dependencies:
        install.get_packet(i, "http")

    os.chdir(current)

def local_resolve(name):
    current = os.getcwd()
    try:
        pkg_root = os.path.join(".conduitpkg", name)
    except Exception:
        print(f"[!] Error, package {name} not installed [!]")
    os.chdir(pkg_root)

    with open("package.json", "r") as f:
        dependencies = json.load(f)["dependencies"]

    for i in dependencies:
        install.local_get_packet(i, "http")

    os.chdir(current)