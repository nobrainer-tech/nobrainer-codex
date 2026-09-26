# External SSD: supported paths and verification

Data migration is deliberately separate from `install.py`. It depends on the host OS, browser/desktop permission model, encryption key handling and independent backups. A one-command universal SSD move would be unsafe.

## Preflight

1. Confirm the real running executable, client-selected model/effort, process parent, `CODEX_HOME`, `CODEX_SQLITE_HOME`, open files, app support/cache and destination mount identity. On macOS use `diskutil info` plus `lsof`; on Linux use `findmnt` and `/proc/<pid>/fd`; on Windows use PowerShell `Get-Volume` and process/file-handle inspection. If tools are missing, stop rather than claim independence.
2. Inspect free bytes on the data volume, destination space, encryption state, hardware/SMART availability and any filesystem warning. A healthy fsck is not a hardware-life test. If filesystem checks disagree, investigate offline without unmounting beneath the operator; repeat only after a causal change.
3. Inventory Git remotes and dirty/untracked/ignored worktrees. GitHub only covers confirmed remote objects, not Codex conversations, credentials, database volumes or local work. Back up the rest on independent storage. Keep credentials outside the public repo; use a private recovery method for the encryption passphrase.
4. Determine who uses the original Codex home. Do not move its root while an independent gateway or other process holds an open coordination DB there. On this Mac, opencodex uses an internal `~/.codex` file and cannot depend on an absent external drive.

## Cutover and proof

1. Record exact sources, destinations, timestamps, running containers/ports/restart policies, symlink targets and rollback paths. Prepare application-consistent SQLite backups, PostgreSQL logical dumps or cleanly stopped volume copies; prove at least one isolated restore. Do not tar active PostgreSQL files.
2. Read local copy-tool docs before choosing flags. Preserve symlinks, ownership, ACL, xattrs and sparse VM images where possible. Full-file checksums and path inventories, not mtimes, establish content parity. Treat timeout, short copy or socket file as incomplete.
3. Prove the operator continues after closing GUI. Gracefully close GUI/app-server, stop VM and other writers, perform final copy, compare, then atomically switch only known paths. Keep originals under dated rollback names. Do not use `docker system prune`, `colima delete`, volume removal or reset a database.
4. Start exactly the previously running containers. Mount every real target of Docker bind paths in the guest, including worktrees that became symlinks. Verify volume hashes/DB queries/health, ports, Docker context/socket, open VM images, CLI login, GUI account, existing active and archived conversations, manually selected models and worktrees. Do not send a test turn into an owner's conversation.
5. Protect startup without the SSD: detect the correct UUID and unlocked encrypted volume **before** writing. Test a missing-drive simulation for every entry point, including the actual official Dock/start-menu icon and auto-start jobs. On platforms where an official launcher cannot be intercepted safely, do not claim fail-closed behavior; choose a guarded launcher or obtain a vendor-supported solution. Never change the signed app bundle or turn off platform security.
6. Finish encryption (not just start it), keep secrets in a local password manager outside the disk, and retain all source originals until the owner confirms GUI behavior and independent backups are proven. Measure reclaimed physical space with `df`/volume free bytes only after approved cleanup.

## Restore

Stop new GUI/VM writers; verify the rollback manifest, reverse only the exact atomic path switches, restore original service policies and start precisely the original running set. Recheck login, one session, both databases and the official app. Retain the original internal archive of older conversations. If the SSD is unavailable, preserve the originals and notify the owner; do not generate a fresh empty profile.

This procedure is a portable decision/verification contract. Platform-specific file operations require a separate implementation and real-host tests; no script here silently migrates the machine.
