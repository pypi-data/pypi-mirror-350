# lc-dir

**Instantly copy all relevant Python files from any folder in your project to your clipboard—perfect for use with AI code assistants and LLMs.**

---

## Why use lc-dir?

When working with LLMs (like ChatGPT, Claude, or Copilot), you often need to share **only part of your codebase**—a single directory, a feature, or a component, not the whole repo.

**lc-dir** lets you do exactly that.  
- No more zipping folders or hand-pasting dozens of files.
- No more sending the entire project when only one area matters.
- Get context for refactoring, debugging, or reviewing code **fast**.

---

## Key Features

- **Easy:** Instantly copies all `.py` files under any directory (recursively) to your clipboard, ready for LLMs.
- **Flexible:** Works from any subfolder, or specify any target directory.
- **Search:** Give it a folder name; it’ll find the match for you.
- **Integrated:** Uses your [llm-context](https://github.com/ContextLab/llm-context) workflow for formatting and clipboard.

---

## Installation

first install llm-context CLI if you haven't already:
```sh
pipx install llm-context
```

Then, install `lc-dir`:

```sh
pipx install lc-dir
````

*(or use `pip install --user lc-dir` if you prefer)*

**Requirements:**

* Python 3.10+
* The [llm-context](https://github.com/ContextLab/llm-context) CLI, initialized in your project (run `lc-init` once per repo).

---

## How to Use

> **Example:** Copy all `.py` files from the current directory and below:

```sh
lc-dir
```

> **Example:** Copy all `.py` files from a specific subdirectory (recursively):

```sh
lc-dir path/to/subdir
```

> **Example:** Search for a folder by name, even if you’re not sure where it is:

```sh
lc-dir common
```

If more than one match is found, you’ll be prompted to choose.

---

### Typical Workflow

1. **Navigate** anywhere in your project directory tree.
2. Run `lc-dir [optional-subfolder]`
3. **Paste** in your LLM interface.

   * The clipboard will contain all relevant code, formatted for LLMs, just as if you ran `llm-context` but limited to your chosen scope.

---

## Use Cases

* **LLM-powered code review:** Share just the area you want help with.
* **Refactoring:** Provide only the module or feature you’re working on.
* **Bug fixing:** Send just the files around the problem.
* **Onboarding:** Give teammates or LLMs a focused view of part of the repo.

---

## Troubleshooting

* If the clipboard isn’t updated, ensure you’ve initialized your repo with `lc-init`.
* If you see “ModuleNotFoundError”, re-install with `pipx install lc-dir` and check your Python version.
* You must have [llm-context](https://github.com/ContextLab/llm-context) CLI installed in the project for this to work.

---

## License

MIT

---

**Contributions and issues welcome!**
