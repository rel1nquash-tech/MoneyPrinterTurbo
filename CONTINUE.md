# MoneyPrinterTurbo — Continue Here

## One-command resume

This file is the canonical handoff point for continuing the current development work.

From the repository root, run:

```powershell
python scripts/continue_dev.py
```

The command prints the active branch, current commit, working-tree state, the current Sprint 6 status, and the next recommended task.

## Required branch

`feature/trend-generator`

Do **not** continue this work directly on `main`.

## Current state

- World Cup preset/manual API-free pipeline: completed.
- Modular Trends providers: completed.
- Daily Trends WebUI: completed.
- Daily Trends → Video Generator session-state prefill: completed.
- AI Script Studio: completed and CI validated.
- Sprint 6 multi-format pipeline foundation: completed.
  - `app/video_pipeline/variants.py`
  - `app/video_pipeline/planner.py`
  - `app/video_pipeline/runner.py`
  - `test/video_pipeline/test_variants.py`
  - `test/video_pipeline/test_runner.py`
- Safe multi-format video-use aggregation: completed.
  - `prepare_render_workspace()` in `app/video_use/workspace.py`
  - manifest and format-aware workspace tests in `test/video_use/test_workspace.py`
- Multi-format WebUI entry point: added at
  `webui/pages/🎬 Multi-format Video.py`
- Opt-in multi-format selection integrated into `webui/Main.py` (commit `0643f93`, followed by explicit task callback fix `4632d2a`).
- Existing single-format generation path remains the default when the checkbox is off or only one format is selected.
- Main WebUI syntax compilation added to `.github/workflows/script-studio-tests.yml`.
- Multi-format runner now catches per-format task exceptions, logs failures, continues remaining formats, and skips empty video lists; focused regression tests were added.
- Multi-format video-use workspace validates every source and destination before copying, so a missing later source cannot leave partial files that block retries; a regression test covers this case.

## Important safety constraints

1. Preserve existing functionality.
2. Do not modify `app/services/task.py` for this Sprint 6 integration.
3. Keep the existing single-format Video Generator behavior intact.
4. Work only on `feature/trend-generator`.
5. Prefer small, isolated, tested changes.
6. Multi-format rendering must create one existing video-generation task per selected format.
7. Failed formats must not discard successful formats.
8. Original task outputs must remain untouched.
9. Do not automatically render, call an LLM, or alter existing Trend → Video Generator session-state behavior merely by opening a page.

## Current implementation detail

`render_variants()` injects the existing `tm.start()` function and creates independent `VideoParams` copies for each selected aspect ratio. Supported formats are:

- `9:16` → vertical → 1080×1920
- `1:1` → square → 1080×1080
- `16:9` → landscape → 1920×1080

`prepare_render_workspace()` copies successful outputs into a separate `video-use` directory and writes `RENDER_MANIFEST.json` containing source filename, variant, task ID, and original path.

## Next task

Core multi-format hardening and controlled local rendering validation are complete.

- Latest implementation commit f01d9f8 passed GitHub Actions (66 targeted tests and both page compilations).
- Main UI was exercised with one, two, and three formats using local video and custom WAV audio; outputs and workspace copies were verified.
- Longer sources and offline subtitle burn-in are now validated (see extended checkpoint below). External stock/TTS validation is blocked by DNS/timeouts in the current environment.
- Reproduce offline validation with `.venv/Scripts/python scripts/validate_multi_format.py`; it creates real FFmpeg outputs under storage.
- Keep task.py unchanged and preserve opt-in selection.

## Verification before continuing

Run at minimum:

```powershell
python -m py_compile webui/Main.py
python -m pytest test/script_studio test/video_pipeline test/video_use -q
```

Then verify the Streamlit page manually with one format first, followed by all three formats. Never start with three formats when debugging a new integration.

## Recent commits

The latest known commits on this branch include:

- `dce9777` — safe multi-format video-use aggregation tests
- `ac6d555` — multi-format video-use workspace aggregation
- `7300967` — multi-format rendering runner
- `2fe933c` — render planner

The exact current HEAD should always be read from Git rather than assumed from this document.

## Hardening checkpoint (2026-10-27)

Initial clean local HEAD: 79a8666; fetched remote HEAD: 4f965ca. All three handoff commits remain ancestors. GitHub runs 38907738110 and 38907723240 succeeded.

- Runner retains its successful-results list contract and optionally collects typed failures with format, task ID, and reason. Invalid video payloads no longer break later formats or count as successes.
- Planner accepts the default string aspect and deep-copies nested materials. Existing video preprocessing mutates MaterialInfo.url, making isolation necessary.
- Workspace rejects duplicate destinations before copying; original source bytes are preserved.
- Custom audio resolution accepts the existing absolute server file path; no task.py changes needed.
- Local targeted suite after hardening: 57 passed (11 existing Pydantic deprecation warnings). Both WebUI pages compile. Additional UI changes are recorded in the next checkpoint.
- No real FFmpeg/LLM/video generation was performed.

## WebUI checkpoint (2026-10-27)

- Core hardening commit: 4fa834f.
- Main clears previous completed-video state before a new attempt; keeps prefill/material state and the direct single-format tm.start path.
- Both pages show failed format/task/reason and successful format/task outputs. Empty selection starts no task; empty single-format output is rejected.
- Dedicated-page workspaces are scoped to the first successful task, avoiding collisions across render sessions.
- Added executable Main generation-block regression tests with fake UI/task services. These are not browser or real-render tests.
- CI includes both pages' compilation and triggers for the previously omitted workspace/Main/dedicated-page paths.
- Verification: 57 targeted tests passed; both pages compiled. CI for f53561c succeeded: https://github.com/rel1nquash-tech/MoneyPrinterTurbo/actions/runs/40581828163.
- Next: verify pushed CI, then manually validate one, two, and three formats with controlled source/audio inputs.

## Final verification follow-up

- f53561c: WebUI failure reporting, stale-state reset, scoped dedicated workspace, and CI coverage; pushed successfully.
- Expanded UI route tests to assert successful single square/landscape/portrait results and two-format partial success explicitly.
- Final local targeted suite: 58 passed, 11 existing Pydantic warnings. No real video generation or browser interaction performed.
- 940f8d6: final test follow-up pushed; GitHub Actions completed successfully: https://github.com/rel1nquash-tech/MoneyPrinterTurbo/actions/runs/40581918749. All 58 targeted tests and both page compilations passed in CI.
- Remaining work is controlled manual video generation with one, two, then three formats; no real-render success is claimed.

## Real rendering validation (2026-10-27)

- Found a real custom-audio failure: get_audio_duration only accepted lowercase .mp3, despite the uploader accepting WAV/M4A/AAC/FLAC/OGG. Voice duration dispatch now probes all string paths through the existing MoviePy helper; task.py remains untouched.
- Added an opt-in offline real-task smoke script: `.venv/Scripts/python scripts/validate_multi_format.py`. It creates 1-second synthetic video/WAV fixtures, disables auto-upload in its process, and exercises one, two, then three formats with real FFmpeg.
- Real smoke completed all six outputs. Verified 1080x1920, 1080x1080, 1920x1080 resolutions, nonzero duration, audio, frame decoding, unchanged input SHA-256 hashes, and identical workspace copies.
- Local report: storage/validation/ca0752ab-3e14-406b-ae61-771b14a1e65c/report.json. Generated media stays ignored under storage.
- Targeted unit tests: 66 passed (11 existing Pydantic warnings). Both pages, voice.py and the smoke script compile.
- Browser validation in progress; direct Main single-format generation with uploaded local video and WAV already completed.
- Scope: local materials/custom audio, subtitles off, background music off. External providers/TTS/subtitles are not covered by this smoke run.

## Browser validation completed (2026-10-28)

- Resumed after the local Streamlit server stopped. Existing logs confirmed the one-format and two-format UI runs completed on October 27.
- Three-format UI run completed October 28 with local MP4, uploaded WAV, subtitles off, background music off. The page displayed each format with its own task ID.
- UI task IDs: single 0d6449c8-6045-4143-8b68-e6805fe53621; two-format 8f2ae551-444f-4140-a954-c2a29cec8203 / 9fcdc98f-d0cb-4bc9-b30a-5323c6da325d; three-format 44cb9080-d5d0-4c38-94c0-b8abf64e49bb / 8988d4ea-7621-4e02-b4f5-eb0bb02cae4e / cd2df91e-5e98-4ea5-b7f8-752c95310c6e.
- Independently opened all six UI outputs with MoviePy: expected dimensions, positive duration, audio stream, and decodable first frame verified.
- Prepared the three-format workspace through the UI. All three copies match their original output hashes; fixture video/audio hashes remain unchanged.
- Clearing all formats and pressing Generate displayed "Select at least one output format." and removed the previous post-production output section.
- Local evidence: storage/validation/ca0752ab-3e14-406b-ae61-771b14a1e65c/ui-report.json and ui-three-formats.png.
- CI for f01d9f8: successful, https://github.com/rel1nquash-tech/MoneyPrinterTurbo/actions/runs/40582592635.
- Existing Windows log encoding warnings were avoided on the resumed test server by launching Python with -X utf8. They did not prevent the prior outputs from completing.
- No changes to main or app/services/task.py. External providers/TTS/subtitles remain outside the completed local validation scope.

## Extended subtitle validation (2026-10-28)

- Extended scripts/validate_multi_format.py with --duration (1-30 seconds) and --subtitles. Default smoke behavior is retained. CI now compiles this script too.
- Ran `.venv/Scripts/python -X utf8 scripts/validate_multi_format.py --duration 8 --subtitles` with the real no-voice timeline and Edge subtitle formatter; this uses no remote TTS or Whisper model.
- One, two, then three formats completed: six actual 10-second outputs from an 8-second local source. Verified expected dimensions, audio streams, decodable frames, SRT files, unchanged source hashes and identical workspace copies.
- Visually inspected vertical, square and landscape sample frames: subtitles are burned in and remain within the output frame.
- Evidence: storage/validation/8ddd5bbc-fe12-4e1d-a7a1-08c57951bd34/report.json and PNG frames. This validates subtitle generation/layout with an estimated offline timeline, not speech recognition or speech-to-subtitle synchronization.
- Local targeted suite: 66 passed, 11 existing Pydantic warnings; both pages and validation script compile.
- External probe: Edge TTS en-US-JennyNeural timed out on all three attempts (15 seconds each). Pexels search for nature failed DNS resolution for api.pexels.com. Pixabay/Coverr are not configured. No external provider success is claimed; no credentials or persistent network settings changed.
- Next external step: rerun provider validation once DNS/connectivity is available. Core local rendering and subtitle validation are complete; avoid repeating these runs without a relevant code change.
