# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from ..api import advanced

def main():
    if sys.argv[1]=="run":
        if "--local" in sys.argv:
            advanced.run_entry(sys.argv[2], True)
        else:
            advanced.run_entry(sys.argv[2])
    elif sys.argv[1]=="get":
        if sys.argv[2]=="repos":
            if "--local" in sys.argv:
                repos=advanced.get_repos(True)
            else:
                repos=advanced.get_repos()
            for repo in repos:
                print(f"[+] Repo: {repo} [+]")
        elif sys.argv[2]=="pkg":
            if "--local" in sys.argv:
                advanced.install_pkg(sys.argv[3], True)
            else:
                advanced.install_pkg(sys.argv[3])
    elif sys.argv[1]=="post_install":
        if not "--local" in sys.argv:
            advanced.post_install(False)
        else:
            advanced.post_install()
    elif sys.argv[1]=="init":
        advanced.init_pkg(sys.argv[2])
    elif sys.argv[1]=="repo":
        if sys.argv[2]=="add":
            if "--local" in sys.argv:
                advanced.add_repo(sys.argv[3], True)
            else:
                advanced.add_repo(sys.argv[3])
        elif sys.argv[2]=="remove":
            if "--local" in sys.argv:
                advanced.remove_repo(sys.argv[3], True)
            else:
                advanced.remove_repo(sys.argv[3])
    elif sys.argv[1]=="compress":
        advanced.compress(sys.argv[2])
    elif sys.argv[1]=="extract":
        if "--local" in sys.argv:
            advanced.extract(sys.argv[2], True)
        else:
            advanced.extract(sys.argv[2])
    elif sys.argv[1]=="uninstall":
        if "--local" in sys.argv:
            advanced.uninstall_pkg(sys.argv[2], True)
        else:
            advanced.uninstall_pkg(sys.argv[2])
    elif sys.argv[1]=="info":
        if "--local" in sys.argv:
            advanced.print_pkg_info(sys.argv[2], True)
        else:
            advanced.print_pkg_info(sys.argv[2])
    elif sys.argv[1]=="help":
        print("[+] ----- Help Message ----- [+]")
        print("[*] run                      [*]")
        print("[*] get repos                [*]")
        print("[*] get pkg                  [*]")
        print("[*] post_install             [*]")
        print("[*] init                     [*]")
        print("[*] repo add                 [*]")
        print("[*] repo remove              [*]")
        print("[*] compress                 [*]")
        print("[*] extract                  [*]")
        print("[*] uninstall                [*]")
        print("[*] help                     [*]")
        print("[*] info                     [*]")
        print("[+] --- Help Message End --- [+]")
    else:
        print("[!] Command Not Found    [!]")
        print("[*] Try with 'cpkg help' [*]")