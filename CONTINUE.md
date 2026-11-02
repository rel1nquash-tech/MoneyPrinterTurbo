# MoneyPrinterTurbo — Continue Here

Before changes, run `python scripts/continue_dev.py` from the repository root. Work on `feature/trend-generator` and follow [AGENTS.md](AGENTS.md).

## Current state

- Opt-in multi-format support and `webui/Main.py` integration are complete. Single-format generation retains its existing path; multi-format tasks use `render_variants()` and successful results can be copied into a separate workspace.
- Local and browser tests covered one, two and three formats. Real Pexels, Edge speech and subtitles were validated in all formats. The 21-second Turkish speech test covered the direct pipeline. A separate 15-second Turkish Pexels/Emel single-format test succeeded through Main WebUI on 2026-11-02; evidence: storage/tasks/38a5f7bb-8833-4226-a938-f854e05630e5/final-1.mp4 and storage/validation/turkish-20261030/ui-turkish-frame.png.
- Edge TTS is pinned at 7.3.1. This machine uses an ignored local trusted CA bundle for Pexels; TLS verification remains enabled.
- Latest relevant verification: 75 targeted tests and 7 service regressions passed; [provider recovery CI](https://github.com/rel1nquash-tech/MoneyPrinterTurbo/actions/runs/40952010685) passed. No claim of subjective audio-quality or synchronization validation.

## Next task

The user prefers English content with English narration and English subtitles. Use English for future content and acceptance tests unless requested otherwise; prior Turkish results remain useful evidence but Turkish-specific validation is not required. Existing English Pexels/Edge samples (storage/validation/edge-731/render-report.json) cover 9:16, 1:1 and 16:9. On 2026-11-03, source-vs-output audio cross-correlation at 8 kHz showed 0 ms peak lag and rounded 1.0000 correlation in each format; English SRT text and 0.10–1.65 s cue were present. This does not replace listening or establish word-level subtitle sync.

The requested multi-format implementation and controlled production checks are complete. English content is the preferred direction. The user liked the English sample; no explicit listening/synchronization acceptance has been supplied.

Remaining acceptance: user listening feedback on the existing English sample. Optional improvement: shorter square-format captions, only if readability feedback justifies changing the current behavior. Do not keep rerunning completed renders or treating completed Turkish UI checks as blockers. Detailed audio measurements and task IDs are archived below.

Reuse existing evidence before rendering again: `storage/validation/turkish-20261030/render-report.json` and its sample frames. These are local ignored artifacts and may not exist on other machines. Only repeat long renders when relevant changes or unresolved validation require them.

## Verification

For Sprint 6 behavior changes, run `python -m pytest test/video_pipeline test/video_use test/script_studio -q` when the environment permits, plus focused tests as appropriate. For documentation-only work, inspect the diff and relevant commands. Do not claim unrun tests passed.

Detailed dated results, evidence paths and superseded diagnostics: [Sprint 6 history](docs/sprint-6-history.md).
