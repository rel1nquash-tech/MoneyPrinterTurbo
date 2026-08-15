import os
import sys

import streamlit as st

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.script_studio.generator import (  # noqa: E402
    PLATFORM_LABELS,
    generate_package,
)


st.set_page_config(
    page_title="AI Script Studio",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title("✍️ AI Script Studio")
st.caption("Tek bir trendden yayınlanmaya hazır içerik paketi oluştur.")

prefilled_subject = st.session_state.get("video_subject", "")
trend_category = st.session_state.get("trend_category", "")

subject = st.text_area(
    "Konu",
    value=prefilled_subject,
    height=90,
    placeholder="Örn. Yapay zekâda bu haftanın en önemli gelişmesi...",
)

col1, col2, col3 = st.columns(3)
with col1:
    language = st.text_input("Dil", value="tr-TR")
with col2:
    duration = st.slider("Hedef süre (sn)", min_value=15, max_value=180, value=45, step=5)
with col3:
    category = st.text_input("Kategori", value=trend_category)

selected_labels = st.multiselect(
    "Platformlar",
    options=list(PLATFORM_LABELS.values()),
    default=[
        PLATFORM_LABELS["tiktok"],
        PLATFORM_LABELS["instagram_reels"],
        PLATFORM_LABELS["youtube_shorts"],
        PLATFORM_LABELS["x"],
        PLATFORM_LABELS["threads"],
        PLATFORM_LABELS["linkedin"],
    ],
)
label_to_platform = {label: platform for platform, label in PLATFORM_LABELS.items()}
selected_platforms = [label_to_platform[label] for label in selected_labels]

extra_requirements = st.text_area(
    "Ek talimat (opsiyonel)",
    placeholder="Örn. Finansal konularda abartılı yatırım tavsiyesi verme.",
    height=80,
)

if st.button("🚀 İçerik Paketini Oluştur", type="primary", use_container_width=True):
    if not subject.strip():
        st.error("Önce bir konu gir veya Daily Trends ekranından bir trend seç.")
        st.stop()
    if not selected_platforms:
        st.error("En az bir yayın platformu seç.")
        st.stop()

    with st.spinner("Senaryo ve platform içerikleri hazırlanıyor..."):
        try:
            package = generate_package(
                subject=subject,
                language=language,
                duration=duration,
                platforms=selected_platforms,
                extra_requirements=extra_requirements,
            )
            st.session_state["script_studio_package"] = package
            st.session_state["script_studio_category"] = category
        except Exception as exc:
            st.error(f"İçerik paketi oluşturulamadı: {exc}")

package = st.session_state.get("script_studio_package")
if package:
    st.divider()
    st.subheader("Ana içerik")

    title = st.text_input("Başlık", value=package.title, key="studio_title")
    hook = st.text_area("Hook", value=package.hook, height=100, key="studio_hook")
    script = st.text_area("Senaryo", value=package.script, height=260, key="studio_script")
    cta = st.text_input("CTA", value=package.cta, key="studio_cta")

    st.subheader("Platform içerikleri")
    for platform, copy in package.platforms.items():
        with st.expander(PLATFORM_LABELS.get(platform, platform), expanded=False):
            st.text_input("Başlık", value=copy.title, key=f"studio_{platform}_title")
            st.text_area("Açıklama", value=copy.caption, height=120, key=f"studio_{platform}_caption")
            st.text_input(
                "Hashtag",
                value=" ".join(copy.hashtags),
                key=f"studio_{platform}_hashtags",
            )

    st.divider()
    if st.button("🎬 Video Generator'a Aktar", type="primary", use_container_width=True):
        st.session_state["video_subject"] = title or subject
        st.session_state["video_script"] = f"{hook}\n\n{script}\n\n{cta}".strip()
        st.session_state["video_terms"] = category
        st.session_state["trend_prefill_active"] = True
        st.session_state["script_studio_source"] = True
        st.switch_page("webui/Main.py")
