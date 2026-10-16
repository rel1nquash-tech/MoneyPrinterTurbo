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

Validate the hardened multi-format orchestration and continue controlled integration testing.

- Check GitHub Actions for the latest CI result, including `python -m py_compile webui/Main.py` and targeted pytest suites.
- Manual UI validation remains necessary in this order: one selected format, then two formats, then all three formats.
- Consider focused tests for UI orchestration without importing Streamlit's full page.
- Do not touch `task.py`.

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
