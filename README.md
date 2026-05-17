# ea-plugin-template

Template repo for personal EA plugins (companion to
[`ea-system`](https://github.com/crheckman/ea-system)). Plugins run on
their own cron schedule, with their own context, logs, and Slack output
channel — and can be added or removed without touching EA core.

Architecture details: `crh/ea-system:docs/plugin-architecture.md`.

## Bootstrapping a new plugin

```bash
gh repo create <owner>/ea-plugin-<short-name> \
    --template <owner>/ea-plugin-template \
    --private \
    --clone ~/.ea/plugins/<short-name>
```

Then in `~/.ea/plugins/<short-name>/`:

1. Edit `plugin.json` — set `name`, `schedule`, `context.*` grants,
   `output.channel_key`, `output.format_anchors`. Flip `enabled` to
   `true` once you're ready for it to run.
2. Edit `collect.py` — implement the preprocessor.
3. Edit `skill.md` — write the Claude prompt.
4. (optional) Create `config.json` for plugin-specific user config.
5. (optional) Create `.env.secrets` for API keys etc. (gitignored).
6. `git add -A && git commit -m "Initial implementation" && git push`
7. On the EA host: `setup.sh` to register the cron entry.

## Files

| File | Committed? | Purpose |
|---|---|---|
| `plugin.json` | yes | manifest: schedule, context grants, output route |
| `collect.py` | yes | preprocessor; emits JSON for the skill |
| `skill.md` | yes | Claude prompt for the plugin's run |
| `config.json` | yes | plugin user config (e.g. watchlists) |
| `README.md` | yes | this file |
| `.gitignore` | yes | excludes `state/`, `.env.secrets`, `__pycache__/` |
| `.env.secrets` | no | API keys etc., per-machine |
| `state/` | no | runtime state (cursors, dedupe), per-machine |

## Conventions

- **Single-user, private repo.** Don't worry about contributor docs.
- **Branch**: `main`. No PR ceremony.
- **Secrets**: `.env.secrets` only. Re-supplied per machine; never pushed.
- **Ledger writes**: use `ea_plugins.ledger`. IDs start with plugin name
  prefix. The helper auto-sets `source = 'plugin:<name>'`.
- **Failures are isolated.** If `collect.py` or the Claude run fails,
  only this plugin's log and its own Slack channel see it. EA core
  (email, calendar, work briefings) is unaffected.
