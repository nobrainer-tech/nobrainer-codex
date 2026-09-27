# NoBrainer Codex installer contract

SPEC_ID: nobrainer-codex-20260926
VERSION: 0.2.0
STATUS: IMPLEMENTING
OWNER: NoBrainer.Tech
APPROVAL: Owner's 2026-09-26 request for a Codex-capabilities-first public installer and page, the five nobrainer-tech-flow instructions, 15 ready subagents, catalog-backed context and reasoning visibility, with SSD migration optional.

## Outcome and scope

After cloning the public repo, one explicit `--apply` configures an existing signed-in Codex installation on Windows, macOS or Linux without changing the current model/effort, conversations, authentication or unrelated settings. `--check` previews the exact state and explains blockers; rerun is idempotent. A human-readable installation prompt supplies the URL and tells an agent to inspect and use the installer; it does not grant permission for SSD data movement or account changes.

SSD relocation is optional and separately authorized. It is a platform-specific process with an existing-volume/UUID gate, independent backup, atomic cutover, rollback and after-upgrade check. No cross-platform claim that the official desktop GUI is fail-closed without an actual supported launch gate. Do not follow symlinks to repair or delete unknown data.

## Requirements and acceptance

| ID | Requirement | Evidence |
|---|---|---|
| AC01 | Full Flow URL and owner's five nobrainer-tech-flow instructions installed byte-for-byte | `--check` and file readback |
| AC02 | `agents.max_concurrent_threads_per_session=15`, Luna default, no fixed worker effort | parse config after apply |
| AC03 | Selected model's local catalog ceiling applied when available; other models never falsely advertised at that ceiling | supported/unsupported catalog fixtures |
| AC03a | Preflight reports selected model's catalog reasoning levels and whether `max` is listed; it never changes selected effort or promises client support | catalog fixtures and readback |
| AC04 | User-selected model and effort unchanged, existing config sections/comments retained | original vs new config comparison |
| AC05 | CLI context visible via supported `tui.status_line`; desktop `/status` explained separately | parsed config + official docs |
| AC06 | Idempotent, atomic write and internal backup; malformed catalog fails before writes, while an unavailable catalog leaves the context setting unchanged | temp-home tests |
| AC07 | English-only public website leads with 15 configured slots, 1M+ GPT-6 API context clearly distinguished from the local Codex catalog, and MAX only where supported; the orchestration tree and optional before/after SSD illustration match the copy without implying Docker is required or savings are guaranteed | link/static checks + rendered mobile/desktop review |
| AC08 | SSD runbook differentiates data copy, actual runtime verification, owner cleanup gate and absent-volume failure | readback and isolated probe where possible |
| AC09 | One copy button copies the complete install prompt with an accessible result; optional `codex://` opens a registered app without claiming prompt prefill | local browser interaction and static checks |

## Brand typography

Match the rendered English homepage at https://nobrainer.tech/, checked on 2026-09-27, rather than an older generic Signature example. The shared product-page contract lives in `site/assets/brand-typography.css`, loaded after page styles. Keep this file identical in the Codex and Claude repositories.

- Font family: `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`; no downloaded display font. Actual system face varies by operating system.
- Hero heading: weight 700, size `clamp(54px, 6.15vw, 88px)`, line-height 1.02, letter-spacing -0.052em, word-spacing 0.025em.
- At 900px and below: size `clamp(56px, 8.5vw, 80px)`. At 580px and below: 56px, line-height 1.03, tracking -0.042em. At 360px and below: 52px.
- Header identity follows https://flow.nobrainer.tech/ (owner correction, 2026-09-27): system font, 21px, weight 750, line-height 1.65, tracking -1px, antialiased rendering. Keep 21px on mobile and move the identity to its own header row at 700px and below. Domain is cobalt; stem and product path use the main ink. The orange domain dot is a 4px square with margins 0 2px 0 1px, not a text period.
- The full identity links to `#top` on the current product page, with its full domain/path as the accessible name. Hover does not underline it; keyboard focus stays visible. A breadcrumb above the hero eyebrow links `nobrainer.tech` to the homepage and marks this product with `aria-current="page"`. Use 13px text, line-height 1.6, an 18px bottom gap and a slash separator with 10px spacing, matching Flow. No fabricated hierarchy or additional navigation destination.
- Preserve product-specific wording and wrapping. Verify computed heading styles against the live homepage at matching viewports, plus mobile overflow and copy controls. A matching font-family declaration alone is not visual parity.

## Owner gates and rollback

Installation writes only `AGENTS.md` and `config.toml` in an explicitly discovered Codex home. Backups under that same home are security-sensitive; no public commits of generated material. Restore via the manifest and rerun `--check`. SSD encryption, deletion and migration remain separate explicit approvals. No automatic remote installation, pushing, publishing or model substitutions. Repo/site release reads back URL and returned content. The actual macOS migration has its own private local ledger; the public repo does not copy it.
