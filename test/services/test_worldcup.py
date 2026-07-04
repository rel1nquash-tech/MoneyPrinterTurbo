import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.models.schema import VideoParams
from app.services import worldcup


class TestWorldCupPreset(unittest.TestCase):
    def test_apply_worldcup_defaults_sets_safe_short_defaults(self):
        params = VideoParams(video_subject="Morocco 2022 run")

        result = worldcup.apply_worldcup_defaults(params)

        self.assertIs(result, params)
        self.assertEqual(params.video_language, "en")
        self.assertEqual(params.video_aspect, "9:16")
        self.assertEqual(params.video_count, 1)
        self.assertEqual(params.video_clip_duration, 4)
        self.assertEqual(params.video_concat_mode, "sequential")
        self.assertTrue(params.match_materials_to_script)
        self.assertTrue(params.subtitle_enabled)
        self.assertEqual(params.video_terms, worldcup.DEFAULT_SAFE_BROLL_TERMS)
        self.assertIn("30-50 second", params.video_script_prompt)
        self.assertIn("faceless", params.custom_system_prompt.lower())

    def test_apply_worldcup_defaults_preserves_manual_script_and_terms(self):
        params = VideoParams(
            video_subject="Argentina vs France",
            video_script="Manual narration.",
            video_terms=["stadium crowd", "fans with flags"],
            video_script_prompt="Use my custom instructions.",
            custom_system_prompt="Use my custom system prompt.",
            video_clip_duration=2,
        )

        worldcup.apply_worldcup_defaults(params)

        self.assertEqual(params.video_script, "Manual narration.")
        self.assertEqual(params.video_terms, ["stadium crowd", "fans with flags"])
        self.assertEqual(params.video_script_prompt, "Use my custom instructions.")
        self.assertEqual(params.custom_system_prompt, "Use my custom system prompt.")
        self.assertEqual(params.video_clip_duration, 2)

    def test_apply_worldcup_defaults_replaces_only_blank_terms(self):
        params = VideoParams(video_subject="World Cup history", video_terms="   ")

        worldcup.apply_worldcup_defaults(params)

        self.assertEqual(params.video_terms, worldcup.DEFAULT_SAFE_BROLL_TERMS)

    def test_safe_terms_do_not_request_match_footage(self):
        unsafe_words = ["broadcast", "highlight", "official footage", "match clip"]

        joined_terms = " ".join(worldcup.DEFAULT_SAFE_BROLL_TERMS).lower()

        for word in unsafe_words:
            self.assertNotIn(word, joined_terms)

    def test_webui_safe_stock_sources_are_pexels_and_pixabay(self):
        self.assertEqual(worldcup.SAFE_STOCK_SOURCES, ("pexels", "pixabay"))

    def test_build_subject_uses_only_supplied_topic_facts(self):
        subject = worldcup.build_subject(
            {
                "match": "Argentina vs France, 2022 final",
                "angle": "why the final felt impossible to predict",
                "facts": [
                    "Argentina led 2-0",
                    "France came back",
                ],
            }
        )

        self.assertIn("Argentina vs France, 2022 final", subject)
        self.assertIn("Angle: why the final felt impossible to predict", subject)
        self.assertIn("Facts: Argentina led 2-0; France came back", subject)

    def test_load_topics_keeps_only_dict_items(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump([{"match": "Morocco 2022"}, "skip me"], handle)
            topic_path = handle.name

        try:
            topics = worldcup.load_topics(topic_path)
        finally:
            Path(topic_path).unlink(missing_ok=True)

        self.assertEqual(topics, [{"match": "Morocco 2022"}])


if __name__ == "__main__":
    unittest.main()
