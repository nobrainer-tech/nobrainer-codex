# NoBrainer Codex installer contract

SPEC_ID: nobrainer-codex-20260926
VERSION: 0.2.0
STATUS: IMPLEMENTING
OWNER: NoBrainer.Tech
APPROVAL: Owner's 2026-09-26 request for a Codex-capabilities-first public installer and page, the five NoBrainer.Tech Flow instructions, 15 ready subagents, catalog-backed context and reasoning visibility, with SSD migration optional.

## Outcome and scope

After cloning the public repo, one explicit `--apply` configures an existing signed-in Codex installation on Windows, macOS or Linux without changing the current model/effort, conversations, authentication or unrelated settings. `--check` previews the exact state and explains blockers; rerun is idempotent. A human-readable installation prompt supplies the URL and tells an agent to inspect and use the installer; it does not grant permission for SSD data movement or account changes.

SSD relocation is optional and separately authorized. It is a platform-specific process with an existing-volume/UUID gate, independent backup, atomic cutover, rollback and after-upgrade check. No cross-platform claim that the official desktop GUI is fail-closed without an actual supported launch gate. Do not follow symlinks to repair or delete unknown data.

## Requirements and acceptance

| ID | Requirement | Evidence |
|---|---|---|
| AC01 | Full Flow URL and owner's five NoBrainer.Tech Flow instructions installed byte-for-byte | `--check` and file readback |
| AC02 | `agents.max_concurrent_threads_per_session=15`, Luna default, no fixed worker effort | parse config after apply |
| AC03 | Selected model's local catalog ceiling applied when available; other models never falsely advertised at that ceiling | supported/unsupported catalog fixtures |
| AC03a | Preflight reports selected model's catalog reasoning levels and whether `max` is listed; it never changes selected effort or promises client support | catalog fixtures and readback |
| AC04 | User-selected model and effort unchanged, existing config sections/comments retained | original vs new config comparison |
| AC05 | CLI context visible via supported `tui.status_line`; desktop `/status` explained separately | parsed config + official docs |
| AC06 | Idempotent, atomic write and internal backup; malformed catalog fails before writes, while an unavailable catalog leaves the context setting unchanged | temp-home tests |
| AC07 | English-only public website leads with supported Codex settings, context and delegation, shows updated hero/social graphics, and places SSD as an optional final section without invented savings or safety guarantees | link/static checks + rendered mobile/desktop review |
| AC08 | SSD runbook differentiates data copy, actual runtime verification, owner cleanup gate and absent-volume failure | readback and isolated probe where possible |

## Owner gates and rollback

Installation writes only `AGENTS.md` and `config.toml` in an explicitly discovered Codex home. Backups under that same home are security-sensitive; no public commits of generated material. Restore via the manifest and rerun `--check`. SSD encryption, deletion and migration remain separate explicit approvals. No automatic remote installation, pushing, publishing or model substitutions. Repo/site release reads back URL and returned content. The actual macOS migration has its own private local ledger; the public repo does not copy it.
