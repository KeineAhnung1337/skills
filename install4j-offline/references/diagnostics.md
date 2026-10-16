# Troubleshooting checklist

Start with project and compiler versions, failing media/OS, exact reproduction step, and first error (redacted). Identify the failing phase before changing settings:

| Symptom | Inspect locally |
| --- | --- |
| Compiler fails | Missing payload, source paths, variable values, incompatible project/compiler versions, script compilation, platform-specific media or JRE inputs. For a safe local reproduction consider `install4jc --verbose --test <project>`; verbose output can expose paths or variables, so redact it. |
| Installer will not start | Media type/architecture, bundled or discovered JRE, extracted executable permissions, supported OS, antivirus/quarantine, and local extraction space. |
| Screen or action fails | Order/conditions of screens and actions, variable initialization, Java custom code, privilege boundary, and the installer log. Compare GUI, console, and unattended behavior. |
| Payload or launcher fails | Distribution tree and Install files action, file associations, main class/module, classpath, VM parameters, JRE architecture, service account/permissions. Check installed files and launcher logs. |
| Upgrade/update or uninstall fails | Application identity, previously installed version, file ownership/overwrite rules, update source availability, locked files/services, uninstall actions and preserved user data. Test against disposable copies of real prior releases. |
| Signing or platform-specific build fails | Correct target platform, local signing prerequisites, timestamp/notarization network dependencies, and secrets handling. Don't weaken release signing merely to silence the failure. |

Generated installers normally produce an `i4j_log` in a temporary directory. If the project has an Install files action and completes successfully, the log can be copied to `<installation dir>/.install4j/installation.log`. For a controlled disposable test, `-Dinstall4j.log=<path>` saves it to an explicit path; `-Dinstall4j.keepLog=true` or `INSTALL4J_KEEP_LOG=true` can retain a temporary log. Check the **installed version's** local manual before using options because details may differ. Installer logs may contain user paths, variables, or sensitive data: keep local and redact.

Never execute an unfamiliar installer on the host just to obtain logs. First inspect project scripts and choose a disposable environment; if none is available, stop at static analysis and dry-run compilation and state the limitation.
