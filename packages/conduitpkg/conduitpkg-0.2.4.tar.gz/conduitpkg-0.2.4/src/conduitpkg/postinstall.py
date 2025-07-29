# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os

def post_install():
    user_root = os.path.expanduser("~")
    os.chdir(user_root)
    if ".conduitpkg" in os.listdir("."):
        return
    os.mkdir(".conduitpkg")
    os.chdir(".conduitpkg")
    with open("installed.json", "w") as f:
        json.dump([], f)
    with open("entries.json", "w") as f:
        json.dump({}, f)
    with open("list.json", "w") as f:
        json.dump([], f)

def local_post_install():
    if ".conduitpkg" in os.listdir("."):
        return
    os.mkdir(".conduitpkg")
    os.chdir(".conduitpkg")
    with open("installed.json", "w") as f:
        json.dump([], f)
    with open("entries.json", "w") as f:
        json.dump({}, f)
    with open("list.json", "w") as f:
        json.dump([], f)