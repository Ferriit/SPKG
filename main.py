#!/usr/bin/env python3

# TODO: Add install option for chocolatey and mmake spkg reload also load the installed packages


import subprocess as sub
import json
import os
import sys
import time

def findmanagers():
    commands = {
        "apt": "apt -version",
        "dnf": "dnf --version",
        "pacman": "pacman --version",
        "flatpak": "flatpak --version",
        "snap": "snap version",
        "homebrew": "brew --version",
        "winget": "winget --version",
        "chocolatey": "choco --version",
        "scoop": "scoop --version",
        "npm": "npm --version",
        "pip": "pip --version",
        "gem": "gem --version",
        "conda": "conda --version",
        "cargo": "cargo --version",
        "yarn": "yarn --version",
        "composer": "composer --version",
        "brewcask": "brew cask --version",
        "maven": "mvn --version",
        "spack": "spack --version",
        "guix": "guix --version",
        "slackpkg": "slackpkg --version",
        "zypper": "zypper --version",
        "portage": "emerge --version"
    }

    packagemanagers = list(commands.keys())

    packages = {}

    for i in packagemanagers:
        print(f"\033[0mChecking for \033[34;1m{i[0].upper() + i[1:].lower()}")
        packages[i] = sub.run([commands[i]], shell=True, capture_output=True, text=True).stdout != ""

    installed = []

    for i in packagemanagers:
        if packages[i]:
            installed.append(i)
    
    print(f"\033[22mFound \033[1m{len(installed)} package managers\033[22m (searched through \033[1m{len(packagemanagers)} package managers\033[22m)\033[0m")

    if not packages["flatpak"]:
        if {"y": True, "n": False}[input("Flatpak was not found. Do you want to install it? (y/n) :  ")[0].lower()]:
            installpackage("flatpak")


    if os.name == "posix":
        open(f"/home/{os.getlogin()}/spkg/managers.json", "w").write(json.dumps({"packages": packages, "installed": installed}, indent=True))
    elif os.name == "nt":
        open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "w").write(json.dumps({"packages": packages, "installed": installed}, indent=True))
    
    return [packages, installed]


def searchpackage(package):
    commands = {
        "apt": "apt search ",
        "dnf": "dnf search ",
        "pacman": "pacman -Ss ",
        "flatpak": "flatpak search ",
        "snap": "snap find ",
        "homebrew": "brew search ",
        "winget": "winget search ",
        "chocolatey": "choco search ",
        "scoop": "scoop search ",
        "npm": "npm search ",
        "pip": "pip search ",
        "gem": "gem search ",
        "conda": "conda search ",
        "cargo": "cargo search ",
        "yarn": "yarn search ",
        "composer": "composer search ",
        "brewcask": "brew cask search ",
        "maven": "mvn dependency:search -DartifactId=",
        "spack": "spack search ",
        "guix": "guix search ",
        "slackpkg": "slackpkg search ",
        "zypper": "zypper search ",
        "portage": "emerge --search "
    }

    if os.name == "posix":
        packagemanagers = json.loads(open(f"/home/{os.getlogin()}/spkg/managers.json", "r").read())
    elif os.name == "nt":
        packagemanagers = json.loads(open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "r").read())

    results = []

    for i in packagemanagers["installed"]:
        print(f"Checking \033[34;1m{i[0].upper() + i[1:].lower()}\033[0m: ", end="", flush=True)
        firstresult = sub.run([commands[i] + package], shell=True, capture_output=True, text=True).stdout
        result = package in firstresult and "not found" not in firstresult.lower()
        print({True: "\033[32;1mFound\033[0m", False: "\033[31;1mNot Found\033[0m"}[result])
        
        if result:
            results.append(i)

    return results


def installpackage(package):
    if os.name == "posix":
        installedpackages = json.loads(open(f"/home/{os.getlogin()}/spkg/installed.json", "r").read())
    elif os.name == "nt":
        installedpackages = json.loads(open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "r").read())

    if package in list(installedpackages.keys()):
        installedwith = installedpackages[package]
        print(f"\033[33;1mWarning:\033[0m Package {package} already installed with \033[34;1m{installedwith[0].upper() + installedwith[1:].lower()}\033[0m")
        sys.exit()

    available = searchpackage(package)

    commands = {
        "apt": "sudo apt install ",
        "dnf": "sudo dnf install ",
        "pacman": "sudo pacman -S ",
        "flatpak": "flatpak install ",
        "snap": "sudo snap install ",
        "homebrew": "brew install ",
        "winget": "winget install ",
        "chocolatey": "choco install ",
        "scoop": "scoop install ",
        "npm": "npm install -g ",
        "pip": "pip install ",
        "gem": "gem install ",
        "conda": "conda install ",
        "cargo": "cargo install ",
        "yarn": "yarn global add ",
        "composer": "composer require ",
        "brewcask": "brew install --cask ",
        "maven": "mvn install:install-file -Dfile=",
        "spack": "spack install ",
        "guix": "guix package -i ",
        "slackpkg": "slackpkg install ",
        "zypper": "sudo zypper install ",
        "portage": "sudo emerge "
    }

    print(f"Please choose a package manager to install \"{package}\" with")

    out = ""
    for i in range(len(available)):
        out += str(i + 1) + ": " + available[i][0].upper() + available[i][1:].lower() + ", "

    confirm = True

    while confirm:
        choice = int(input(out[:-2] + " (0 to abort) :  ")) - 1

        if choice == -1:
            sys.exit()

        confirm = {"n": True, "y": False}[input(f"Are you sure you want to use {available[choice][0].upper() + available[choice][1:].lower()}? (y/n) :  ")[0].lower()]


    os.system(commands[available[choice]] + package)

    if os.name == "posix":
        try:
            installedpackages = json.loads(open(f"/home/{os.getlogin()}/spkg/installed.json", "r").read())
        except FileNotFoundError:
            open(f"/home/{os.getlogin()}/spkg/installed.json", "w").write("{}")
            installedpackages = json.loads(open(f"/home/{os.getlogin()}/spkg/installed.json", "r").read())
    elif os.name == "nt":
        try:
            installedpackages = json.loads(open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "r").read())
        except FileNotFoundError:
            open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "w").write("{}")
            installedpackages = json.loads(open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "r").read())

    installedpackages[package] = available[choice]

    if os.name == "posix":
        open(f"/home/{os.getlogin()}/spkg/installed.json", "w").write(json.dumps(installedpackages, indent=True))
    elif os.name == "nt":
        open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "w").write(json.dumps(installedpackages, indent=True))

def removepackage(package):
    commands = {
        "apt": "apt remove -y ",
        "dnf": "dnf remove -y ",
        "pacman": "pacman -Rns ",
        "flatpak": "flatpak uninstall -y ",
        "snap": "snap remove ",
        "homebrew": "brew uninstall ",
        "winget": "winget uninstall ",
        "chocolatey": "choco uninstall ",
        "scoop": "scoop uninstall ",
        "npm": "npm uninstall -g ",
        "pip": "pip uninstall -y ",
        "gem": "gem uninstall ",
        "conda": "conda remove ",
        "cargo": "cargo uninstall ",
        "yarn": "yarn remove ",
        "composer": "composer remove ",
        "brewcask": "brew uninstall --cask ",
        "maven": "mvn dependency:remove -DartifactId=",  # Maven doesn't have a direct remove command like others
        "spack": "spack uninstall ",
        "guix": "guix package --remove ",
        "slackpkg": "slackpkg remove ",
        "zypper": "zypper remove ",
        "portage": "emerge --unmerge "
    }

    if os.name == "posix":
        installedpackages = json.loads(open(f"/home/{os.getlogin()}/spkg/installed.json", "r").read())
    elif os.name == "nt":
        installedpackages = json.loads(open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "r").read())

    try:
        packagemanager = installedpackages[package]
    except KeyError:
        print(f"\033[31;1mError: \033[0mPackage \"{package}\" not installed")
        sys.exit()

    del installedpackages[package]

    if os.name == "posix":
        open(f"/home/{os.getlogin()}/spkg/installed.json", "w").write(json.dumps(installedpackages, indent=True))
    elif os.name == "nt":
        open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "w").write(json.dumps(installedpackages, indent=True))
    
    os.system(commands[packagemanager] + package)


def flagstopackage(flags: list[str]):
    packageflags = {
        "-all": "all",
        "-installed": "installed",
        "-apt": "apt",
        "-dnf": "dnf",
        "-pac": "pacman",
        "-flat": "flatpak",
        "-snap": "snap",
        "-brew": "homebrew",
        "-win": "winget",
        "-choco": "chocolatey",
        "-scoop": "scoop",
        "-npm": "npm",
        "-pip": "pip",
        "-gem": "gem",
        "-conda": "conda",
        "-cargo": "cargo",
        "-yarn": "yarn",
        "-comp": "composer",
        "-brewcask": "brewcask",
        "-mvn": "maven",
        "-spack": "spack",
        "-guix": "guix",
        "-slack": "slackpkg",
        "-zypper": "zypper",
        "-portage": "portage"
    }

    All = list(packageflags.values())[2:]

    result = []

    for i in flags:
        result.append(packageflags[i])
        if i == "-installed":
            if os.name == "posix":
                packagemanagers = json.loads(open(f"/home/{os.getlogin()}/spkg/managers.json", "r").read())
            elif os.name == "nt":
                packagemanagers = json.loads(open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "r").read())

            result = packagemanagers["installed"]
            break

        if i == "-all":
            result = All
            break

    return result
    

def update(packagemanagerflags: list[str]):
    commands = {
        "apt": "sudo apt update && sudo apt upgrade -y",  # Update command for APT
        "dnf": "sudo dnf update -y",                     # Update command for DNF
        "pacman": "sudo pacman -Syu",                     # Update command for Pacman
        "flatpak": "flatpak update -y",                   # Update command for Flatpak
        "snap": "sudo snap refresh",                      # Update command for Snap
        "homebrew": "brew update && brew upgrade",        # Update command for Homebrew
        "winget": "winget upgrade --all",                 # Update command for Winget
        "chocolatey": "choco upgrade all -y",             # Update command for Chocolatey
        "scoop": "scoop update * && scoop upgrade *",     # Update command for Scoop
        "npm": "npm update -g",                           # Update command for NPM
        "pip": "pip install --upgrade <package-name>",    # Update command for Pip
        "gem": "gem update",                              # Update command for Gem
        "conda": "conda update --all",                    # Update command for Conda
        "cargo": "cargo update",                          # Update command for Cargo
        "yarn": "yarn upgrade",                           # Update command for Yarn
        "composer": "composer update",                    # Update command for Composer
        "brewcask": "brew update && brew upgrade --cask",  # Update command for Brew Cask
        "maven": "mvn versions:use-latest-versions",       # Maven update equivalent (updating dependencies to the latest version)
        "spack": "spack update",                          # Update command for Spack
        "guix": "guix package --upgrade",                 # Update command for Guix
        "slackpkg": "slackpkg update && slackpkg upgrade",# Update command for Slackpkg
        "zypper": "sudo zypper refresh && sudo zypper update -y", # Update command for Zypper
        "portage": "sudo emerge --sync && sudo emerge --update --deep --newuse @world"  # Update command for Portage
    }

    toupdate = flagstopackage(packagemanagerflags)

    out = "Updating "
    for i in toupdate:
        out += f"\033[34;1m{i}\033[0m, "

    print(out[:-2])    

    for i in toupdate:
        os.system(commands[i])


def show(package):
    if os.name == "posix":
        installedpackages = json.loads(open(f"/home/{os.getlogin()}/spkg/installed.json", "r").read())
    elif os.name == "nt":
        installedpackages = json.loads(open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "r").read())

    commands = {
        "apt": "apt show ",
        "dnf": "dnf info ",
        "pacman": "pacman -Qi ",
        "flatpak": "flatpak info ",
        "snap": "snap info ",
        "homebrew": "brew info ",
        "winget": "winget show ",
        "chocolatey": "choco info ",
        "scoop": "scoop info ",
        "npm": "npm show ",
        "pip": "pip show ",
        "gem": "gem info ",
        "conda": "conda list | grep ",
        "cargo": "cargo search ",
        "yarn": "yarn info ",
        "composer": "composer show ",
        "brewcask": "brew info --cask ",
        "maven": "mvn dependency:resolve -DartifactId=",  # Closest to showing Maven artifact info
        "spack": "spack info ",
        "guix": "guix show ",
        "slackpkg": "slackpkg info ",  # Not a direct command, assumes custom alias or script
        "zypper": "zypper info ",
        "portage": "equery meta ",  # 'equery' is part of gentoolkit for querying package metadata
    }
    
    if package in list(installedpackages.keys()):
        manager = installedpackages[package]
        print(f"\033[0mShowing from \033[34;1m{manager[0].upper() + manager[1:].lower()}\033[0m")
        time.sleep(0.1)
        os.system(commands[manager] + package)

    else:
        print(f"\033[31;1mError:\033[0m Package {package} not found")


def detach(packages: list[str]):
    if os.name == "posix":
        installedpackages = json.loads(open(f"/home/{os.getlogin()}/spkg/installed.json", "r").read())
    elif os.name == "nt":
        installedpackages = json.loads(open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "r").read())

    out = ""
    for i in packages:
        out += "\033[33;1m" + i + "\033[0m, "

    choice = {"y": True, "n": False}[input(f"Are you sure you want to \033[31mdetach\033[0m {out[:-2]}? (y/n) :  ")[0].lower()]

    try:
        if choice:
            for package in packages:
                del installedpackages[package]
                print(f"Successfully detached \033[34;1m\"{package}\"\033[0m")
        else:
            sys.exit()
    except KeyError:
        print(f"\033[31;1mError:\033[0m Package \"{package}\" was not found")
        sys.exit()

    if os.name == "posix":
        open(f"/home/{os.getlogin()}/spkg/installed.json", "w").write(json.dumps(installedpackages, indent=True))
    elif os.name == "nt":
        open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "w").write(json.dumps(installedpackages, indent=True))


def attach(packages: list[str], manager: str):
    if os.name == "posix":
        installedpackages = json.loads(open(f"/home/{os.getlogin()}/spkg/installed.json", "r").read())
    elif os.name == "nt":
        installedpackages = json.loads(open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "r").read())

    for i in packages:
        installedpackages[i] = flagstopackage([manager])[0]

    if os.name == "posix":
        open(f"/home/{os.getlogin()}/spkg/installed.json", "w").write(json.dumps(installedpackages, indent=True))
    elif os.name == "nt":
        open(f"C:\\users\\{os.getlogin()}\\spkg\\managers.json", "w").write(json.dumps(installedpackages, indent=True))


    out = ""
    for i in packages:
        out += "\033[34;1m" + i + "\033[0m, "


    print(f"Successfully attached \"{out[:-2]}\"")


if __name__ == "__main__":
    #findmanagers()
    #removepackage("golang")

    global version
    version = "0.1.0"
    try:
        args = sys.argv[1:]

        if args[0] == "install":
            args = args[1:]
            for i in args:
                installpackage(i)
        
        elif args[0] == "uninstall":
            args = args[1:]
            for i in args:
                removepackage(i)
        
        elif args[0] == "search":
            args = args[1:]
            for i in args:   
                searchpackage(i)
    
        elif args[0] == "reload":
            findmanagers()

        elif args[0] == "version":
            print(f"\033[34;1mSPKG\033[0m version {version}")

        elif args[0] == "update":
            update(args[1:])

        elif args[0] == "show":
            args = args[1:]
            for i in args:
                show(i)

        elif args[0] == "detach":
            detach(args[1:])

        elif args[0] == "attach":
            attach(args[1:-1], args[-1])
 
        elif args[0] == "help":
            print("""SPKG (Searching Package Manager) is a tool to help you manage your package managers. It offers regular commands, such as:

install: Installs a package. Requires sudo privileges and a package name:
    > sudo spkg install <package>

    When executed, install will look through all your package managers to try to find a match and then ask you which one to install.


uninstall: Uninstalls a package. Requires sudo privileges and package name:
    > sudo spkg uninstall <package>

    When executed, uninstall will delete the package with the correct package manager for you


search: Searches through all package managers to find a match for you
    > spkg search <package>


reload: Updates the list of known package managers. Required sudo privileges and has to be run on install of SPKG or any other package managers.
    > sudo spkg reload


version: Prints the version of SPKG you're using.
    > spkg version


update: Updates the packages you specify with flags. Requires sudo privileges.
    > sudo spkg update <flags>

    Flags:
        -all: Updates all possible packages
        -installed: Updates all installed packages
        -apt: Updates APT
        -dnf: Updates DNF
        -pac: Updates Pacman
        -flat: Updates Flatpak
        -snap: Updates Snap
        -brew: Updates Homebrew
        -win: Updates Winget
        -choco: Updates Chocolatey
        -scoop: Updates Scoop
        -npm: Updates NPM
        -pip: Updates PyPI (PIP)
        -gem: Updates gem
        -conda: Updates Conda
        -cargo: Updates Cargo
        -yarn: Updates Yarn
        -comp: Updates Composer
        -brewcask: Updates Brew cask
        -mvn: Updates Maven
        -spack: Updates Spack
        -guix: Updates GUIX
        -slack: Updates SlackPkg
        -zypper: Updates Zypper
        -portage: Updates Portage


show: Shows an installed package with the correct Package Manager.
    > spkg show <package>


detach: Makes SPKG forget a package (it gets removed from the installed.json file, meaning that SPKG won't hinder you from installing stuff). Requires sudo privileges. Can take multiple packages.
    > sudo spkg detach <package>


attack: Attached a package to the installed.json file to show SPKG that it's installed. Requires sudo privileges. Can take multiple packages.
    > sudo spkg attach <package> <package-manager>


help: Prints a help message.
            """)
    except IndexError:
        print("\033[31;1mError: \033[0mNot enough arguments given")
