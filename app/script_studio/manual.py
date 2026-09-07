"""Manual Script Studio flow that does not call an LLM provider."""


def _clean(value: str) -> str:
    return (value or "").strip()


def build_manual_video_payload(
    subject: str,
    title: str,
    hook: str,
    script: str,
    cta: str,
    visual_terms: str,
) -> dict[str, str]:
    """Validate and format a manually written script for Video Generator."""
    video_subject = _clean(title) or _clean(subject)
    narration_parts = [_clean(hook), _clean(script), _clean(cta)]
    video_script = "\n\n".join(part for part in narration_parts if part)

    if not video_subject:
        raise ValueError("Bir konu veya başlık gir.")
    if not _clean(script):
        raise ValueError("En az bir senaryo metni gir.")
    if not _clean(visual_terms):
        raise ValueError("Pexels için en az bir görsel arama terimi gir.")

    return {
        "video_subject": video_subject,
        "video_script": video_script,
        "video_terms": _clean(visual_terms),
    }
