import os
import sys

import streamlit as st

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.trends.webui import (  # noqa: E402
    apply_video_generator_prefill,
    get_provider_options,
    get_topics_for_providers,
    topics_to_json,
)


st.set_page_config(
    page_title="Daily Trends",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title("🔥 Daily Trends")
st.caption("Trend seç, önce Script Studio ile içeriği hazırla veya doğrudan video üret.")

provider_options = get_provider_options()
provider_names = [name for name, _ in provider_options]
provider_labels = {name: label for name, label in provider_options}

selected_providers = st.multiselect(
    "Providers",
    options=provider_names,
    default=provider_names,
    format_func=lambda name: provider_labels[name],
)

topics = get_topics_for_providers(selected_providers)

if not topics:
    st.info("Select at least one provider to see daily trends.")
    st.stop()

export_json = topics_to_json(topics)

if st.button("Generate All", type="primary"):
    st.session_state["daily_trends_export_json"] = export_json

for index, topic in enumerate(topics):
    with st.container(border=True):
        st.subheader(topic.title)
        st.write(topic.description)
        st.metric("Score", topic.score)

        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button(
                "✍️ Open Script Studio",
                key=f"script_topic_{index}_{topic.category}",
                use_container_width=True,
            ):
                apply_video_generator_prefill(st.session_state, topic)
                st.session_state["script_studio_topic_id"] = topic.id
                st.session_state["script_studio_category"] = topic.category
                st.switch_page("pages/✍️ AI Script Studio.py")

        with action_col2:
            if st.button(
                "🎬 Generate Video",
                key=f"generate_topic_{index}_{topic.category}",
                use_container_width=True,
            ):
                apply_video_generator_prefill(st.session_state, topic)
                st.switch_page("Main.py")

if st.session_state.get("daily_trends_export_json"):
    st.code(st.session_state["daily_trends_export_json"], language="json")
    st.download_button(
        "Download JSON",
        data=st.session_state["daily_trends_export_json"],
        file_name="daily-trends.json",
        mime="application/json",
    )
