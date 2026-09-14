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

Controlled Main.py integration.

Target behavior:

- Keep the current single-format path unchanged when one format is selected.
- Add an opt-in multi-format selection to the existing Video Generator UI.
- When multiple formats are selected, call `render_variants()` rather than duplicating the task-generation implementation.
- Store the successful multi-format results in session state without breaking the existing completed-video fields.
- Use `prepare_render_workspace()` for the optional video-use post-production action when multi-format results exist.
- Do not touch `task.py`.
- Add focused tests before considering the integration complete.

## Verification before continuing

Run at minimum:

```powershell
python -m pytest test/video_pipeline test/video_use test/script_studio test/video_use -q
```

Then verify the Streamlit page manually with one format first, followed by all three formats. Never start with three formats when debugging a new integration.

## Recent commits

The latest known commits on this branch include:

- `dce9777` — safe multi-format video-use aggregation tests
- `ac6d555` — multi-format video-use workspace aggregation
- `7300967` — multi-format rendering runner
- `2fe933c` — render planner

The exact current HEAD should always be read from Git rather than assumed from this document.
