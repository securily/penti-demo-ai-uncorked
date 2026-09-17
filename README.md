# Penti demo — AI Uncorked

<p align="center">
  <a href="https://penti.ai"><img src="docs/penti-logo.svg" alt="Penti" height="36" /></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://www.silverlogic.com"><img src="docs/silverlogic-logo.jpg" alt="The SilverLogic" height="56" /></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://www.brdgit.com"><img src="docs/brdgit-logo.jpg" alt="BRDGIT" height="56" /></a>
</p>

<p align="center">
  <strong>Penti</strong>
  · hosted by <strong>The SilverLogic</strong>
  · sponsored by <strong>BRDGIT</strong>
</p>

Live Harbor Books agent from **Stop Chatting. Start Looping: Live Agents in Production**.

Shared for **[AI Uncorked](https://lnkd.in/ec9E_khp)** at **The SilverLogic** HQ, Boca Raton — Wednesday, September 16, 2026, 5:30–8:30 PM (6413 Congress Ave #130). Talk by **Cariel Cohen**, Co-Founder and CTO of **[Penti.ai](https://penti.ai)**. Sponsored by **[BRDGIT](https://www.brdgit.com)**.

This is the same Read → Eval → Print → Loop you watch on stage: an agent looks at the books, decides one next step, runs it, and repeats until leftover cash matches the register.

---

## What you will see

Harbor Books closed December rent.

| | Amount |
|---|---|
| Budget | **$10,000** |
| Cash paid | **$10,000** |
| Register leftover | still **$10,000** (wrong — should be **$0**) |

The agent must make the books match the cash. It reads `books/`, then writes a corrected line to `books/leftover.csv`.

---

## Requirements

- **macOS or Linux** (Windows works with the activate path below)
- **Python 3.10 or newer** (`python3 --version`)
- **At least one LLM API key** — Gemini is the fastest to mint

You do **not** need AWS, Docker, or a Penti account.

---

## Setup — step by step

### 1. Clone this repo

```bash
git clone https://github.com/securily/penti-demo-ai-uncorked.git
cd penti-demo-ai-uncorked
```

### 2. Create a virtualenv and install Python packages

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add an API key

```bash
cp .env.example .env
```

Open `.env` in any editor and paste **at least one** real key on the matching line:

| Variable | Where to mint it |
|---|---|
| `GEMINI_API_KEY` | https://aistudio.google.com/app/apikey |
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| `ANTHROPIC_API_KEY` | https://console.anthropic.com/settings/keys |

Optional (only if you already have them): `CURSOR_API_KEY`, `MUSE_API_KEY`.

Do **not** commit `.env`. Do not put key values in the README or the UI.

### 4. Start the server

```bash
python server.py
```

You should see:

```
Harbor Books budget REPL → http://127.0.0.1:8785
  Keys present: gemini
```

(`Keys present` lists whichever providers you pasted.)

### 5. Open the demo

In a browser: **http://127.0.0.1:8785**

Click **settings** (top right) to confirm keys show `present`. Pick a model, then click **The files** → **Begin**.

---

## How to walk the loop

Each round is four beats:

1. **Look** — the agent reads what is in `books/`
2. **Decide** — it picks one command (and you can **Run and compare** another model)
3. **Do** — the command runs in a sandbox
4. **Repeat** — keep the result and look again

Definition of done (on screen):

1. See the register still leftover **$10,000**
2. See the receipt: paid **$10,000**
3. Write `books/leftover.csv` so spent is **$10,000** and leftover is **$0**

Allowed commands: `cat`, `head`, `ls`, `grep`, `python3`, `echo`, and writing `books/leftover.csv`. No network from the sandbox.

---

## Restart the books

If a run already wrote `leftover.csv`, open **settings** → **Restart books**, or stop the server and delete `books/leftover.csv`. Then refresh the page.

---

## Tests (optional)

```bash
source .venv/bin/activate
python -m pytest -q
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ERR_CONNECTION_REFUSED` on :8785 | The server is not running. From the repo: `source .venv/bin/activate && python server.py` |
| Settings says a key is `missing` | The value is empty or `.env` is in the wrong folder. Keys must be in `penti-demo-ai-uncorked/.env`. Restart `python server.py` after editing. |
| “No API key for …” when you hit Decide | Same as above — restart after saving `.env`. |
| Port already in use | Something else is on 8785. Stop it, or change `PORT` in `server.py`. |
| Cursor / Composer models fail | Those need a local Penti educational workspace. Use Gemini, OpenAI, or Claude for the stranger path. |

---

## License

MIT — see `LICENSE`.
