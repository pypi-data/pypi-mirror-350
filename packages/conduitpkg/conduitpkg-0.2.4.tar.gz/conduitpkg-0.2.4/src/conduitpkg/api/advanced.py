# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .. import install
from .. import postinstall
from .. import packaging
from .. import builder
import shutil
import json
import os

def install_pkg(name, local=False, protocol="http"):
    if local:
        local_advanced_install(name, protocol)
    elif not local:
        advanced_install(name, protocol)
    else:
        print("[!] Unknown Method [!]")

def run_entry(name, local=False):
    if local:
        local_exec_entry(name)
    elif not local:
        exec_entry(name)
    else:
        print("[!] Unknown Method [!]")

def advanced_install(name, protocol="http"):
    print("[+] Installing Globally [+]")
    install.get_pkg.get_packet(name, protocol)
    print("[+] Resolving Dependencies Globally [+]")
    install.dependencies.resolve(name)

def local_advanced_install(name, protocol="http"):
    print("[+] Installing Locally [+]")
    install.get_pkg.local_get_packet(name, protocol)
    print("[+] Resolving Dependencies Locally [+]")
    install.dependencies.local_resolve(name)

def exec_entry(command):
    print("[+] Running Global Entry [+]")
    current=os.getcwd()
    entry=install.entries.get_entry(command)
    cpkg_root = os.path.join(os.path.expanduser("~"), ".conduitpkg")
    os.chdir(cpkg_root)
    os.system(entry)
    os.chdir(current)

def local_exec_entry(command):
    print("[+] Running Local Entry [+]")
    entry=install.entries.local_get_entry(command)
    cpkg_root = ".conduitpkg"
    os.chdir(cpkg_root)
    os.system(entry)
    os.chdir("..")

def compress(dir):
    print("[+] Compressing [+]")
    os.chdir(dir)
    packaging.comp.compress.compress()
    os.chdir("..")
    if "dist" in os.listdir("."):
        shutil.rmtree("dist")
    shutil.copytree(os.path.join(dir, "dist"), "dist")
    shutil.rmtree(os.path.join(dir, "dist"))

def extract(name, local=False, zipped=True):
    if zipped:
        print("[+] Extracting from zip... [+]")
        if local:
            print("[+] Installing Locally [+]")
            packaging.extr.extract.local_extract(name)
        elif not local:
            print("[+] Installing Globally [+]")
            packaging.extr.extract.extract(name)
        else:
            return
    elif not zipped:
        print("[+] Installing from folder [+]")
        if local:
            print("[+] Installing Locally [+]")
            packaging.extr.extract.local_gextract(name)
        elif not local:
            print("[+] Installing Globally [+]")
            packaging.extr.extract.gextract(name)
        else:
            return
    else:
        print("[!] Unknown Method [!]")
        return
    
def post_install(local=True):
    if local:
        print("[+] Initializing Locally... [+]")
        postinstall.local_post_install()
    elif not local:
        print("[+] Initializing Globally... [+]")
        postinstall.post_install()
    else:
        return
    
def init_pkg(name):
    if name in os.listdir("."):
        print("[!] Packet Already Exists [!]")
        return
    builder.new_packet(name)

def add_repo(name, local=False):
    if local:
        print("[+] Adding Repo Locally [+]")
        os.chdir(".conduitpkg")
        with open("list.json", "r") as f:
            actual = json.load(f)
            if name not in actual:
                actual.append(name)
        with open("list.json", "w") as f:
                json.dump(actual, f)
        os.chdir("..")
    elif not local:
        print("[+] Adding Repo Globally [+]")
        current = os.getcwd()
        os.chdir(os.path.join(os.path.expanduser("~"), ".conduitpkg"))
        with open("list.json", "r") as f:
            actual = json.load(f)
            if name not in actual:
                actual.append(name)
        with open("list.json", "w") as f:
            json.dump(actual, f)
        os.chdir(current)
    else:
        print("[!] Unknown Env [!]")

def remove_repo(name, local=False):
    if local:
        print("[+] Removing Repo Locally [+]")
        os.chdir(".conduitpkg")
        with open("list.json", "r") as f:
            actual = json.load(f)
            if name in actual:
                actual.remove(name)
        with open("list.json", "w") as f:
            json.dump(actual, f)
        os.chdir("..")
    elif not local:
        print("[+] Removing Repo Globally [+]")
        current = os.getcwd()
        os.chdir(os.path.join(os.path.expanduser("~"), ".conduitpkg"))
        with open("list.json", "r") as f:
            actual = json.load(f)
            if name in actual:
                actual.remove(name)
        with open("list.json", "w") as f:
            json.dump(actual, f)
        os.chdir(current)
    else:
        print("[!] Unknown Env [!]")

def get_repos(local=False):
    if local:
        print("[+] Listing Local Repos [+]")
        os.chdir(".conduitpkg")
        with open("list.json", "r") as f:
            actual = json.load(f)
        os.chdir("..")
        return actual
    elif not local:
        print("[+] Listing Global Repos [+]")
        current = os.getcwd()
        os.chdir(os.path.join(os.path.expanduser("~"), ".conduitpkg"))
        with open("list.json", "r") as f:
            actual = json.load(f)
        os.chdir(current)
        return actual
    else:
        print("[!] Unknown Env [!]")

def uninstall_pkg(name, local=False):
    current = os.getcwd()
    if local:
        print("[+] Uninstalling at Local [+]")
        os.chdir(".conduitpkg")
    elif not local:
        print("[+] Uninstalling at Global [+]")
        os.chdir(os.path.join(os.path.expanduser("~"), ".conduitpkg"))
    else:
        print("[!] Unknown Env [!]")
        return
    print("[+] Removing from installed.json [+]")
    with open("installed.json", "r") as f:
        installed_pkgs = json.load(f)
    print("[ --- INSTALLED PKG'S --- ]")
    for i, pkg in enumerate(installed_pkgs):
        print(f" {i+1}/{len(installed_pkgs)} : {pkg}")
    installed_pkgs.pop(installed_pkgs.index(name))
    with open("installed.json", "w") as f:
        json.dump(installed_pkgs, f)
    print("[+] Reading Packet Entries [+]")
    with open(os.path.join(name, "package.json"), "r") as f:
        entries = json.load(f)["entries"]
    with open("entries.json", "r") as f:
        fentries = json.load(f)
    print("[+] Removing Entries [+]")
    for k in entries.keys():
        if k in fentries.keys():
            del fentries[k]
    with open("entries.json", "w") as f:
        json.dump(fentries, f)
    print("[+] Returning to Working Directory [+]")
    os.chdir(current)

def print_pkg_info(pkg, local=False):
    current = os.getcwd()
    if local:
        print("[+] Searching Package at Local   [+]")
        pkg_root = os.path.join(".conduitpkg", pkg)
    elif not local:
        print("[+] Searching Package at Global  [+]")
        pkg_root = os.path.join(os.path.expanduser("~"), ".conduitpkg", pkg)
    else:
        print("[!] Unknown Env [!]")
        return
    os.chdir(pkg_root)
    with open("package.json") as f:
        pkg_info = json.load(f)
    os.chdir(current)
    print("[+] ------------ BEGIN OF INFORMATION -------------- [+]")
    print(f"[+] Package {pkg} Information                        [+]")
    print(f"[+] Version : {pkg_info.version}                     [+]")
    print(f"[+] Author : {pkg_info.author}                       [+]")
    print(f"[+] Author Email : {pkg_info.author_email}           [+]")
    print(f"[+] Maintainer Email : {pkg_info.mantainer_email}    [+]")
    print(f"[+] License : {pkg_info.license}                     [+]")
    print(f"[+] Dependencies : {pkg_info.dependencies}           [+]")
    print(f"[+] Entries : {pkg_info.entries}                     [+]")
    print("[-] ------------ END OF INFORMATION ---------------- [+]")

