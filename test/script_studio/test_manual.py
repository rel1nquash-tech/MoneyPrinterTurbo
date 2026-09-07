import pytest

from app.script_studio.manual import build_manual_video_payload


def test_build_manual_video_payload_formats_transfer_values():
    payload = build_manual_video_payload(
        subject="AI trend",
        title="AI update",
        hook="Stop scrolling.",
        script="A short narration.",
        cta="Follow for more.",
        visual_terms="artificial intelligence, data center",
    )

    assert payload["video_subject"] == "AI update"
    assert payload["video_script"] == "Stop scrolling.\n\nA short narration.\n\nFollow for more."
    assert payload["video_terms"] == "artificial intelligence, data center"


@pytest.mark.parametrize(
    ("subject", "title", "script", "visual_terms", "message"),
    [
        ("", "", "A script.", "ai", "konu veya başlık"),
        ("AI", "", "", "ai", "senaryo"),
        ("AI", "", "A script.", "", "arama terimi"),
    ],
)
def test_build_manual_video_payload_validates_required_values(
    subject, title, script, visual_terms, message
):
    with pytest.raises(ValueError, match=message):
        build_manual_video_payload(
            subject=subject,
            title=title,
            hook="",
            script=script,
            cta="",
            visual_terms=visual_terms,
        )
