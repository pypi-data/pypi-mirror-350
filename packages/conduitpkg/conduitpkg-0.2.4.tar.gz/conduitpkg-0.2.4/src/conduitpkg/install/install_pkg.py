# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from git import Repo
import os
import json
from . import search_packet as search
from . import dependencies
from urllib.request import urlopen, urlretrieve
from ..packaging.extracting import extract
import shutil

def get_packet(name, protocol):
    current = os.getcwd()
    print("[+] Searching Packet [+]")
    print("[+] Listing Repos [+]")
    repos_list = search.get_repos()
    where = []
    print("[+] Searching on repos [+]")
    for repo in repos_list:
        print(f"[+] Searching on Repo {repo} the packet {name} [+]")
        if search.is_in_repo(repo, name):
            where.append(repo)
            print(f"[+] Package {name} is in {repo} [+]")
    if len(where) < 1:
        print("[!] Packet doesn't exist [!]")
    elif len(where) > 1:
        print("[!] Warning: this is i various repos [!]")
        for rep in where:
            print(f"Repo: {rep} ")
            opt=input(f"Is {name} pkg from this repo? (y/n) >>> ")
            if opt=="y":
                repo=rep
                break
            elif opt=="n":
                pass
    else:
        repo = where[0]
    pkg_list = search.get_pkg_list(repo)
    pkg_url = pkg_list[name]
    # tengo que hacer la parte de descarga del paquete
    # primero averiguar donde esta el paquete, y despues descargarlo
    if protocol == "git":
        print("[+] Cloning [+]")
        os.mkdir(name)
        Repo.clone_from(pkg_url, name)
        extract.gextract(name)
        print(f"[+] Packet '{name}' Installed [+]")
    elif protocol=="http":
        urlretrieve(pkg_url, name+".zip")
        extract.extract(name)
    if name in os.listdir("."):
        shutil.rmtree(name)
    user_root = os.path.join(os.path.expanduser("~"), ".conduitpkg")
    os.chdir(user_root)
    with open("installed.json", "r+") as f:
        installed_list = json.load(f)
        installed_list.append(name)
        json.dump(installed_list, f)
    os.chdir(current)




def local_get_packet(name, protocol):
    current=os.getcwd()
    print("[+] Searching Packet [+]")
    print("[+] Listing Repos [+]")
    repos_list = search.get_local_repos()
    where = []
    print("[+] Searching on repos [+]")
    for repo in repos_list:
        print(f"[+] Searching on Repo {repo} the packet {name} [+]")
        if search.is_in_repo(repo, name):
            where.append(repo)
            print(f"[+] Package {name} is in {repo} [+]")
    if len(where) < 1:
        print("[!] Packet doesn't exist [!]")
    elif len(where) > 1:
        print("[!] Warning: this is i various repos [!]")
        for rep in where:
            print(f"Repo: {rep} ")
            opt=input(f"Is {name} pkg from this repo? (y/n) >>> ")
            if opt=="y":
                repo=rep
                break
            elif opt=="n":
                pass
    else:
        repo = where[0]
    pkg_list = search.get_pkg_list(repo)
    pkg_url = pkg_list[name]
    # tengo que hacer la parte de descarga del paquete
    # primero averiguar donde esta el paquete, y despues descargarlo
    if protocol == "git":
        print("[+] Cloning [+]")
        os.mkdir(name)
        Repo.clone_from(pkg_url, name)
        extract.local_gextract(name)
        print(f"[+] Packet '{name}' Installed [+]")
    elif protocol=="http":
        urlretrieve(pkg_url, name+".zip")
        extract.local_extract(name)
    if name in os.listdir("."):
        shutil.rmtree(name)
    user_root = ".conduitpkg"
    os.chdir(user_root)
    with open("installed.json", "r") as f:
        installed_list = json.load(f)
    with open("installed.json", "w") as f:
        installed_list.append(name)
        json.dump(installed_list, f)
    os.chdir(current)