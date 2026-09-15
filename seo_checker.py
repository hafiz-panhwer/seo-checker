"""
SEO Checker - core logic
Ek URL leta hai, uska HTML fetch karta hai, aur basic SEO checks karta hai:
- Title tag (hai ya nahi, length theek hai ya nahi)
- Meta description (hai ya nahi, length theek hai ya nahi)
- H1 tag (kitne hain - ek hona chahiye)
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
        issues.append("Title tag missing hai")
    elif len(title_text) > 60:
        issues.append(f"Title bohot lamba hai ({len(title_text)} characters, 60 se kam rakho)")
    elif len(title_text) < 30:
        issues.append(f"Title bohot chota hai ({len(title_text)} characters, 30-60 ke beech rakho)")

    # Meta description check
    meta_desc = soup.find("meta", attrs={"name": "description"})
    desc_text = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else ""
    report["meta_description"] = desc_text
    report["meta_description_length"] = len(desc_text)
    if not desc_text:
        issues.append("Meta description missing hai")
    elif len(desc_text) > 160:
        issues.append(f"Meta description bohot lambi hai ({len(desc_text)} characters, 160 se kam rakho)")
    elif len(desc_text) < 70:
        issues.append(f"Meta description bohot choti hai ({len(desc_text)} characters, 70-160 ke beech rakho)")

    # H1 check
    h1_tags = soup.find_all("h1")
    report["h1_count"] = len(h1_tags)
    report["h1_texts"] = [h1.text.strip() for h1 in h1_tags]
    if len(h1_tags) == 0:
        issues.append("H1 tag missing hai")
    elif len(h1_tags) > 1:
        issues.append(f"Page pe {len(h1_tags)} H1 tags hain, sirf ek hona chahiye")

    # Image alt text check
    images = soup.find_all("img")
    images_without_alt = [img.get("src", "unknown") for img in images if not img.get("alt")]
    report["total_images"] = len(images)
    report["images_without_alt"] = len(images_without_alt)
    if images_without_alt:
        issues.append(f"{len(images_without_alt)} images mein alt text missing hai")

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
    test_url = input("Check karne ke liye URL daalo (e.g. https://example.com): ").strip()
    result = check_seo(test_url)
    print_report(test_url, result)
