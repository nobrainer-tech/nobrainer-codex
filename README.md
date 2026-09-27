# NoBrainer Codex

**Website:** [nobrainer.tech/codex](https://nobrainer.tech/codex/)

Get more from the Codex app you already use: **15 configured agent slots, catalog-backed context, and a clear way to see when MAX reasoning is offered**. GPT-6 API models list a **1.05M-token context window**, but the Codex client may expose less; this installer uses the selected model's local catalog instead of promising 1M to everyone. [nobrainer-tech-flow](https://github.com/nobrainer-tech/nobrainer-tech-flow) gives MAIN a practical way to delegate scoped Luna work and keep longer sessions on track. Moving Codex data to an external SSD is optional.

## Start from a URL

Give your coding agent this prompt:

> Install NoBrainer Codex from https://github.com/nobrainer-tech/nobrainer-codex. Read the repository instructions and `docs/spec.md`. Run `python3 install.py --check` first. Show me the selected model's catalog-backed context limit, available reasoning levels, and the exact proposed changes. Then run `python3 install.py --apply` for the configuration I authorized and verify the readback. Keep my selected MAIN model, reasoning effort, sign-in and existing chats. Treat external SSD relocation as a separate optional task.

The [public page](https://nobrainer.tech/codex/) has one-click prompt copying and an optional `codex://` link for installations that register the app protocol. That link opens the app; it does not paste or submit the prompt. Open Codex manually if the protocol is unavailable.

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
- When the selected model appears in the local catalog, sets its configured context window to the catalog limit and a 90% compaction threshold. The 1.05M-token GPT-6 API specification is not a guarantee of the same Codex client window.
- Reports the selected model's catalog-listed reasoning levels, including `max` when present. This surfaces the option; it does not change the reasoning effort you selected in a conversation or guarantee that the current client exposes every catalog level.
- Shows context remaining, used and window size in the **CLI** status line. Desktop users can inspect context with `/status`; desktop UI support is not inferred from the TUI setting.

The actual context window and subagent capacity can be lower than configuration permits. The toolkit does not create tokens or unlock a provider limit. Scoped workers can avoid repeatedly loading irrelevant project context, but token savings depend on the task. Keep MAIN on the model and effort you chose; use `max` deliberately when the model and client offer it.

## Optional: external SSD

Running out of internal storage? Read the [external SSD runbook](docs/external-ssd.md) before moving a byte. The installer never moves data. Desktop launch behavior and rollback need separate, real-host verification.

If Browser interaction stops working after a move or update, the same runbook covers live-helper checks and the optional in-app Computer Use route when that tool is exposed in your Codex conversation. A visible sidebar tab alone is not proof of interaction access.

Sources: [Codex configuration reference](https://developers.openai.com/codex/config-file/config-reference), [GPT-6 Astra model specification](https://developers.openai.com/api/docs/models/gpt-6-astra), [slash commands](https://developers.openai.com/codex/reference/slash-commands), [nobrainer-tech-flow](https://github.com/nobrainer-tech/nobrainer-tech-flow).
