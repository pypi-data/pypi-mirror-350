# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os

def get_entry(name):
    current = os.getcwd()
    user_root = os.path.expanduser("~")
    cpkg_root = os.path.join(user_root, ".conduitpkg")
    os.chdir(cpkg_root)
    with open("entries.json", "r") as f:
        entries = json.load(f)
    os.chdir(current)
    if name not in entries:
        print("[!] Entry doesn't exist [!]")
        return
    return entries[name]

def local_get_entry(name):
    current = os.getcwd()
    cpkg_root = ".conduitpkg"
    os.chdir(cpkg_root)
    with open("entries.json", "r") as f:
        entries = json.load(f)
    os.chdir(current)
    if name not in entries:
        print("[!] Entry doesn't exist [!]")
        return
    return entries[name]

def export_entry(name, entry):
    current = os.getcwd()
    cpkg_root = ".conduitpkg"
    os.chdir(cpkg_root)
    with open("entries.json", "r") as f:
        entries = json.load(f)
        entries[name] = entry
    with open("entries.json", "w") as f:
        json.dump(entries, f)
    os.chdir(current)

def local_export_entry(name, entry):
    current = os.getcwd()
    cpkg_root = ".conduitpkg"
    os.chdir(cpkg_root)
    with open("entries.json", "r") as f:
        entries = json.load(f)
        entries[name] = entry
    with open("entries.json", "w") as f:
        json.dump(entries, f)
    os.chdir(current)