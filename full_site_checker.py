"""
Full Site SEO Checker
Ek website ka poora sitemap dhoondta hai (sitemap.xml se, ya agar na mile to
homepage se internal links crawl karke), aur har page ka SEO check karta hai.
"""

import requests
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree
from bs4 import BeautifulSoup

from seo_checker import check_seo


def get_urls_from_sitemap(base_url: str) -> list:
    sitemap_url = urljoin(base_url, "/sitemap.xml")
    try:
        resp = requests.get(sitemap_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return []
        root = ElementTree.fromstring(resp.content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        # Agar yeh sitemap-index hai (sitemaps ka sitemap), to har sub-sitemap ke andar jao
        sitemap_locs = [el.text for el in root.findall(".//sm:sitemap/sm:loc", ns)]
        if sitemap_locs:
            urls = []
            for sub_sitemap in sitemap_locs:
                urls.extend(get_urls_from_sitemap_url(sub_sitemap))
            return urls

        urls = [el.text for el in root.findall(".//sm:url/sm:loc", ns)]
        return urls
    except Exception:
        return []


def get_urls_from_sitemap_url(sitemap_url: str) -> list:
    try:
        resp = requests.get(sitemap_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        root = ElementTree.fromstring(resp.content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        return [el.text for el in root.findall(".//sm:url/sm:loc", ns)]
    except Exception:
        return []


def get_urls_by_crawling(base_url: str, max_pages: int = 15) -> list:
    """Sitemap na mile to homepage se same-domain links nikal ke crawl karo (1 level deep)."""
    domain = urlparse(base_url).netloc
    visited = set()
    to_visit = [base_url]
    found = []

    while to_visit and len(found) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            found.append(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            for a in soup.find_all("a", href=True):
                link = urljoin(base_url, a["href"])
                if urlparse(link).netloc == domain and link not in visited and link not in to_visit:
                    to_visit.append(link)
        except Exception:
            continue

    return found


def check_full_site(base_url: str, max_pages: int = 15) -> list:
    urls = get_urls_from_sitemap(base_url)
    source = "sitemap.xml"

    if not urls:
        urls = get_urls_by_crawling(base_url, max_pages)
        source = "homepage crawl"

    urls = urls[:max_pages]
    print(f"\n{len(urls)} pages mili ({source} ke through). Check kar raha hoon...\n")

    results = []
    for url in urls:
        try:
            report = check_seo(url)
            results.append((url, report))
        except Exception as e:
            results.append((url, {"issues": [f"Page load nahi hua: {e}"], "issues_count": -1}))

    return results


def print_full_site_report(results: list):
    total_issues = 0
    print("=" * 70)
    print("FULL SITE SEO REPORT")
    print("=" * 70)

    for url, report in results:
        count = report.get("issues_count", 0)
        status = "OK" if count == 0 else f"{count} issue(s)"
        print(f"\n[{status}] {url}")
        for issue in report.get("issues", []):
            print(f"    - {issue}")
        if count > 0:
            total_issues += count

    print("\n" + "=" * 70)
    print(f"Total pages checked: {len(results)}")
    print(f"Total issues found across site: {total_issues}")
    print("=" * 70)


if __name__ == "__main__":
    site_url = input("Apni site ka homepage URL daalo (e.g. https://example.com): ").strip()
    results = check_full_site(site_url)
    print_full_site_report(results)
