# SEO Checker — Project Guide

This document explains what was built, why, and how it works — so you can confidently explain it to anyone (colleague, interviewer, LinkedIn audience).

---

## 1. What is this project?

A tool that automatically checks a webpage (or an entire website) for common **on-page SEO issues** — the same things an SEO executive checks manually, but done in seconds by code.

It checks:
- **Title tag** — missing, too short (<30 chars), or too long (>60 chars)
- **Meta description** — missing, too short (<70 chars), or too long (>160 chars)
- **H1 tags** — missing, or more than one on a page (should be exactly one)
- **Images without `alt` text** — bad for accessibility and image SEO

It works two ways:
1. **One page at a time** — paste a URL, get a report
2. **Whole site at once** — paste the homepage, it finds the sitemap and checks every page

---

## 2. Why this was built

You already do SEO manually for `etgcalculator.us` and other sites. Checking title length, meta description length, H1 counts, and alt text by hand across dozens of pages is slow and repetitive. This tool automates that repetitive checking so you can focus on strategy instead of manual auditing — and it doubles as a public portfolio piece showing you can build real tools, not just use them.

---

## 3. How it was built — step by step

### Step 1: Environment setup
- Installed Python (a working Python 3.12 install was located and added to the system PATH)
- Installed VS Code as the code editor
- Installed the required packages: `requests` (to fetch web pages), `beautifulsoup4` (to parse HTML)

### Step 2: Core logic (`seo_checker.py`)
- Takes a URL
- Downloads the page's HTML using `requests`
- Parses the HTML using `BeautifulSoup` to find the `<title>`, `<meta name="description">`, `<h1>` tags, and `<img>` tags
- Applies simple rules (e.g. "title should be 30–60 characters") to flag issues
- Returns a structured report (a Python dictionary) with all findings

### Step 3: Full-site checking (`full_site_checker.py`)
- Given a homepage URL, it first tries to fetch `/sitemap.xml` (almost every site has one — it's a standard file search engines use)
- Parses the XML to get a list of every page URL on the site
- If no sitemap exists, it falls back to crawling: starting from the homepage, it follows internal links to discover pages
- Runs the same `check_seo()` logic on every page found, and combines the results into one report

### Step 4: Web interface (`app.py`, using Streamlit)
- Streamlit is a Python library that turns a script into a web app with almost no extra code — no HTML/CSS/JavaScript needed for the basics
- Built a simple UI: a text box for the URL, a button, and a results area
- Added two tabs: "Single Page" and "Full Site"
- Styled it with custom CSS (gradient title, card-style results, colored badges for "No Issues" vs "X Issues") so it looks professional instead of like a bare developer tool

### Step 5: Publishing the code (GitHub)
- Initialized a git repository in the project folder
- Installed GitHub CLI (`gh`) and logged in
- Created a public repository: **https://github.com/hafiz-panhwer/seo-checker**
- Pushed the code — this makes it visible to anyone, and lets people download/reuse it

### Step 6: Hosting it live (Streamlit Community Cloud)
- Streamlit offers free hosting for apps whose code is on GitHub
- Connected the GitHub repo to Streamlit Cloud (via "Sign in with GitHub")
- Deployed the app — Streamlit installs the dependencies from `requirements.txt` and runs `app.py` on their servers
- Result: a public link anyone can open in a browser, no installation needed: **https://seo-checker-aftdz2ljsgzokvcq4jp8g8.streamlit.app/**
- Any time new code is pushed to GitHub, Streamlit Cloud automatically redeploys the app with the update

---

## 4. How it actually works (technical, if someone asks "how does it check SEO?")

1. **Fetching**: `requests.get(url)` sends an HTTP request to the page, just like a browser does, and gets back the raw HTML.
2. **Parsing**: `BeautifulSoup` turns that raw HTML text into a structure you can query, e.g. `soup.find("title")` finds the `<title>` tag instantly instead of manually searching text.
3. **Rule checking**: Plain Python `if` conditions compare lengths and counts against known SEO best-practice ranges (these ranges — 30-60 chars for titles, 70-160 for meta descriptions — are industry-standard SEO guidelines, not invented numbers).
4. **Sitemap discovery**: Most websites publish `sitemap.xml` at a fixed location so Google can find every page. The tool reads this same file, so it "sees" the site the same way Google does.
5. **Web app**: Streamlit re-runs the Python script top-to-bottom every time you interact with the page (click a button, type text), and redraws the UI — that's the whole trick behind how it feels "live."

---

## 5. If someone asks "did you build this yourself?"

Honest answer: **Yes, with AI assistance (Claude)** — you directed what to build, made the decisions (public repo, Streamlit for hosting, design choices), and understand how each part works; the code itself was written with an AI pair-programmer, the same way many developers today use AI tools to move faster. This is a completely normal and increasingly standard way to build software — the important skill is knowing what to build, why, and being able to explain how it works, which this guide covers.

---

## 6. Links to remember

- **Code (GitHub)**: https://github.com/hafiz-panhwer/seo-checker
- **Live app**: https://seo-checker-aftdz2ljsgzokvcq4jp8g8.streamlit.app/

---

## 7. Possible next steps (if you want to keep building)

- Add keyword density checking
- Add broken link detection
- Wrap the checker as an **MCP server** so AI assistants like Claude can call it directly as a tool
- Add a "download report as PDF/CSV" button
