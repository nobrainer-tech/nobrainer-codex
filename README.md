# NoBrainer Codex

Use Codex's real capabilities without losing your current model, reasoning setting or conversations. This public toolkit pairs Codex with [nobrainer-tech-flow](https://github.com/nobrainer-tech/nobrainer-tech-flow): bounded Luna delegation, visible context, session handoffs and an evidence-led external SSD guide. Focused worker scopes can avoid repeatedly loading a full project brief; token savings depend on the actual task. A configured window never expands a model beyond its real limit.

## Start from a URL

Give your coding agent this prompt:

> Install NoBrainer Codex from https://github.com/nobrainer-tech/nobrainer-codex. Read the repository instructions and `docs/spec.md`. Run `python3 install.py --check` first, explain the exact changes to me, then run `python3 install.py --apply` for the configuration I authorized. Keep my selected MAIN model, reasoning effort, sign-in and existing chats. Confirm the readback. For external SSD relocation, stop at the separate backup/encryption and owner approval gates in `docs/external-ssd.md`; never run a legacy migration script.

Clone before running code (Python **3.11+**, Git and an existing Codex installation required):

```bash
git clone https://github.com/nobrainer-tech/nobrainer-codex.git
python3 nobrainer-codex/install.py --check
python3 nobrainer-codex/install.py --apply
```

Windows PowerShell uses `py -3.11 nobrainer-codex/install.py --check` and then `--apply`. Pass `--codex-home PATH` if you use a nondefault `CODEX_HOME`. If no model catalog proves the selected model's window, the installer leaves context settings unchanged and reports the missing evidence. No browser/desktop account actions or external disk writes occur during installation.

## What it does

- Installs the owner's five [nobrainer-tech-flow](https://github.com/nobrainer-tech/nobrainer-tech-flow) global instruction bullets in `AGENTS.md` and makes no new sidebar conversation.
- Sets the configured upper bound of **15 concurrent subagents** and the default worker model to **GPT-6 Luna**. Dispatching depends on useful independent tasks and the actual host/provider capacity.
- When the active model appears in a local catalog with a verified limit, sets its configured context window to that limit (GPT-6 Astra/Luna/Sol currently advertise **872,000**) and a 90% compaction threshold. Does not change the selected model or effort.
- Shows context remaining, used and window size in the **CLI** status line. Desktop users can inspect context with `/status`; desktop UI support is not inferred from the TUI setting.

The actual context window and subagent capacity may be less than local configuration permits. `max` is a model-specific reasoning option, not a knob to apply to every conversation: the installer leaves manually chosen reasoning unchanged. For a focused strategy, choose Sol low/medium or Astra low for MAIN and delegate independent work to Luna at a supported per-task effort.

## SSD, recovery and upgrades

Read [External SSD runbook](docs/external-ssd.md) before moving a byte. The official desktop app bundle stays in its supported install location. A configuration file or symlink is not proof that the GUI uses relocated data, or that the official Dock icon refuses startup when the SSD is missing. Preserve verified backups and the original source until the owner confirms the result.

Sources: [Codex configuration reference](https://developers.openai.com/codex/config-file/config-reference), [environment variables](https://developers.openai.com/codex/config-file/environment-variables), [slash commands](https://developers.openai.com/codex/reference/slash-commands), [nobrainer-tech-flow](https://github.com/nobrainer-tech/nobrainer-tech-flow).
