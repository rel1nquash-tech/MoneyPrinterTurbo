# Repository Development Rules

## Start here

Before making changes, read `CONTINUE.md` and run `python scripts/continue_dev.py` from the repository root.

## Branch and safety

- Work only on `feature/trend-generator` for this ongoing project.
- Never make changes directly on `main`.
- Preserve existing behavior and backward compatibility.
- Prefer small, focused, testable changes.
- Inspect the current implementation before editing.
- Do not rewrite large files wholesale when a smaller edit is possible.
- Do not modify `app/services/task.py` for Sprint 6 multi-format work unless the user explicitly authorizes it.
- Do not commit API keys, credentials, tokens, or local configuration secrets.

## Sprint 6 focus

The project is adding opt-in multi-format video generation for 9:16, 1:1, and 16:9. The current foundation lives in `app/video_pipeline/` and the post-production workspace integration lives in `app/video_use/workspace.py`.

The isolated UI page is `webui/pages/🎬 Multi-format Video.py`. The next planned milestone is a controlled integration into `webui/Main.py`.

## Required behavior for Main.py integration

- Preserve the existing single-format path when one format is selected.
- Use the existing `render_variants()` orchestration for multi-format selections.
- Do not duplicate the existing task implementation.
- Preserve existing session-state keys and trend-to-video prefill behavior.
- Aggregate successful outputs even if one format fails.
- Never overwrite or mutate original task output files.
- Use `prepare_render_workspace()` only for successful multi-format results.

## Testing expectations

- Add focused tests for behavior changes.
- Run relevant tests before claiming completion.
- At minimum, run `python -m pytest test/video_pipeline test/video_use test/script_studio -q` for Sprint 6 changes when the environment permits.
- If tests cannot run, state that clearly and do not claim they passed.
- Update `CONTINUE.md` when the current state or next task changes.
