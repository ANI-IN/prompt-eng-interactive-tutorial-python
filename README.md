# Prompt Engineering for Python Engineers

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ANI-IN/prompt-eng-interactive-tutorial-python)

A hands-on, notebook-based course that teaches prompt engineering and LLM application development with the Claude API, written for software engineers who already know Python. You craft real prompts against a live Claude model and a programmatic grader tells you whether each exercise passes. Every notebook is a standard Jupyter notebook that runs on a regular Python kernel and calls Claude through the official [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python).

> **New here? Read [Getting Started](#getting-started) top to bottom.** The most common setup problems are an API key that the kernel hasn't picked up yet and a `.env` file in the wrong folder. Both are covered in detail below.

---

## Contents

- [Who this is for](#who-this-is-for)
- [What you'll learn](#what-youll-learn)
- [Repository layout](#repository-layout)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Option A: GitHub Codespaces (zero install)](#option-a-github-codespaces-zero-install)
  - [Option B: Local setup (step by step)](#option-b-local-setup-step-by-step)
- [How the exercises and grading work](#how-the-exercises-and-grading-work)
- [Solutions](#solutions)
- [Validating the course](#validating-the-course)
- [Troubleshooting](#troubleshooting)
- [Notes, costs, and the pinned model](#notes-costs-and-the-pinned-model)
- [Known limitations](#known-limitations)

---

## Who this is for

Software engineers comfortable with Python, REST APIs, JSON, and Git. No prior LLM or prompt-engineering experience is required. If you can read a `requests.get` call and write a function, you're ready.

---

## What you'll learn

Each chapter teaches one core technique and names it explicitly so you can connect the hands-on practice to the wider prompt-engineering literature.

| Chapter | Technique |
|---|---|
| 00 Setup and How To | Environment check + your first API call |
| 01 Basic Prompt Structure | Prompt anatomy: system, user, and assistant roles |
| 02 Being Clear and Direct | Clear and direct instruction |
| 03 Assigning Roles | Role prompting (persona prompting) |
| 04 Separating Data and Instructions | Templates and XML delimiters |
| 05 Formatting Output | Output formatting and structured responses (JSON Schema + Pydantic) |
| 06 Precognition | Chain of Thought (CoT) |
| 07 Using Examples | Few-shot prompting |
| 08 Avoiding Hallucinations | Grounding to reduce hallucinations |
| 09 Complex Prompts from Scratch | Combining every technique |
| 10.1 Appendix | Prompt chaining |
| 10.2 Appendix | Tool use (function calling) + the SDK tool runner |
| 10.3 Appendix | Retrieval-Augmented Generation (RAG) |

Work through them in order. Each lesson builds on the previous ones.

---

## Repository layout

```
.
├── notebooks/            # The course. 13 notebooks (00 → 10.3). Start here.
├── notebooks_solved/     # Fully-solved copies of every notebook, saved with their outputs.
├── lib/
│   ├── helpers.py        # get_completion(prompt, system=""), client, MODEL; loads .env
│   └── grading.py        # tiny grading helpers used by the exercises
├── hints.py              # per-exercise hints (printed by the hint cells)
├── tests/                # offline test suite (no API key needed)
├── tools/
│   └── run_notebooks.py  # executes notebooks end to end against the live API
├── .devcontainer/        # GitHub Codespaces config (installs requirements + the kernel)
├── .env.example          # template: copy to .env and add your key
├── requirements.txt      # Python dependencies
└── README.md
```

The helper wraps the Anthropic Messages API in a single function:

```python
from lib.helpers import get_completion, MODEL
print(get_completion("In one sentence, what is an idempotent HTTP method?"))
```

`get_completion(prompt, system="")` is all you need for most chapters. Chapters that need the full API (structured outputs, tool use) call `client.messages.create(...)` directly with the shared `client`, and read the reply with `response_text(response)`.

The first code cell of every notebook finds the project root (the folder that contains `lib/helpers.py`) and puts it on `sys.path`, so the imports work regardless of the directory Jupyter starts the kernel in.

---

## Getting started

### Prerequisites

| Requirement | Notes |
|---|---|
| **Python 3.10+** | 3.11 or 3.12 recommended. Check with `python3 --version`. |
| **An Anthropic API key** | Create one at [console.anthropic.com](https://console.anthropic.com). A small amount of credit is enough for the whole course. |
| **A Jupyter front-end** | Either **VS Code** + the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extensions (recommended), or JupyterLab (installed by `requirements.txt`). |
| **Git** | To clone the repository. |

All Python dependencies (`anthropic`, `python-dotenv`, `jupyterlab`, `ipykernel`, ...) are listed in `requirements.txt`.

---

### Option A: GitHub Codespaces (zero install)

Everything runs in your browser; the dev container installs the requirements, registers the Jupyter kernel, and configures the editor automatically.

1. **Add your API key once.** On GitHub: **Settings → Codespaces → Secrets → New secret**. Name it exactly `ANTHROPIC_API_KEY`, paste your key, and grant **this repository** access to it.
2. **Launch the Codespace.** Click the **Open in GitHub Codespaces** badge above, or **Code → Codespaces → Create codespace on main**. The first build takes a minute or two while the dependencies install.
3. **Open a notebook** from `notebooks/`. Click **Select Kernel** (top right) and choose **Python (prompt-eng)** (or the default Python 3.12 environment).
4. **Run the cells.** Your `ANTHROPIC_API_KEY` secret is picked up automatically (the container also writes it into a gitignored repo-root `.env`), so the first API call works immediately.

> Codespaces gives personal accounts a free monthly quota. Stop or delete the Codespace when you're done to conserve it.

If a notebook reports an authentication error in Codespaces, the secret wasn't set before the container started. Add the `ANTHROPIC_API_KEY` secret, then **rebuild the container** (Command Palette → *Codespaces: Rebuild Container*).

---

### Option B: Local setup (step by step)

Follow these in order. **The order matters.** In particular, add your `.env` and then **restart the kernel** so the key is actually loaded.

#### Step 1: Clone the repository

```bash
git clone https://github.com/ANI-IN/prompt-eng-interactive-tutorial-python.git
cd prompt-eng-interactive-tutorial-python
```

#### Step 2: Create a virtual environment and install dependencies

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Step 3: Register the Jupyter kernel

This registers a kernel named **Python (prompt-eng)** that points at the virtual environment, so VS Code and JupyterLab run the notebooks with the packages you just installed:

```bash
python -m ipykernel install --user --name prompt-eng-python --display-name "Python (prompt-eng)"
```

- **VS Code users:** install the **Python** (`ms-python.python`) and **Jupyter** (`ms-toolsai.jupyter`) extensions. You can also pick `.venv` directly from **Select Kernel → Python Environments**.
- **JupyterLab users:** run `jupyter lab` from the project root (with the venv active) and choose the **Python (prompt-eng)** kernel.

#### Step 4: Add your API key

Create the environment file **in the project root** and set your key:

```bash
cp .env.example .env
# then edit .env and set:
# ANTHROPIC_API_KEY=sk-ant-your-real-key
```

> ⚠️ **The `.env` file must live in the repository root**, not in `notebooks/`. `lib/helpers.py` loads `<project root>/.env` (one level up from `lib/`), regardless of which folder the kernel runs from. A key placed in `notebooks/.env` will **not** be read.

`.env` is gitignored, so your key is never committed. Never paste your key into a notebook cell. If your shell already exports `ANTHROPIC_API_KEY`, that value wins over `.env`.

#### Step 5: Restart the kernel after configuring `.env`

This is the single most common gotcha. **The key is read only once, the first time `lib.helpers` is imported**, and Python caches the module for the rest of the kernel session.

- If you create or edit `.env` **after** the kernel already ran the import cell, the client was built without a key, and re-running the cell will **not** fix it (the import is cached).
- **Fix:** restart the kernel, then run cells from the top.
  - VS Code: the **Restart** button at the top of the notebook, or Command Palette → **Jupyter: Restart Kernel**.
  - JupyterLab: **Kernel → Restart Kernel**.

**Rule to remember:** any time you change `.env`, restart the kernel.

#### Step 6: Run your first notebook

1. Open `notebooks/00_Setup_and_How_To.ipynb`.
2. Select the **Python (prompt-eng)** kernel (top-right kernel picker).
3. Run the cells top to bottom. The first code cell prints the model and `API key configured: True`; the next cell prints a one-sentence answer from Claude.

If that prints an answer, your environment is working. Move on to `01_Basic_Prompt_Structure.ipynb` and continue in order.

---

## How the exercises and grading work

Each chapter has one or more **exercise cells** containing a placeholder like `"[Replace this text]"`. Replace it with your own prompt, run the cell, and a grader prints:

```
This exercise has been correctly solved: True
```

The graders are deterministic substring/shape checks (e.g. "the response contains `404`", "the JSON has a `summary` string"). Any prompt that produces the required output passes; there's rarely a single right answer. Each exercise is followed by a hint cell that prints a hint from `hints.py`.

- **Editing a prompt does NOT require a kernel restart.** Only editing `.env` does. Just re-run the cell.
- **Unfilled placeholders are never sent to Claude.** While a prompt still contains `"[Replace this text"` (or `"[Build your prompt here"`), `get_completion` prints a reminder and returns an empty string, so the exercise grades `False` and costs nothing.
- Some cells **intentionally send malformed requests** to teach you the API contract (e.g. a message missing its `role` returns `400 ... messages.0.role: Field required` in Chapter 1). Those cells catch `anthropic.BadRequestError` and print it, so "Run All" keeps going. The markdown above them says so; that error is the lesson, not a bug.
- Exercises 9.1 and 9.2 have no automated grader: you evaluate your prompt against a success-criteria checklist.

---

## Solutions

`notebooks_solved/` contains **fully-solved copies** of every notebook, with each placeholder filled in and the outputs from a full validation run saved in place, so you can read the expected output of every cell without spending tokens. Open any of them, select the kernel, and **Run All** to reproduce a passing solution end to end. Use them to check your work or to get unstuck, but try each exercise yourself first.

Model output varies from run to run, so your text will differ from the saved outputs; the grades should not.

---

## Validating the course

Offline checks (no API key needed): grading helpers, hint coverage, valid Python in every code cell, exercise/solved notebook parity, no committed secrets:

```bash
python -m pytest -q
```

Live end-to-end run (needs `ANTHROPIC_API_KEY`; costs a little API credit):

```bash
python tools/run_notebooks.py                       # every solved notebook; all graded exercises must pass
python tools/run_notebooks.py --folder notebooks    # every exercise notebook; all cells must run without errors
python tools/run_notebooks.py 05 10.2               # just a few chapters
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `WARNING: ANTHROPIC_API_KEY is not set` when importing the helpers | No key in the environment or in the root `.env`. | Create the **root** `.env` (Step 4), then **restart the kernel**. |
| `TypeError: Could not resolve authentication method` | The kernel imported `lib.helpers` before the key was available, and cached a client with no key. | **Restart the kernel** and run from the top. Confirm the key is in the **root** `.env`. |
| Auth error persists after adding the key | `.env` is in `notebooks/` instead of the project root, or the kernel wasn't restarted. | Move `.env` to the repo root; restart the kernel. |
| `ModuleNotFoundError: No module named 'anthropic'` (or `dotenv`) | The notebook is running on a kernel that doesn't have the requirements installed. | Select the **Python (prompt-eng)** kernel (or the `.venv` interpreter). If it's missing, redo Steps 2 and 3. |
| `StopIteration` in the first cell | The notebook was opened outside the project folder, so `lib/helpers.py` can't be found. | Open the notebook from inside the cloned repository. |
| `400 ... messages.0.role: Field required` | This is the **intentional** malformed-request demo in Chapter 1. | Nothing to fix: it illustrates that every message needs a `role`. |
| `400 ... temperature` (or another sampling parameter) | You passed `temperature` to a current model, which doesn't accept it. | Remove it, or use `**SAMPLING_PARAMS`, which only adds it for older models. |
| `WARNING: Claude declined this request (stop_reason='refusal', ...)` and an empty answer | A safety classifier declined the prompt. The most common trigger is asking Claude to write out its "thinking" or "scratchpad" (`category='reasoning_extraction'`). | Rephrase: ask for an analysis of the input (e.g. `<analysis>` tags) instead of Claude's thinking. See Chapter 6. |
| `400 ... tool_choice` | Forced tool use (`{"type": "any"}` / `{"type": "tool"}`) isn't supported on the newest models. | Use `{"type": "auto"}` and ask for the tool in the prompt (see Appendix 10.2). |
| `400 ... credit balance is too low` | Your Anthropic account has no API credits. | Add credit under **Billing** at [console.anthropic.com](https://console.anthropic.com). |
| `401 authentication_error` | Invalid or revoked key. | Regenerate the key in the console, paste it into the **root** `.env`, restart the kernel. |
| `404 not_found_error` mentioning the model | `CLAUDE_MODEL` in `.env` names a model your account can't access, or has a typo. | Remove `CLAUDE_MODEL` to use the default, or fix the model ID. |
| Kernel doesn't appear in the picker | Kernel not registered, or VS Code needs a reload. | Re-run Step 3; reload the VS Code window; **Select Kernel → Jupyter Kernel → Python (prompt-eng)**. |
| `APIConnectionError` / connection error | Network, proxy, or firewall is blocking `api.anthropic.com`. | Check connectivity/VPN/proxy settings. |

Still stuck? Open `notebooks_solved/` for a known-good version of the same cell and compare.

---

## Notes, costs, and the pinned model

- **Model:** the course is pinned to `claude-opus-5-5` (see `lib/helpers.py`). To use another model, set `CLAUDE_MODEL` in `.env` (for example `CLAUDE_MODEL=claude-sonnet-5-5`) and restart the kernel.
- **Determinism:** current Claude models don't accept sampling parameters like `temperature`, so the same prompt can produce slightly different wording between runs. The graders check properties of the answer, not exact text. On older models that do accept it (e.g. `claude-sonnet-4-6`), the helper automatically sends `temperature=0`.
- **Thinking:** current models reason internally before answering. The reasoning arrives as `thinking` blocks, counts toward `max_tokens` (the helper uses 16,000), and is billed as output. Always read replies with `response_text()` (or filter for `block.type == "text"`) rather than `response.content[0].text`.
- **Cost:** exercises are short. A full run of every solved notebook makes roughly 60 API calls and typically costs a few US dollars on the default model (less on Sonnet or Haiku). You must have credit on your Anthropic account.
- **Privacy:** your API key lives only in `.env` (gitignored) or your shell environment. It is never printed by the notebooks and never sent anywhere except Anthropic's API.

---

## Known limitations

- **Outputs vary between runs.** Saved outputs in `notebooks_solved/` are one real run; your text will differ. The exact-match exercises (2.2 `pytest`, 6.2 `A`) are written to be robust but, like any LLM check, could occasionally need a re-run.
- **Model-specific behavior.** The notebooks are validated against `claude-opus-5-5`. A few demonstrations depend on the model: native thinking (Chapter 6) needs a model with adaptive thinking (Sonnet/Opus 4.6 or later), and the `tool_choice` notes in Appendix 10.2 describe the newest models.
- **Appendix 10.3 server tools** (web search, web fetch, Files API) are described with Python snippets but not executed, because they need extra account setup and incur additional charges.
- **Exercises 9.1 and 9.2** are self-assessed against a checklist rather than graded automatically.
