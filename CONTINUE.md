# MoneyPrinterTurbo — Continue Here

Before changes, run `python scripts/continue_dev.py` from the repository root. Work on `feature/trend-generator` and follow [AGENTS.md](AGENTS.md).

## Current state

- Opt-in multi-format support and `webui/Main.py` integration are complete. Single-format generation retains its existing path; multi-format tasks use `render_variants()` and successful results can be copied into a separate workspace.
- Local and browser tests covered one, two and three formats. Real Pexels, Edge speech and subtitles were validated in all formats. The 21-second Turkish speech test was run through the pipeline, not through the WebUI.
- Edge TTS is pinned at 7.3.1. This machine uses an ignored local trusted CA bundle for Pexels; TLS verification remains enabled.
- Latest relevant verification: 75 targeted tests and 7 service regressions passed; [provider recovery CI](https://github.com/rel1nquash-tech/MoneyPrinterTurbo/actions/runs/40952010685) passed. No claim of subjective audio-quality or synchronization validation.

## Next task

FFmpeg volumedetect on all three existing Turkish outputs reports narration mean/peak -19.5/-3.1 dBFS and final-video mean/peak -22.6/-6.1 dBFS. The earlier 8 kHz sampling result understated the peaks. Cross-correlation of the decoded narration and final-video audio, downmixed to mono at 8 kHz, found a 0 ms peak lag and rounded normalized correlation 1.0000 in all three formats (searched +/-1 second). This checks output audio alignment with the source, not word-level subtitle timing. Listening is still needed to assess perceived loudness and speech/subtitle synchronization. Long square-format captions arise because `voice.create_subtitle()` aggregates Edge word cues into punctuation-delimited script lines. Any future opt-in splitting should preserve word-cue timing and existing defaults; assess readability before changing behavior. Complete Turkish WebUI acceptance when browser automation is available; the in-app browser currently lists the tab but its automation binding reports `browser.user is unavailable`.

Reuse existing evidence before rendering again: `storage/validation/turkish-20261030/render-report.json` and its sample frames. These are local ignored artifacts and may not exist on other machines. Only repeat long renders when relevant changes or unresolved validation require them.

## Verification

For Sprint 6 behavior changes, run `python -m pytest test/video_pipeline test/video_use test/script_studio -q` when the environment permits, plus focused tests as appropriate. For documentation-only work, inspect the diff and relevant commands. Do not claim unrun tests passed.

Detailed dated results, evidence paths and superseded diagnostics: [Sprint 6 history](docs/sprint-6-history.md).
