# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import shutil
import os
import json

def compress():
    current = os.getcwd()
    try:
        with open("package.json", "r") as f:
            name = json.load(f)["name"]
    except Exception:
        print("[!] Not in a package directory [!]")
    try:
        os.mkdir("dist")
    except Exception:
        pass
    os.chdir("dist")
    dist_path = os.path.join("dist", name)
    if name in os.listdir("."):
        shutil.rmtree(name)
    os.mkdir(name)
    os.chdir("..")
    shutil.copy("package.json", os.path.join(dist_path, "package.json"))
    shutil.copytree("src", os.path.join(dist_path, "src"))
    shutil.copy("builder.zl", os.path.join(dist_path, "builder.zl"))
    shutil.copy("LICENSE.txt", os.path.join(dist_path, "LICENSE.txt"))
    shutil.copy("README.md", os.path.join(dist_path, "README.md"))
    shutil.make_archive(dist_path, "zip", dist_path)
    os.chdir(current)
