# HackTricks Objection Tutorial — Command Reference

This page collects the commands from the [HackTricks Objection Tutorial](https://hacktricks.wiki/en/mobile-pentesting/android-app-pentesting/frida-tutorial/objection-tutorial/)
that are now tested and working with the patched objection wheel (v1.12.5-fixed).

`console.log()` works inside the objection REPL — no need to use `send()`.

Tested on: **Android 14 (SDK 34), arm64-v8a, Frida gadget 17.16.2, frida-tools 14.5.0**

---

## Connect

```bash
# Attach by process name (recommended)
objection -n asvid.github.io.fridaapp start

# Or via gadget (non-rooted device)
objection patchapk -s app-release.apk --network-security-config --enable-debug
adb install -r app-release.objection.apk
objection -n Gadget start
```

## Environment & Info

```
env
frida
ping
```

## File Operations

```
file download <remote path> [<local path>]
file upload <local path> [<remote path>]
```

## Loading custom Frida scripts

Scripts can use `console.log()` — output is shown in both the objection REPL and Frida CLI.

### Via objection REPL (evaluate)

```
evaluate hook.js
```

### Via Frida CLI + adb forward (gadget mode)

```bash
# In a separate terminal, forward the port
adb forward tcp:27042 tcp:27042

# Load script on attach
frida -H 127.0.0.1:27042 Gadget -l hook.js

# Or load it after attaching, inside the Frida CLI:
#   %load hook.js
```

### Via startup script

```bash
objection -n asvid.github.io.fridaapp start --startup-script hook.js
```

### Via import (objection REPL — separate session, may fail in gadget mode)

```
import hook.js
```

## Jobs

```
import ssl-bypass.js "ssl-bypass"
jobs list
jobs kill <job_id>
```

## SSL Pinning & Root Detection

```
android sslpinning disable
android root disable
android root simulate
android shell_exec whoami
```

## Screenshots & UI

```
android ui screenshot /tmp/screenshot
android ui FLAG_SECURE false
```

## Proxy & Deoptimize

```
android proxy set 192.168.1.10 8080
android deoptimize
android intent implicit_intents --dump-backtrace
```

## Static Analysis (Dynamic)

```
android hooking list activities
android hooking list services
android hooking list receivers
android hooking get current_activity
```

## Search Classes & Methods

```
android hooking search classes asvid.github.io.fridaapp
android hooking search methods asvid.github.io.fridaapp MainActivity
android hooking list class_methods asvid.github.io.fridaapp.MainActivity
android hooking list classes
android hooking list class_loaders
```

## Hooking

```bash
# Hook a single method with all options
android hooking watch class_method asvid.github.io.fridaapp.MainActivity.sum --dump-args --dump-backtrace --dump-return

# Hook an entire class
android hooking watch class asvid.github.io.fridaapp.MainActivity --dump-args --dump-return

# Change boolean return value
android hooking set return_value asvid.github.io.fridaapp.MainActivity.checkPin true
```

## Heap / Class Instances

```
android heap search instances <class>
android heap print fields <hashcode>
android heap print methods <hashcode> --without-arguments
android heap execute <hashcode> <method> --return-string
android heap evaluate <hashcode>
```

## Keystore & Intents

```
android keystore list
android intent launch_activity
android intent launch_service
```

## Memory

```
memory dump all <local destination>
memory dump from_base <base_address> <size> <local destination>
memory list modules
memory list exports libfoo.so
memory list exports libfoo.so --json exports.json
memory search "<pattern eg: 41 41 41 ?? 41>" (--string) (--offsets-only)
memory write "<address>" "<pattern eg: 41 41 41 41>" (--string)
```

## SQLite

```
sqlite connect /data/data/<package>/databases/app.db
sqlite connect /data/data/<package>/databases/app.db --sync
```

## Early Instrumentation

```bash
# Run a command immediately on attach
objection -n asvid.github.io.fridaapp start --startup-command "android sslpinning disable"

# Run a script immediately on attach
objection -n asvid.github.io.fridaapp start --startup-script ssl-bypass.js
```

## Exit

```
exit
```

## Patched Syntax (Fixes in this fork)

These command patterns were broken in upstream objection due to the webpack emoji
header issue and `normalizePattern` manging multi-dot class names. They now work:

```
# HackTricks multi-arg syntax
android hooking search methods asvid.github.io.fridaapp MainActivity
android hooking search classes asvid.github.io.fridaapp

# Class watch (dot-syntax class name)
android hooking watch class asvid.github.io.fridaapp.MainActivity

# Class method watch (dot-syntax class.method)
android hooking watch class_method asvid.github.io.fridaapp.MainActivity.sum
```

## Source

- <https://github.com/Aceproulx/objection>
- <https://github.com/sensepost/objection>
- <https://hacktricks.wiki/>
