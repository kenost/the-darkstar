# The Darkstar

A daily, static research newspaper about black holes and neutron stars. The publisher reads recent arXiv abstracts, selects previously unused papers, uses Sol to select and draft attributed reporting and Terra for an independent source audit, creates a research-inspired cover illustration, and writes a dated edition plus an archive. Every article links to the source preprint, preferably its current arXiv HTML rendering (falling back to the abstract page when HTML is unavailable). It does **not** represent preprints as peer-reviewed findings.

## Repository branches

- [`main`](https://github.com/kenost/the-darkstar/tree/main) contains only the generated static website served by GitHub Pages.
- [`source`](https://github.com/kenost/the-darkstar/tree/source) contains this publisher, its deployment script and timer definitions, dependencies, and documentation. It does not contain generated editions, the local issue-data archive, machine credentials, or the legacy tunnel/notification configuration.

The generator runs on Ken's machine because its OpenClaw model authentication is local. Changes to this branch do not themselves deploy an edition. The 07:20 Helsinki timer builds `site/`; the 08:00 timer mirrors that directory to `main`. Commit and push publisher changes to `source` separately. GitHub Pages is configured to serve `main` from its root; it never serves this source branch.

## Local edition

```sh
python3 -m pip install -r requirements.txt
export GEMINI_API_KEY=... # only for cover art; set privately, do not commit
# OpenClaw Gateway must have usable openai/gpt-6-sol and openai/gpt-6.1-terra routes
python3 publish.py
python3 -m http.server 8000 --directory site
```

`publish.py --date YYYY-MM-DD` makes a dated edition. It exits without changing anything if that edition already exists; `--force` replaces it. `--dry-run` reports the eligible shortlist without calling AI. An editorial AI pass chooses 3–7 articles according to the strength of that day's research. An incomplete run never updates the front page. `site/` is the deployable static artifact; `issues/` is the source archive used for duplicate checks. If the raster image API is out of quota, the text AI attempts a validated SVG cover; if that also fails, a deterministic illustration directed by the AI's research-specific image brief keeps the edition publishable. The site labels the method used.

## Daily automation

The active `darkstar-publish.timer` runs the publisher at 07:20 Helsinki time on Ken's machine. It selects and drafts with `openai/gpt-6-sol`, then audits with `openai/gpt-6.1-terra` through the authenticated OpenClaw Gateway, using a dedicated `darkstar-editor` agent with no personal memory or messaging bindings. The publisher verifies the actual model returned and stops rather than publishing on a silent provider fallback. Gemini remains the raster-image route for the cover; if its quota is unavailable, Sol attempts a validated SVG illustration before the deterministic fallback. The Gemini key is stored only in the private service environment. The service allows up to 30 minutes for research and generation. The publisher calls the installed OpenClaw CLI at `~/.npm-global/bin/openclaw` (override with `DARKSTAR_OPENCLAW_BIN`); the agent ID can be overridden with `DARKSTAR_OPENCLAW_AGENT`. Back issues and duplicate checks persist in `issues/`.

Generation is not run by GitHub Actions because the Gateway's local OAuth profile is not available to a GitHub-hosted runner. If moving generation to GitHub later, configure a supported hosted model credential and an equivalent publishing route first.

## Stable free hosting: GitHub Pages

The primary public address is `https://kenost.github.io/the-darkstar/`. This is a GitHub Pages project site: static files live at the root of the **public** repository `kenost/the-darkstar`'s `main` branch, with Pages set to **Deploy from a branch → main → /(root)**. The machine's SSH key authenticates as `kenost`, so no API token is needed for the daily upload. Do not put secrets or publisher source on the Pages **branch**.

`python3 ops/deploy_github_pages.py` pushes the current site and dated issues to its `main` branch. The script uses a separate checkout in `~/.local/state/the-darkstar/pages-checkout`, mirrors **only** the public `site/` tree, and pushes `main`. It is idempotent and never puts `.git` under the local web server's document root. The Pages URL serves the current front page, both archived editions and shared assets independently of the local tunnel. Generated pages carry canonical links to the stable address.

The upload service and timer are installed and enabled under `~/.config/systemd/user`. The existing 07:20 publisher continues to use local Sol/Terra credentials; the upload timer runs at 08:00 Helsinki time and retries every six hours, without requiring those credentials on GitHub. Its first manual run succeeded. The old quick tunnel still serves previously shared links as a legacy route, but its changing-URL notification timer is disabled now that Pages is primary.

Cloudflare Pages Direct Upload is a good alternative if a Cloudflare account becomes available: its free plan provides a fixed `*.pages.dev` name, 500 builds/month and 20,000 static files; a local Wrangler upload can deploy the same `site/` folder. It needs an account, a Pages project, and a Pages-edit API token. Netlify's current 300-credit free plan charges 15 credits per production deployment, so a daily issue would exhaust its deploy allowance in about 20 days even before bandwidth use.

## Local service setup

The versioned `ops/darkstar-publish.*` and `ops/darkstar-pages-deploy.*` systemd units document the live daily schedule. Install them under `~/.config/systemd/user` on the publishing machine, then reload and enable the timers. The unit files currently contain that machine's absolute workspace path; adjust it on another host. Put `GEMINI_API_KEY=...` in `~/.config/the-darkstar/environment` with permissions `0600` (never in Git). The earlier Cloudflare Quick Tunnel is a legacy route for old links, not the primary host, and its local service files are not stored on this branch.

The masthead has a light/dark switch. It saves each reader's preference in local storage, including across dated issues; the generated pages and archived editions share `site/theme.js` and `site/style.css`.

## Email subscription path

Do not launch email subscriptions on the rotating Quick Tunnel URL: links inside sent mail cannot be repaired after a tunnel restart. First establish a stable public URL (for example a free `github.io` or Cloudflare Pages address using an account under Ken's control). Then generate one digest per successfully published issue from `issues/YYYY-MM-DD.json`: edition date and permalink, each article title, deck (ingress), and a direct article anchor. Send only after the issue is publicly reachable; use the issue date as an idempotency key so retries do not mail twice. A hosted mailing-list provider should manage opt-in confirmation, unsubscribe links, suppression and bounced addresses; subscriber emails should never be stored in `site/` or `issues/`.

Current free options (checked 27 Nov 2026): [follow.it](https://follow.it/publishers/features-and-pricing) offers a basic RSS-to-email plan with unlimited followers/emails, but its free polling is up to six hours and messages may carry provider branding/ads; one RSS item per edition containing the article titles and decks would give a daily digest. [EmailOctopus](https://emailoctopus.com/pricing) offers 2,500 subscribers and 10,000 sends/month, enough for about 333 daily recipients in a 30-day month, with more control over the exact email. [MailerLite](https://www.mailerlite.com/pricing) offers 250 subscribers and 2,500 sends/month, about 83 daily recipients. [Buttondown](https://buttondown.com/pricing) is free for the first 100 subscribers but RSS-to-email is a paid add-on. No mailing-list provider account or subscriber form is configured yet.

If the daily publisher fails, its locally configured failure handler alerts Ken; the previous edition stays live. That private notification unit is not versioned here.

## Editorial contract

The generator uses arXiv Atom entries and bounded excerpts from the original PDFs when available. It prioritizes recent black-hole/neutron-star research, excludes previously used arXiv IDs, checks title similarity, and passes prior headlines into every drafting prompt. Its editorial brief asks for question-led, mechanism-first explanations of *why* a result matters, not abstract paraphrases or sensational headlines. It requests distinct deep and accessible treatments, explicit uncertainty and original-paper citations. It validates source IDs/links and rejects unsupported reference URLs. The people profile now follows the researchers and their collaboration beyond the current paper, with enough space for a substantive 650–850-word account. The generator reads affiliations from the paper's first page and fetches earlier arXiv publications shared by at least two current authors. It also retrieves representative prior work by individual authors and cites earlier papers separately. It builds the collaboration story from documented coauthor overlap and methods, and silently omits unsupported personal details instead of writing defensive asides. It does not invent degrees, personal history, or project roles. The publisher can attach a real, appropriately licensed team or instrument photograph from its curated library; it never depicts synthetic people as actual researchers. For up to two non-lead stories, the AI may plan a source-grounded, text-free editorial illustration of the physical scene or structure if it adds visual understanding. No prose cards, flowcharts or labels are drawn inside the image; captions carry the explanation and distinguish conceptual art from data. It never invents a researcher portrait or passes illustration off as an observation. The full paper should still be read before treating any quantitative claim as settled.

Source-grounded equations, when useful, are converted at publication time into native MathML with plain-language captions; the converter is self-hosted in `vendor/` (MIT license), so readers need no external math script. On phones, story text uses larger type and responsive images; the page has no horizontal overflow at 320, 390 or 500 CSS-pixel widths. Cover captions explain the depicted physics and identify the source paper. The About section discloses AI assistance without making production method the caption's headline.

Publication is intentionally stopped if source retrieval, text generation, validation, or artwork fails. This avoids silently publishing an empty or misleading daily edition.
