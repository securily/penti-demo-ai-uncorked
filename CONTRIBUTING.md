# Contributing

Contributions are welcome. This page covers how to propose a change and what has to pass before it lands.

## Getting set up

```bash
git clone https://github.com/securily/penti-demo-ai-uncorked.git
cd penti-demo-ai-uncorked
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your own keys locally
python -m pytest -q
```

## How a change lands

1. Fork the repository and create a branch off `main`.
2. Make your change. Keep the pull request focused on one thing.
3. Run `python -m pytest -q` and `ruff check .` locally.
4. Open a pull request and fill in the template.
5. Automated checks run, and the maintainer named in [CODEOWNERS](.github/CODEOWNERS) reviews it.
6. Once the checks pass and the review is approved, a maintainer merges it.

Direct pushes to `main` are blocked. Every change, including a maintainer's own, goes through a pull request with an approving review. Approvals from the author of the change do not count.

## Rules that matter most

* **Never commit secrets.** No API keys, tokens, credentials or customer data, not even in tests, fixtures or comments. Keep values in your local `.env`. `.env.example` carries variable names only. Push protection is on and will block a commit that contains a recognized secret; if it fires, rotate that key before doing anything else.
* **No real data.** This demo runs on the sample books in this repository. Do not add real financial records, customer names or production identifiers.
* **Keep dependencies lean.** New dependencies need a reason in the pull request. Dependabot watches what we have.
* **Watch what the agent can execute.** This project runs agent loops that execute commands. Any change that widens what the loop can run should say so in the pull request.

## Style

* Python formatted and linted with [ruff](https://docs.astral.sh/ruff/).
* Clear commit messages in the imperative, for example "add retry to ledger fetch".
* Tests for new behavior go under `tests/`.

## Reporting security issues

Do not open an issue for a vulnerability. Follow [SECURITY.md](SECURITY.md) instead.

## Conduct

By taking part you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
