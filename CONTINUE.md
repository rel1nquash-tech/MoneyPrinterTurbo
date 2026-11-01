# MoneyPrinterTurbo — Continue Here

Before changes, run `python scripts/continue_dev.py` from the repository root. Work on `feature/trend-generator` and follow [AGENTS.md](AGENTS.md).

## Current state

- Opt-in multi-format support and `webui/Main.py` integration are complete. Single-format generation retains its existing path; multi-format tasks use `render_variants()` and successful results can be copied into a separate workspace.
- Local and browser tests covered one, two and three formats. Real Pexels, Edge speech and subtitles were validated in all formats. The 21-second Turkish speech test was run through the pipeline, not through the WebUI.
- Edge TTS is pinned at 7.3.1. This machine uses an ignored local trusted CA bundle for Pexels; TLS verification remains enabled.
- Latest relevant verification: 75 targeted tests and 7 service regressions passed; [provider recovery CI](https://github.com/rel1nquash-tech/MoneyPrinterTurbo/actions/runs/40952010685) passed. No claim of subjective audio-quality or synchronization validation.

## Next task

Investigate the low sampled narration levels with an appropriate loudness measurement and listen for speech/subtitle synchronization. Assess whether long square-format captions should be split. Complete Turkish WebUI acceptance when browser automation is available; previous browser automation could not verify the current URL.

Reuse existing evidence before rendering again: `storage/validation/turkish-20261030/render-report.json` and its sample frames. These are local ignored artifacts and may not exist on other machines. Only repeat long renders when relevant changes or unresolved validation require them.

## Verification

For Sprint 6 behavior changes, run `python -m pytest test/video_pipeline test/video_use test/script_studio -q` when the environment permits, plus focused tests as appropriate. For documentation-only work, inspect the diff and relevant commands. Do not claim unrun tests passed.

Detailed dated results, evidence paths and superseded diagnostics: [Sprint 6 history](docs/sprint-6-history.md).
