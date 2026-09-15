"""
SEO Checker - Web App (Streamlit)
Browser mein URL daalo, button dabao, SEO report dekho.
"""

import streamlit as st

from seo_checker import check_seo
from full_site_checker import check_full_site

st.set_page_config(page_title="SEO Checker", page_icon="🔍")

st.title("🔍 SEO Checker")
st.write("Kisi bhi webpage ya poori site ka on-page SEO check karo.")

mode = st.radio("Kya check karna hai?", ["Ek page", "Poori site (sitemap se)"])

url = st.text_input("URL daalo", placeholder="https://example.com")

if st.button("Check karo"):
    if not url.strip():
        st.warning("Pehle URL daalo.")
    else:
        with st.spinner("Check ho raha hai..."):
            if mode == "Ek page":
                try:
                    report = check_seo(url.strip())
                    st.subheader("Result")
                    st.write(f"**Title:** {report['title']} ({report['title_length']} chars)")
                    st.write(f"**Meta Description:** {report['meta_description'] or '(missing)'} ({report['meta_description_length']} chars)")
                    st.write(f"**H1 tags:** {report['h1_count']} -> {report['h1_texts']}")
                    st.write(f"**Images without alt text:** {report['images_without_alt']} / {report['total_images']}")

                    if report["issues_count"] == 0:
                        st.success("Koi SEO issue nahi mila!")
                    else:
                        st.error(f"{report['issues_count']} issue(s) mile:")
                        for issue in report["issues"]:
                            st.write(f"- {issue}")
                except Exception as e:
                    st.error(f"Page check nahi ho saka: {e}")
            else:
                try:
                    results = check_full_site(url.strip())
                    total_issues = sum(r.get("issues_count", 0) for _, r in results if r.get("issues_count", 0) > 0)
                    st.subheader(f"{len(results)} pages checked — {total_issues} total issues")
                    for page_url, report in results:
                        count = report.get("issues_count", 0)
                        with st.expander(f"{'✅' if count == 0 else '⚠️ ' + str(count) + ' issue(s)'} — {page_url}"):
                            for issue in report.get("issues", []):
                                st.write(f"- {issue}")
                            if count == 0:
                                st.write("Koi issue nahi.")
                except Exception as e:
                    st.error(f"Site check nahi ho saka: {e}")

st.caption("Built with Python + Streamlit")
