# ea-plugin-template

The skeleton for an EA plugin: one directory with a `plugin.json` (manifest
v2) at its root. A plugin adds a capability to the EA without code in EA
core, and it lives in its own repo. The full guide is `docs/plugins.md` in
the ea-system repo.

## A new plugin

```bash
gh repo create <owner>/ea-plugin-<name> --template <owner>/ea-plugin-template \
    --private --clone
cd ea-plugin-<name>
```

1. Edit `plugin.json`: set `name` (lowercase letters, digits and hyphens),
   `description`, the `schedules`, `output.channel_key` and
   `output.format_anchors`. Add the capabilities the plugin needs (see
   below).
2. Implement `collect.py` (it prints the JSON the skill reads) and write
   `skill.md`.
3. Commit and push.
4. On the EA host, as the owner:

   ```bash
   python3 scripts/ea-plugin.py install git:git@github.com:<owner>/ea-plugin-<name>.git
   ```

   It prints the capabilities. Read them, then run it again with
   `--accept-capabilities` (a source on the owner's `trusted_sources` skips
   that step unless the plugin runs code as the owner).
5. Add the cron line that `run-plugin.sh --check-schedules` reports as
   missing. Restart the chat bot if the plugin has a chat trigger or a card.

Updates: push, then `ea-plugin.py update <name>`. A changed capability
asks for consent again.

## Capabilities

All of them sit under `capabilities` in `plugin.json`:

| Key | What it adds |
|---|---|
| `schedules` | cron passes; `llm` is `claude`, `remote-first`, `remote` or `none` (`collect.py` writes the post as `post`) |
| `chat` | a chat trigger: `{"skill", "keywords", "patterns"}` |
| `tools` / `denied_tools` | agent tool grants (each must name `{plugin_dir}`) and denials |
| `cards` | confirmation cards: a pending file, the wording, and an executor that runs on approve |
| `mail_rules` | closure senders, excluded senders, keep-from-Anthropic domains |
| `network` | internet hosts (listed for consent) and local endpoints for the resident's allowlist |
| `secrets` | the secret names the plugin reads from `.env.secrets` |
| `owner_hooks` | owner zone only: mediated verbs, Graph auth sources, owner cron jobs |
| `claude_plugin` | a Claude Code plugin root loaded into agent sessions |

Set `"zone": "owner"` only for a plugin that needs the owner's tokens. Its
code then runs as the owner from the owner's private directory, and every
install and update needs explicit consent.

## Files

| File | In git | Purpose |
|---|---|---|
| `plugin.json` | yes | the manifest |
| `collect.py` | yes | the preprocessor; prints JSON for the skill |
| `skill.md` | yes | the prompt for the scheduled pass |
| `config.json` | yes | plugin settings (optional) |
| `.env.secrets` | no | secrets, per machine |
| `state/` | no | runtime state, per machine |

## Conventions

- A private repo, branch `main`.
- Secrets live in `.env.secrets` only, re-supplied per machine.
- Ledger writes go through `ea_plugins.ledger`; row ids start with the
  plugin name, and the helper sets `source = 'plugin:<name>'`.
- A failed run reaches only this plugin's log and channel.
