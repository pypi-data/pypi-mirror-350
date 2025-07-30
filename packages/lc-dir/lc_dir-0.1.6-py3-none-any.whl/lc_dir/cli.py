#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

def find_git_root(path):
    orig = os.path.abspath(path)
    while True:
        if os.path.isfile(os.path.join(path, ".gitignore")):
            return os.path.abspath(path)
        parent = os.path.dirname(path)
        if parent == path:
            print("Error: Could not find .gitignore in any parent directory of", orig)
            sys.exit(1)
        path = parent

def find_folder(root, query):
    # If the query is an existing path, use it
    candidate = os.path.abspath(os.path.join(root, query))
    if os.path.isdir(candidate):
        return os.path.relpath(candidate, root)

    # Otherwise, search for a folder of that name
    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        for d in dirnames:
            if d.lower() == query.lower():
                matches.append(os.path.relpath(os.path.join(dirpath, d), root))
    if not matches:
        print(f"Error: Folder '{query}' not found in project.")
        sys.exit(1)
    if len(matches) > 1:
        print(f"Multiple matches found for '{query}':")
        for idx, match in enumerate(matches):
            print(f"{idx}: {match}")
        idx = input("Enter index of folder to use: ")
        try:
            idx = int(idx)
            return matches[idx]
        except Exception:
            print("Invalid selection.")
            sys.exit(1)
    return matches[0]

def write_temp_rule(root, rel_folder, rule_name="temp-folder-rule"):
    rules_dir = os.path.join(root, ".llm-context", "rules")
    os.makedirs(rules_dir, exist_ok=True)
    rule_path = os.path.join(rules_dir, f"{rule_name}.md")
    rel_folder = rel_folder.replace("\\", "/").strip("./")
    # default: include every file under the folder (gitignore will still exclude)
    pattern = f'{rel_folder}/**/*' if rel_folder else '**/*'
    rule_content = f"""---
description: "Temp rule for {rel_folder or '.'}"
only-include:
  full_files:
    - "{pattern}"
---
"""
    with open(rule_path, "w", encoding="utf-8") as f:
        f.write(rule_content)
    return rule_name

def run_llm_context_commands(root, rule_name):
    cmds = [
        ["lc-set-rule", rule_name],
        ["lc-sel-files"],
        ["lc-context"]
    ]
    for cmd in cmds:
        print(">>", " ".join(cmd))
        subprocess.run(cmd, cwd=root, check=True)

def main():
    parser = argparse.ArgumentParser(
        description="Copy all .py files (recursively) from a directory to LLM context, using llm-context CLI."
    )
    parser.add_argument("target", nargs="?", default=None, help="(optional) folder to export context from")
    args = parser.parse_args()

    cwd = os.getcwd()
    root = find_git_root(cwd)

    # Determine which folder to use
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
