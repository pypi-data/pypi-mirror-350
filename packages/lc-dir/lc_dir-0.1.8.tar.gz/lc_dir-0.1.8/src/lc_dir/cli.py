#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import shutil
import textwrap
from argparse import RawDescriptionHelpFormatter

# ANSI color codes
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

REQUIRED_CMDS = ["lc-set-rule", "lc-sel-files", "lc-context"]
LLM_CONTEXT_URL = "https://github.com/cyberchitta/llm-context.py"

def ensure_llm_context_installed():
    missing = [cmd for cmd in REQUIRED_CMDS if shutil.which(cmd) is None]
    if missing:
        for cmd in missing:
            print(f"Error: '{cmd}' not found")
        print("Please install llm-context CLI first:")
        print("  pipx install llm-context")
        print(f"See {LLM_CONTEXT_URL} for more.")
        sys.exit(1)

def find_git_root(path):
    orig = os.path.abspath(path)
    while True:
        if os.path.isfile(os.path.join(path, ".gitignore")):
            return os.path.abspath(path)
        parent = os.path.dirname(path)
        if parent == path:
            print(f"Error: Could not find .gitignore in any parent directory of {orig}")
            sys.exit(1)
        path = parent

def find_folder(root, query):
    candidate = os.path.abspath(os.path.join(root, query))
    if os.path.isdir(candidate):
        return os.path.relpath(candidate, root)

    matches = []
    for dirpath, dirnames, _ in os.walk(root):
        for d in dirnames:
            if d.lower() == query.lower():
                matches.append(os.path.relpath(os.path.join(dirpath, d), root))

    if not matches:
        print(f"Error: Folder '{query}' not found in project.")
        sys.exit(1)

    if len(matches) > 1:
        print(f"Multiple matches found for '{query}':")
        for idx, m in enumerate(matches):
            print(f"  {idx}: {m}")
        idx = input("Choose index> ")
        try:
            return matches[int(idx)]
        except:
            print("Invalid selection.")
            sys.exit(1)

    return matches[0]

def write_temp_rule(root, rel_folders, rule_name="temp-folder-rule"):
    """
    Create a single temporary rule including all rel_folders.
    Accepts a string or a list of strings.
    """
    # normalize to list
    if isinstance(rel_folders, str):
        rel_folders = [rel_folders]

    # prepare patterns for each folder (empty string => all files)
    patterns = []
    for rel in rel_folders:
        r = rel.replace("\\", "/").strip("./")
        pat = f"{r}/**/*" if r else "**/*"
        patterns.append(pat)

    rules_dir = os.path.join(root, ".llm-context", "rules")
    os.makedirs(rules_dir, exist_ok=True)
    rule_path = os.path.join(rules_dir, f"{rule_name}.md")

    lines = [
        "---",
        "base: lc-gitignores",
        "description: Default rule for software projects, using lc-gitignores base rule",
        "---",
        f'description: "Temp rule for {", ".join(rel_folders) or "."}"',
        "only-include:",
        "  full_files:"
    ]
    for pat in patterns:
        lines.append(f'    - "{pat}"')
    lines.append("---")
    content = "\n".join(lines) + "\n"

    with open(rule_path, "w", encoding="utf-8") as f:
        f.write(content)

    return rule_name

def run_llm_context_commands(root, rule_name):
    for cmd in [["lc-set-rule", rule_name], ["lc-sel-files"], ["lc-context"]]:
        print(f"{CYAN}>>{RESET}", " ".join(cmd))
        subprocess.run(cmd, cwd=root, check=True)

def main():
    ensure_llm_context_installed()

    parser = argparse.ArgumentParser(
        description="Copy all non-git-ignored files from one or more directories into your llm-context buffer.",
        epilog=textwrap.dedent("""\
            Examples:
              # copy everything under the current folder:
              $ lc-dir

              # copy a specific subfolder:
              $ lc-dir path/to/service

              # search for folders by name anywhere in your repo:
              $ lc-dir common api models
        """),
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="(optional) one or more folders (paths or names) to include"
    )
    args = parser.parse_args()

    cwd = os.getcwd()
    root = find_git_root(cwd)

    if not args.targets:
        rel = os.path.relpath(cwd, root)
        rel = "" if rel == "." else rel
        rel_folders = [rel]
    else:
        rel_folders = []
        for t in args.targets:
            found = find_folder(root, t)
            print(f"{GREEN}Found:{RESET} '{t}' → {found}")
            rel_folders.append(found)

    rule_name = write_temp_rule(root, rel_folders)
    run_llm_context_commands(root, rule_name)

if __name__ == "__main__":
    main()
