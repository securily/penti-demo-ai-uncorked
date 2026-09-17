# Security Policy

Thanks for helping keep this project and its users safe.

## Reporting a vulnerability

Please report security issues privately. Do not open a public issue, pull request or discussion for a suspected vulnerability.

Two ways to reach us:

* GitHub private vulnerability reporting: open the **Security** tab of this repository and choose **Report a vulnerability**.
* Email: **security@penti.ai**

Please include the affected file or endpoint, the version or commit, reproduction steps, and the impact you believe it has. A proof of concept helps.

## What happens next

| Stage | Target |
|---|---|
| We acknowledge your report | 2 business days |
| We confirm the issue and set a severity | 5 business days |
| We ship a fix or share a remediation plan | 30 days for high and critical findings |

We will keep you updated while we work, and we are happy to credit you in the release notes once a fix is public, unless you prefer to stay anonymous.

## Scope

In scope: the code in this repository.

Out of scope: Penti production systems and any other Penti or Certypie property. Do not test them under this policy. If you want to test a Penti product, write to security@penti.ai first.

## Safe harbor

If you make a good faith effort to follow this policy, keep your testing limited to the scope above, avoid privacy violations and service disruption, and give us reasonable time to respond before any public disclosure, we will treat your research as authorized and will not pursue legal action.

## Running this project safely

This is a demonstration project that runs AI agent loops against local sample data.

* Keep API keys in a local `.env` file. Never commit real keys. `.env.example` lists variable names only.
* Run the agent against the sample books in this repository, not against real financial data.
* Review what an agent loop is allowed to execute before you point it at anything you care about.
