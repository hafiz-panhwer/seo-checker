# SEO Checker

A simple Python tool that checks any webpage (or an entire site via its sitemap) for common on-page SEO issues:

- Title tag missing or wrong length
- Meta description missing or wrong length
- Missing or duplicate H1 tags
- Images without alt text

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Check a single page:

```bash
python seo_checker.py
```

Check an entire site (uses `sitemap.xml` automatically, falls back to crawling internal links):

```bash
python full_site_checker.py
```

## Example output

```
[2 issue(s)] https://example.com/some-page/
    - Meta description is too long (187 characters, keep it under 160)
    - Page has 2 H1 tags, there should be only one
```

## Roadmap

- [ ] Wrap as an MCP server so AI assistants (Claude, etc.) can call it directly
- [ ] Keyword density check
- [ ] Broken link detection
