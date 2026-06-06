# webcrawler-py

An async web crawler that maps internal links, generates JSON and CSV reports, and visualises the site structure as a directed graph.

## Prerequisites

- **Python 3.14+**
- **uv** — fast Python package manager

Install `uv` if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on Windows:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Installation

```bash
git clone https://github.com/your-username/webcrawler-py.git
cd webcrawler-py
uv sync
```

## Usage

### One-off crawl

```bash
uv run main.py
```

The URL and limits are read from environment variables (see [Configuration](#configuration)). Set them in a `.env` file before running.

**Example `.env` for crawling a local site:**

```env
CRAWL_URL=https://example.com/
MAX_CONCURRENCY=3
MAX_PAGES=50
MAX_DEPTH=5
```

Then run:

```bash
uv run main.py
```

### Scheduled crawl (every 24 hours)

```bash
uv run scheduler.py
```

The scheduler runs an immediate crawl on startup, then repeats on the configured interval. Press `Ctrl+C` to stop.

## Output files

| File | Description |
|------|-------------|
| `report.json` | Full crawl results — base URL, timestamp, total pages crawled, and per-page data (headings, paragraphs, internal/external links, image URLs). |
| `report.csv` | Flat CSV version of the same data, one row per crawled page. |
| `graph.png` | 1920×1080 directed-graph image showing internal links between pages. Node size scales with the number of incoming links. |

If the crawl is interrupted with `Ctrl+C`, a partial report is saved to `report_partial.json`.

## Configuration

All configuration is done through environment variables. Create a `.env` file in the project root:

```env
# Required for email reports
EMAIL_USER=you@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
RECIPIENT_EMAIL=recipient@example.com

# Crawl settings (optional — defaults shown)
CRAWL_URL=https://crawler-test.com/
MAX_CONCURRENCY=3
MAX_PAGES=25
MAX_DEPTH=20
```

> **Note:** `EMAIL_PASSWORD` must be a [Gmail App Password](https://support.google.com/accounts/answer/185833), not your account password. Never commit `.env` to version control.

| Variable | Default | Description |
|----------|---------|-------------|
| `EMAIL_USER` | — | Gmail address used to send reports |
| `EMAIL_PASSWORD` | — | Gmail App Password |
| `RECIPIENT_EMAIL` | — | Address that receives the report email |
| `CRAWL_URL` | `https://crawler-test.com/` | Root URL to crawl |
| `MAX_CONCURRENCY` | `3` | Maximum simultaneous HTTP connections |
| `MAX_PAGES` | `25` | Maximum pages to crawl per run |
| `MAX_DEPTH` | `20` | Maximum link depth from the root URL |

## Limitations

- **Same-domain only.** The crawler follows internal links exclusively. External URLs are recorded in page data but not crawled.
- **Static HTML only.** Pages rendered by JavaScript (SPAs) are not supported — only the raw HTML returned by the server is parsed.
- **No robots.txt compliance.** The crawler does not check or honour `robots.txt` rules before fetching pages.
- **Rate limiting not handled.** If the target site returns `429 Too Many Requests`, the crawler retries with exponential backoff but does not adapt its concurrency dynamically.
