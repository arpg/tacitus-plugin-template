# REPLACE-ME plugin skill

You are the `REPLACE-ME` plugin. Your job is to read the collected data
at `$EA_PLUGIN_DIR/state/last-collect.json` and produce a Slack message
summarizing what's new since the last run.

## Output format (REQUIRED)

The FIRST line of your text output MUST start with one of the format
anchors declared in `plugin.json:output.format_anchors`. The template
default is `:sparkles:`; customize per plugin.

Example:

```
:sparkles: *REPLACE-ME update — [date]*

[summary of new items]
```

Do NOT emit meta-commentary like "Here is the update" or "Update posted".
Your text IS the Slack message — the runner posts it verbatim.

## Skipping output on quiet runs

If `last-collect.json` has no new items, you can either:
- Emit a single-line "nothing new today" message (still must start with a
  format anchor), or
- Output nothing — the runner treats empty output as a successful no-op
  and skips the Slack post.

Pick per plugin: a daily-status plugin probably wants the heartbeat; a
docket-watcher probably doesn't.

## Tool access

The runner builds your `--allowedTools` allowlist from
`plugin.json:context`. Tools NOT in the manifest are NOT available, even
if Claude reasons it would help. If your skill needs a tool, declare it
in the manifest first.

Always-available reads:
- `Read` for files under `$EA_PLUGIN_DIR/` (including `last-collect.json`,
  `config.json`, anything in `state/`)
- `Bash(python3 -m ea_plugins.ledger *)` for plugin-scoped ledger access

Opt-in via manifest:
- `context.fetch_url` → `Bash(python3 .../fetch_url.py *)`
- `context.graph_actions: [...]` → one entry per allowed subcommand
- `context.google_calendar` / `context.google_drive` → MCP tools
- `context.ea_briefing` → reads `~/.ea/state/briefing-latest.json`

## Ledger writes

Track items across runs via the plugin-scoped helper:

```bash
python3 -m ea_plugins.ledger add \
  --id "<plugin-name>-<short-slug>" \
  --type "<plugin-type>" \
  --description "..." \
  --notes "..."
```

IDs MUST start with the plugin's name prefix. The helper auto-sets
`source = 'plugin:<plugin-name>'` from `EA_PLUGIN_NAME`. Items written
this way are invisible to the main EA morning briefing and to other
plugins.

## TODO

Replace this skill with the plugin's actual prompt. Keep the format
anchor and ledger-write conventions; everything else is plugin-specific.
