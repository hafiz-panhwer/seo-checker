"""
SEO Checker - Web App (Streamlit)
Browser mein URL daalo, button dabao, SEO report dekho.
"""

import streamlit as st

from seo_checker import check_seo
from full_site_checker import check_full_site

st.set_page_config(page_title="SEO Checker", page_icon="🔍", layout="centered")

st.markdown(
    """
    <style>
    .main .block-container { max-width: 760px; padding-top: 2.5rem; }

    .hero {
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
        background: linear-gradient(90deg, #4F8BF9, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        color: #9AA0A6;
        font-size: 1.05rem;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.6rem 0;
        font-weight: 600;
        background: linear-gradient(90deg, #4F8BF9, #7C3AED);
        color: white;
        border: none;
        transition: transform 0.15s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        opacity: 0.92;
        color: white;
    }

    .report-card {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-top: 1.2rem;
        background: rgba(127,127,127,0.05);
    }
    .badge-ok {
        display: inline-block;
        background: rgba(46, 204, 113, 0.15);
        color: #2ecc71;
        padding: 0.15rem 0.7rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-warn {
        display: inline-block;
        background: rgba(231, 76, 60, 0.15);
        color: #e74c3c;
        padding: 0.15rem 0.7rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .field-label {
        color: #9AA0A6;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.1rem;
    }
    .footer-note {
        text-align: center;
        color: #7A7A7A;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🔍 SEO Checker</h1>
        <p>Kisi bhi webpage ya poori site ka on-page SEO instantly check karo.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_single, tab_site = st.tabs(["📄 Ek Page", "🌐 Poori Site"])


def render_single_report(report: dict):
    status_badge = (
        '<span class="badge-ok">✓ No Issues</span>'
        if report["issues_count"] == 0
        else f'<span class="badge-warn">{report["issues_count"]} Issue(s)</span>'
    )

    st.markdown(f'<div class="report-card">{status_badge}<br><br>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="field-label">Title</div>', unsafe_allow_html=True)
        st.write(f"{report['title'] or '—'}")
        st.caption(f"{report['title_length']} characters")

        st.markdown('<div class="field-label">H1 Tags</div>', unsafe_allow_html=True)
        st.write(f"{report['h1_count']} found")
        if report["h1_texts"]:
            st.caption(", ".join(report["h1_texts"]))

    with col2:
        st.markdown('<div class="field-label">Meta Description</div>', unsafe_allow_html=True)
        st.write(f"{report['meta_description'] or '(missing)'}")
        st.caption(f"{report['meta_description_length']} characters")

        st.markdown('<div class="field-label">Images without Alt Text</div>', unsafe_allow_html=True)
        st.write(f"{report['images_without_alt']} / {report['total_images']}")

    if report["issues_count"] > 0:
        st.markdown("---")
        st.markdown('<div class="field-label">Issues Found</div>', unsafe_allow_html=True)
        for issue in report["issues"]:
            st.markdown(f"- {issue}")

    st.markdown("</div>", unsafe_allow_html=True)


with tab_single:
    url = st.text_input("URL daalo", placeholder="https://example.com", key="single_url")
    if st.button("Check karo", key="single_btn"):
        if not url.strip():
            st.warning("Pehle URL daalo.")
        else:
            with st.spinner("Check ho raha hai..."):
                try:
                    report = check_seo(url.strip())
                    render_single_report(report)
                except Exception as e:
                    st.error(f"Page check nahi ho saka: {e}")

with tab_site:
    site_url = st.text_input("Site ka homepage URL daalo", placeholder="https://example.com", key="site_url")
    if st.button("Poori Site Check Karo", key="site_btn"):
        if not site_url.strip():
            st.warning("Pehle URL daalo.")
        else:
            with st.spinner("Sitemap se pages dhoond raha hoon aur check kar raha hoon..."):
                try:
                    results = check_full_site(site_url.strip())
                    total_issues = sum(r.get("issues_count", 0) for _, r in results if r.get("issues_count", 0) > 0)
                    ok_pages = sum(1 for _, r in results if r.get("issues_count", 0) == 0)

                    m1, m2, m3 = st.columns(3)
                    m1.metric("Pages Checked", len(results))
                    m2.metric("Clean Pages", ok_pages)
                    m3.metric("Total Issues", total_issues)

                    st.markdown("---")

                    for page_url, report in results:
                        count = report.get("issues_count", 0)
                        icon = "✅" if count == 0 else "⚠️"
                        label = "No issues" if count == 0 else f"{count} issue(s)"
                        with st.expander(f"{icon} {label} — {page_url}"):
                            if count == 0:
                                st.write("Koi issue nahi mila.")
                            else:
                                for issue in report.get("issues", []):
                                    st.markdown(f"- {issue}")
                except Exception as e:
                    st.error(f"Site check nahi ho saka: {e}")

st.markdown('<div class="footer-note">Built with Python + Streamlit</div>', unsafe_allow_html=True)
