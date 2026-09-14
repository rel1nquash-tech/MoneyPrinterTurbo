import os
from uuid import uuid4

import streamlit as st
from loguru import logger

from app.config import config
from app.models.schema import VideoParams
from app.services import task as tm
from app.utils import utils
from app.video_pipeline.runner import render_variants
from app.video_pipeline.variants import all_video_variants
from app.video_use.workspace import prepare_render_workspace


st.set_page_config(page_title="Multi-format Video", page_icon="🎬", layout="wide")

st.title("🎬 Multi-format Video")
st.caption(
    "Güvenli Sprint 6 entegrasyonu: mevcut video üretim task'ına dokunmadan "
    "9:16, 1:1 ve 16:9 çıktıları ayrı task'lar olarak üretir."
)

subject = st.text_input("Video Subject", key="multi_format_subject")
script = st.text_area("Video Script", height=240, key="multi_format_script")
terms = st.text_input("Video Keywords", key="multi_format_terms")

col1, col2, col3 = st.columns(3)
with col1:
    source_options = ["pexels", "pixabay", "coverr", "local"]
    source = st.selectbox("Video Source", source_options, key="multi_format_source")
with col2:
    clip_duration = st.selectbox("Clip Duration", [2, 3, 4, 5, 6, 7, 8, 9, 10], index=1)
with col3:
    video_count = st.selectbox("Videos per format", [1, 2, 3, 4, 5], index=0)

selected_formats = st.multiselect(
    "Output Formats",
    options=[variant.key for variant in all_video_variants()],
    default=["9:16"],
    format_func=lambda value: next(
        variant.label for variant in all_video_variants() if variant.key == value
    ),
    help="Her format için ayrı bir mevcut video-generation task'ı çalıştırılır.",
)

if source == "pexels" and not config.app.get("pexels_api_keys", ""):
    st.warning("Pexels API Key yapılandırılmamış.")
elif source == "pixabay" and not config.app.get("pixabay_api_keys", ""):
    st.warning("Pixabay API Key yapılandırılmamış.")
elif source == "coverr" and not config.app.get("coverr_api_keys", ""):
    st.warning("Coverr API Key yapılandırılmamış.")

if st.button("🚀 Generate Selected Formats", type="primary", use_container_width=True):
    if not subject and not script:
        st.error("Video Subject ve Video Script aynı anda boş olamaz.")
        st.stop()
    if not selected_formats:
        st.error("En az bir output format seçmelisin.")
        st.stop()
    if source == "pexels" and not config.app.get("pexels_api_keys", ""):
        st.error("Pexels API Key gerekli.")
        st.stop()
    if source == "pixabay" and not config.app.get("pixabay_api_keys", ""):
        st.error("Pixabay API Key gerekli.")
        st.stop()
    if source == "coverr" and not config.app.get("coverr_api_keys", ""):
        st.error("Coverr API Key gerekli.")
        st.stop()

    params = VideoParams(video_subject=subject, video_script=script)
    params.video_terms = terms
    params.video_source = source
    params.video_clip_duration = clip_duration
    params.video_count = video_count

    progress = st.empty()
    results = []

    def start_task(task_id: str, variant_params: VideoParams):
        progress.info(f"Generating {variant_params.video_aspect.value} …")
        logger.info(
            "Starting multi-format task {} ({})",
            task_id,
            variant_params.video_aspect.value,
        )
        return tm.start(task_id=task_id, params=variant_params)

    with st.spinner("Selected video formats are being generated…"):
        results = render_variants(params, start_task, selected_formats)

    progress.empty()
    if not results:
        st.error("Seçilen formatların hiçbiri başarıyla üretilemedi.")
        st.stop()

    st.success(f"{len(results)} format başarıyla üretildi.")

    for result in results:
        st.subheader(f"{result.variant.label} ({result.variant.key})")
        for video_file in result.videos:
            st.video(video_file)
            st.caption(f"Task: {result.task_id}")

    try:
        workspace = prepare_render_workspace(
            base_dir=utils.task_dir(),
            render_results=results,
            subject=subject,
            script=script,
        )
        st.subheader("✨ video-use workspace")
        st.caption(
            "Orijinal task çıktıları değiştirilmez. Tüm başarılı formatlar ayrı dosyalar "
            "olarak workspace'e kopyalanır ve manifest ile eşleştirilir."
        )
        st.code(workspace.command, language="powershell")
        st.success(f"Workspace hazır: {workspace.path}")
    except (OSError, ValueError) as exc:
        st.warning(f"Video-use workspace hazırlanamadı: {exc}")
