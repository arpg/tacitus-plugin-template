#!/usr/bin/env python3
"""
Plugin preprocessor.

Runs before the Claude invocation each scheduled tick. Reads any
per-plugin config + state, gathers new items relevant to this plugin,
and emits a JSON blob on stdout. The runner captures stdout to
`$EA_PLUGIN_DIR/state/last-collect.json`; the skill reads that file
during the Claude run.

Environment (set by run-plugin.sh):
  EA_PLUGIN_NAME  — short plugin name, e.g. "ff-watcher"
  EA_PLUGIN_DIR   — absolute path to the plugin directory
  EA_DIR          — absolute path to ~/.ea (for ledger access via helper)

Files (relative to $EA_PLUGIN_DIR):
  config.json     — plugin-specific user config (committed)
  .env.secrets    — KEY=VALUE secrets, gitignored, loaded into env by runner
  state/          — cursors, dedupe sets, last-seen IDs (gitignored)
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

PLUGIN_DIR = Path(os.environ.get("EA_PLUGIN_DIR", "."))
STATE_DIR = PLUGIN_DIR / "state"
CONFIG_PATH = PLUGIN_DIR / "config.json"


def main() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    config = json.loads(CONFIG_PATH.read_text()) if CONFIG_PATH.exists() else {}

    # TODO: implement the plugin's data-gathering logic here.
    # Return a JSON-serializable object the skill will reason about.
    output = {
        "generated_at": datetime.now().isoformat(),
        "plugin_name": os.environ.get("EA_PLUGIN_NAME", "REPLACE-ME"),
        "config_loaded": bool(config),
        "new_items": [],
        "monitor_health": "ok",
    }

    json.dump(output, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
