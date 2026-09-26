#!/usr/bin/env python3
"""Bounded, cross-platform Codex configuration installer (Python 3.11+)."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import tomllib

FLOW = "https://github.com/nobrainer-tech/nobrainer-tech-flow"
INSTRUCTIONS = f"""# NoBrainer.Tech Flow

- Use NoBrainer.Tech Flow ({FLOW}) through nobrainer-ultra. If missing, install it for the current client using the repository's installation instructions; verify availability and report any blocker honestly.
- Preserve the MAIN model and effort selected by the user. Aggressively and proactively delegate independent work to native GPT-6 Luna subagents, using the exact identifier supported by the host (`gpt-6-luna` or `openai/gpt-6-luna`). Choose supported effort per task; do not force a fixed level or silently substitute another model.
- Maximize useful parallelism to minimize time to a verified result: actively split work into independent tasks, fill all available subagent slots while ready work exists, and promptly assign the next task when a worker finishes. Use the maximum concurrency supported by the host; never create filler tasks merely to fill slots. Give each a clear outcome, relevant context, exclusive write scope and verification criteria. MAIN works in parallel, integrates and verifies results. Avoid duplicated work, conflicting edits and unnecessary delegation. No recursive delegation or new sidebar conversations without explicit authorization.
- Load the relevant Flow skills and their required references for research, planning, implementation, writing and review. Follow project instructions, preserve facts and write naturally in the user's language.
- Complete the requested outcome with the smallest sufficient changes and verification at the actual delivery layer. Preserve unrelated work and secrets. Reuse existing authorization; ask only for a material missing decision or new consequential action. Do not claim success from configuration or another agent's report alone.
"""

STATUS_LINE = '["model-with-reasoning", "context-remaining", "context-used", "context-window-size"]'
TABLE = re.compile(r"^\s*\[([^\]]+)\]\s*(?:#.*)?$")


def set_key(text: str, section: str | None, key: str, value: str) -> str:
    lines = text.splitlines(keepends=True)
    current = None
    matches = []
    ending = len(lines)
    for i, line in enumerate(lines):
        header = TABLE.match(line)
        if header:
            current = header.group(1).strip()
        elif current == section and re.match(rf"^\s*{re.escape(key)}\s*=", line):
            matches.append(i)
    if len(matches) > 1:
        raise ValueError(f"Multiple values for {section or 'root'}.{key}; manual review required")
    replacement = f"{key} = {value}\n"
    if matches:
        lines[matches[0]] = replacement
        return "".join(lines)
    current = None
    start = None
    for i, line in enumerate(lines):
        header = TABLE.match(line)
        if header:
            if current == section:
                ending = i
                break
            current = header.group(1).strip()
            if current == section:
                start = i + 1
    if section is None:
        ending = next((i for i, line in enumerate(lines) if TABLE.match(line)), len(lines))
        lines.insert(ending, replacement)
    elif start is None:
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines += [f"\n[{section}]\n", replacement]
    else:
        lines.insert(ending, replacement)
    return "".join(lines)


def selected_ceiling(config: dict, home: Path) -> tuple[int | None, str]:
    model = config.get("model")
    if not isinstance(model, str):
        return None, "No explicit default model; current conversation choices preserved"
    raw_path = config.get("model_catalog_json")
    if not isinstance(raw_path, str):
        return None, "No local verified model catalog; context override unchanged"
    path = Path(os.path.expandvars(raw_path)).expanduser()
    if not path.is_absolute():
        path = home / path
    if not path.is_file():
        return None, "Model catalog unavailable; context override unchanged"
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("models", [])
    if not isinstance(rows, list):
        raise ValueError("Unexpected model catalog shape")
    matched = [row for row in rows if isinstance(row, dict) and row.get("slug") == model]
    if len(matched) != 1:
        return None, "Selected model missing/ambiguous in catalog; context override unchanged"
    row = matched[0]
    ceiling = row.get("max_context_window")
    if not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling < 8192 or ceiling > 2_000_000:
        raise ValueError("Model ceiling outside verified catalog range")
    return ceiling, f"Catalog advertises {model} at {ceiling} tokens"


def atomic_write(path: Path, data: bytes, mode: int) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=".nobrainer-codex-", dir=path.parent)
    try:
        if hasattr(os, "fchmod"):
            os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if not hasattr(os, "fchmod"):
            os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect/apply NoBrainer Codex without changing authentication or selected conversation settings.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="read-only preview")
    group.add_argument("--apply", action="store_true", help="back up then apply exact changes")
    parser.add_argument("--codex-home", type=Path, help="defaults to CODEX_HOME or ~/.codex")
    options = parser.parse_args()
    home = (options.codex_home or Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))).expanduser()
    if not home.is_dir():
        parser.error("Existing Codex home required; installer never initializes a new profile")
    targets = [home / "AGENTS.md", home / "config.toml"]
    if any(path.is_symlink() or (path.exists() and not path.is_file()) for path in targets):
        parser.error("AGENTS.md/config.toml must be ordinary files; stop to preserve managed links")
    if not targets[1].is_file():
        parser.error("Existing Codex config.toml required; run signed-in Codex first")
    original = targets[1].read_text(encoding="utf-8")
    config = tomllib.loads(original)
    if "max_threads" in config.get("agents", {}):
        parser.error("Legacy agents.max_threads present; resolve it before setting the newer concurrency key")
    window, reason = selected_ceiling(config, home)
    changed = original
    if window:
        changed = set_key(changed, None, "model_context_window", str(window))
        changed = set_key(changed, None, "model_auto_compact_token_limit", str(window * 9 // 10))
    changed = set_key(changed, "agents", "max_concurrent_threads_per_session", "15")
    changed = set_key(changed, "agents", "default_subagent_model", '"openai/gpt-6-luna"')
    changed = set_key(changed, "tui", "status_line", STATUS_LINE)
    result = tomllib.loads(changed)
    for field in ("model", "model_reasoning_effort", "plan_mode_reasoning_effort", "models"):
        if result.get(field) != config.get(field):
            raise ValueError(f"Unexpected change to owner-selected {field}")
    for key in config:
        if key not in {"model_context_window", "model_auto_compact_token_limit", "agents", "tui"}:
            if config[key] != result[key]:
                raise ValueError(f"Unexpected config change: {key}")
    requested = {"codex_home": str(home), "model_selected": config.get("model"),
                 "reasoning_selected": config.get("model_reasoning_effort"),
                 "context_ceiling": window, "context_evidence": reason,
                 "will_change": [str(path) for path, data in zip(targets, (INSTRUCTIONS, changed))
                                 if (path.read_text(encoding="utf-8") if path.is_file() else "") != data]}
    if options.check or not requested["will_change"]:
        print(json.dumps(requested, ensure_ascii=False, indent=2))
        return 0
    folder = home / ("nobrainer-codex-backup-" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    folder.mkdir(mode=0o700)
    preimages = {}
    for path in targets:
        preimages[path] = path.read_bytes() if path.exists() else None
        if preimages[path] is not None:
            shutil.copy2(path, folder / path.name)
    try:
        for path, payload in zip(targets, (INSTRUCTIONS, changed)):
            atomic_write(path, payload.encode("utf-8"), path.stat().st_mode & 0o777 if path.exists() else 0o600)
        assert targets[0].read_text(encoding="utf-8") == INSTRUCTIONS
        actual = tomllib.loads(targets[1].read_text(encoding="utf-8"))
        assert actual == result
    except Exception:
        for path, prior in preimages.items():
            if prior is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, prior, 0o600)
        raise
    requested["backup"] = str(folder)
    requested["readback"] = "PASS"
    print(json.dumps(requested, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"Installer stopped without applying new settings: {error}", file=sys.stderr)
        sys.exit(2)
