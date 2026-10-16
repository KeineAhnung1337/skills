# Scripts and variables

QF-Test embeds scripting nodes in suites; it is not normally a test framework driven wholly by Python. Prefer native nodes for events and checks. **Server script** executes inside QF-Test; **SUT script** executes inside the application's process, has client context, and can access live GUI objects. Interpreters do not share globals across server/SUT or across SUT clients. Use a QF-Test variable or explicit transfer for data exchange. Avoid long-running procedures called from an SUT script; event-thread deadlocks are possible.

The `rc` run context is available in script nodes. Documented methods include `rc.getStr("name")`, `rc.getBool("name")`, `rc.getInt("name")`, `rc.getObj("name")`, `rc.setLocal("name", value)`, `rc.setGlobal("name", value)`, `rc.logMessage(text)`, `rc.logWarning(text)`, `rc.logError(text)`, `rc.check(condition, message)`, `rc.checkEqual(actual, expected, message)`, and `rc.callProcedure("package.procedure", parameters)`. SUT scripts can use `rc.getComponent("componentId")`. Verify signatures, parameter behavior, error levels, and language syntax in the installed `tech_scripting_rc.html` reference.

Jython is **2.7**, not CPython 3: no f-strings, annotations, or Python-3-only libraries. Avoid interpolating QF-Test `$(var)` references into Jython string literals (quotes, backslashes and newlines may break scripts); use `rc.getStr("var")`. Script expressions in attributes include `$[Jython expression]`, `${groovy:expression}`, `${javascript:expression}`; conditions in some nodes accept expressions directly. Check the node and its configured language before changing one.

Minimal conceptual patterns (use within a script node, not as a standalone `.qft` file):

```python
# Jython Server script; the value is safely read at execution time.
actual = rc.getStr("status")
rc.checkEqual(actual, "Ready", "Application reports Ready")
```

```python
# Jython SUT script; only when a recorded component must be inspected directly.
field = rc.getComponent("tfUsername")
rc.setGlobal("usernameLength", len(field.getText()))
```

The second snippet assumes a Java component exposing `getText()` and an existing ID `tfUsername`; it is **not** portable to every engine or application. `rc.check` is not a substitute for a normal check node when that node can express the requirement. For advanced use read the installed manual's “Scripting” and “Advanced scripting” sections, including `rc`, `qf`, thread-affinity rules, and script-language-specific pages.
