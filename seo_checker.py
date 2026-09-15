"""
SEO Checker - core logic
Takes a URL, fetches its HTML, and runs basic on-page SEO checks:
- Title tag (present, and correct length)
- Meta description (present, and correct length)
- H1 tag (count - there should be exactly one)
- Images without alt text
"""

import requests
from bs4 import BeautifulSoup


def check_seo(url: str) -> dict:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    issues = []
    report = {}

    # Title check
    title_tag = soup.find("title")
    title_text = title_tag.text.strip() if title_tag else ""
    report["title"] = title_text
    report["title_length"] = len(title_text)
    if not title_text:
        issues.append("Title tag is missing")
    elif len(title_text) > 60:
        issues.append(f"Title is too long ({len(title_text)} characters, keep it under 60)")
    elif len(title_text) < 30:
        issues.append(f"Title is too short ({len(title_text)} characters, keep it between 30-60)")

    # Meta description check
    meta_desc = soup.find("meta", attrs={"name": "description"})
    desc_text = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else ""
    report["meta_description"] = desc_text
    report["meta_description_length"] = len(desc_text)
    if not desc_text:
        issues.append("Meta description is missing")
    elif len(desc_text) > 160:
        issues.append(f"Meta description is too long ({len(desc_text)} characters, keep it under 160)")
    elif len(desc_text) < 70:
        issues.append(f"Meta description is too short ({len(desc_text)} characters, keep it between 70-160)")

    # H1 check
    h1_tags = soup.find_all("h1")
    report["h1_count"] = len(h1_tags)
    report["h1_texts"] = [h1.text.strip() for h1 in h1_tags]
    if len(h1_tags) == 0:
        issues.append("H1 tag is missing")
    elif len(h1_tags) > 1:
        issues.append(f"Page has {len(h1_tags)} H1 tags, there should be only one")

    # Image alt text check
    images = soup.find_all("img")
    images_without_alt = [img.get("src", "unknown") for img in images if not img.get("alt")]
    report["total_images"] = len(images)
    report["images_without_alt"] = len(images_without_alt)
    if images_without_alt:
        issues.append(f"{len(images_without_alt)} image(s) are missing alt text")

    report["issues"] = issues
    report["issues_count"] = len(issues)

    return report


def print_report(url: str, report: dict):
    print(f"\n=== SEO Report: {url} ===\n")
    print(f"Title: {report['title']} ({report['title_length']} chars)")
    print(f"Meta Description: {report['meta_description'][:80]}... ({report['meta_description_length']} chars)")
    print(f"H1 count: {report['h1_count']} -> {report['h1_texts']}")
    print(f"Images: {report['total_images']} total, {report['images_without_alt']} without alt text")
    print(f"\nTotal Issues Found: {report['issues_count']}")
    for i, issue in enumerate(report["issues"], 1):
        print(f"  {i}. {issue}")
    print()


if __name__ == "__main__":
    test_url = input("Enter a URL to check (e.g. https://example.com): ").strip()
    result = check_seo(test_url)
    print_report(test_url, result)
