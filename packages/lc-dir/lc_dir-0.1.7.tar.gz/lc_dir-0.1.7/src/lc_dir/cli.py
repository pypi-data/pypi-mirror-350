#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import shutil
import textwrap
from argparse import RawDescriptionHelpFormatter
from colorama import init, Fore, Style

# Initialize colorama (for Windows support)
init(autoreset=True)

REQUIRED_CMDS = ["lc-set-rule", "lc-sel-files", "lc-context"]
LLM_CONTEXT_URL = "https://github.com/cyberchitta/llm-context.py"

def ensure_llm_context_installed():
    """Verify that the llm-context CLI is available on PATH."""
    missing = [cmd for cmd in REQUIRED_CMDS if shutil.which(cmd) is None]
    if missing:
        for cmd in missing:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} '{cmd}' not found")
        print(f"{Fore.YELLOW}Please install llm-context CLI first:{Style.RESET_ALL}")
        print("  pipx install llm-context")
        print(f"See {LLM_CONTEXT_URL} for more.")
        sys.exit(1)

def find_git_root(path):
    """Walk upwards until a directory containing .gitignore is found."""
    orig = os.path.abspath(path)
    while True:
        if os.path.isfile(os.path.join(path, ".gitignore")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} Could not find .gitignore above '{orig}'")
            sys.exit(1)
        path = parent

def find_folder(root, query):
    """
    Locate 'query' under 'root'.
    If it's an existing path, returns its relpath.
    Otherwise, searches case-insensitively and reports where it was found.
    """
    # 1) Exact path?
    candidate = os.path.abspath(os.path.join(root, query))
    if os.path.isdir(candidate):
        rel = os.path.relpath(candidate, root)
        print(f"{Fore.GREEN}Found folder '{query}' at: {rel}{Style.RESET_ALL}")
        return rel

    # 2) Search by name
    matches = []
    for dirpath, dirnames, _ in os.walk(root):
        for d in dirnames:
            if d.lower() == query.lower():
                matches.append(os.path.relpath(os.path.join(dirpath, d), root))

    if not matches:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} Folder '{query}' not found in project.")
        sys.exit(1)
    if len(matches) > 1:
        print(f"{Fore.YELLOW}Multiple matches found for '{query}':{Style.RESET_ALL}")
        for idx, match in enumerate(matches):
            print(f"  {idx}: {match}")
        choice = input("Enter index of folder to use: ")
        try:
            sel = int(choice)
            picked = matches[sel]
        except Exception:
            print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
            sys.exit(1)
        print(f"{Fore.GREEN}Using: {picked}{Style.RESET_ALL}")
        return picked

    # single match
    picked = matches[0]
    print(f"{Fore.GREEN}Found folder '{query}' at: {picked}{Style.RESET_ALL}")
    return picked

def write_temp_rule(root, rel_folder, rule_name="temp-folder-rule"):
    """
    Create a temporary llm-context rule to include all files under rel_folder.
    (silent—no output here)
    """
    rules_dir = os.path.join(root, ".llm-context", "rules")
    os.makedirs(rules_dir, exist_ok=True)
    rule_path = os.path.join(rules_dir, f"{rule_name}.md")
    rel = rel_folder.replace("\\", "/").strip("./")
    pattern = f'{rel}/**/*' if rel else '**/*'
    content = f"""---
description: "Temp rule for {rel or '.'}"
only-include:
  full_files:
    - "{pattern}"
---
"""
    with open(rule_path, "w", encoding="utf-8") as f:
        f.write(content)
    return rule_name

def run_llm_context_commands(root, rule_name):
    """Run lc-set-rule, lc-sel-files, lc-context with colored arrows."""
    for cmd in [["lc-set-rule", rule_name], ["lc-sel-files"], ["lc-context"]]:
        arrow = f"{Fore.CYAN}>>{Style.RESET_ALL}"
        print(arrow, " ".join(cmd))
        subprocess.run(cmd, cwd=root, check=True)

def main():
    ensure_llm_context_installed()

    parser = argparse.ArgumentParser(
        description="Copy all non-git-ignored files from a directory (or named folder anywhere) into your llm-context buffer.",
        epilog=textwrap.dedent("""\
            Examples:
              # Copy everything under the current folder:
              $ lc-dir

              # Copy a specific subfolder:
              $ lc-dir path/to/service

              # Search for a folder named "common" anywhere in your repo:
              $ lc-dir common

              # From deep inside a tree, copy "api" wherever it lives:
              $ cd src/app/modules/foo
              $ lc-dir api
        """),
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="(optional) folder to export context from, or name of a folder anywhere in the project",
    )
    args = parser.parse_args()

    cwd = os.getcwd()
    root = find_git_root(cwd)

    if args.target is None:
        rel_folder = os.path.relpath(cwd, root)
        if rel_folder == ".":
            rel_folder = ""
    else:
        rel_folder = find_folder(root, args.target)

    rule_name = write_temp_rule(root, rel_folder)
    run_llm_context_commands(root, rule_name)

if __name__ == "__main__":
    main()
