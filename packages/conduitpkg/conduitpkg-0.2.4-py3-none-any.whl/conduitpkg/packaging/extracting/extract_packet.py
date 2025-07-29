# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import shutil
import pathlib
from zynk_lite import interpreter
from ...install import entries
import json

def extract(name):
    current = os.getcwd()
    user_root = os.path.expanduser("~")
    packet_path = os.path.join(user_root, ".conduitpkg", name)
    shutil.unpack_archive(name+".zip", packet_path)
    os.chdir(packet_path)
    intp = interpreter.ZynkLInterpreter()
    intp.eval_file("builder.zl")
    entry_mng()
    os.chdir(current)
    os.remove(name+".zip")

def gextract(name):
    current = os.getcwd()
    user_root = os.path.expanduser("~")
    packet_path = os.path.join(user_root, ".conduitpkg", name)
    shutil.copytree(name, packet_path)
    os.chdir(packet_path)
    intp = interpreter.ZynkLInterpreter()
    intp.eval_file("builder.zl")
    entry_mng()
    os.chdir(current)
    shutil.rmtree(name)

def local_extract(name):
    current = os.getcwd()
    packet_path = os.path.join(".conduitpkg", name)
    shutil.unpack_archive(name+".zip", packet_path)
    os.chdir(packet_path)
    intp = interpreter.ZynkLInterpreter()
    intp.eval_file("builder.zl")
    local_entry_mng()
    os.chdir(current)
    os.remove(name+".zip")

def local_gextract(name):
    current = os.getcwd()
    packet_path = os.path.join(".conduitpkg", name)
    shutil.copytree(name, packet_path)
    os.chdir(packet_path)
    intp = interpreter.ZynkLInterpreter()
    intp.eval_file("builder.zl")
    local_entry_mng()
    os.chdir(current)
    shutil.rmtree(name)


# esto evitara un poco de dupliación de código

def entry_mng():
    with open("package.json", "r") as f:
        package_file = json.load(f)
    for name, entry in package_file["entries"].items():
        entries.export_entry(name, entry)

def local_entry_mng():
    with open("package.json", "r") as f:
        package_file = json.load(f)
    os.chdir("..")
    os.chdir("..")
    for name, entry in package_file["entries"].items():
        entries.local_export_entry(name, entry)