# QF-Test 11.0 offline skill

Copy this entire `qftest/` directory to `.opencode/skills/qftest/` in a project, or to `~/.config/opencode/skills/qftest/` for your user. Then mention `@qftest` or ask OpenCode to work on a QF-Test suite. The skill ID is the directory name (`qftest`). Keep the `references/` and `scripts/` folders beside `SKILL.md`.

This package has **no network or third-party Python dependencies**. The model runtime must be configured to use a local model separately; a locally stored skill does not make a cloud model offline. QF-Test, a valid license, and the application under test are needed for execution. Localhost MCP is optional, not a network dependency on the internet.

The original notes here cover practical workflows, not every QF-Test node or attribute. On the offline machine, use the version-matched vendor manual shipped with QF-Test at `<QFTEST_HOME>/doc/manual/en/contents.html` (and the installed tutorial, reference, and demo suites). If your licensing/redistribution terms allow, stage the locally installed manual **before** copying this folder:

```sh
python3 qftest/scripts/stage_manual.py /path/to/qftest-11.0.0/doc/manual/en --authorized-to-copy
```

This copies to `qftest/vendor-docs/manual/en/` without downloading anything. It refuses to replace an existing destination. You can also copy permitted tutorial and demo folders yourself. This package does not ship vendor documentation by default. Never mix reference examples from a later release into an 11.0.0 suite without checking the 11.0.0 installation.

For OpenCode V2 and a QF-Test 11.0 MCP server running locally, optionally add the following to the *offline machine's* `opencode.jsonc` (not required for the skill):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "qftest": {
        "type": "remote",
        "url": "http://127.0.0.1:5543/mcp"
      }
    }
  }
}
```

QF-Test's own online manual currently describes a later 11.0 patch release; the installed 11.0.0 manual wins for this package. This package contains no example `.qft` file because creating a plausible-looking but unverified suite would be unsafe. Start from QF-Test's installed example suites or record a minimal case with your actual SUT.
