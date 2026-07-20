# objection - Runtime Mobile Exploration (Patched for Frida Gadget Transport)

`objection` is a runtime mobile exploration toolkit, powered by [Frida](https://frida.re/).

This fork patches objection v1.12.5 to fix **silent RPC export failure** when
connecting via Frida gadget transport (the `-g` flag) — the webpack emoji header
(`📦`, `✄`) in `agent.js` causes Frida V8 to drop all RPC exports even though
`create_script()`/`load()` succeed. Works on **Android 14** / **arm64-v8a**.

## Versions

| Component | Version |
|---|---|
| objection | 1.12.5 |
| Frida | 17.16.2 |
| frida-tools | 14.5.0 |
| Python | 3.13+ |
| Node.js (for building agent) | 20.x |

## Patches

1. **Webpack header strip** — `_get_agent_source()` strips the emoji banner
   so Frida V8 doesn't silently fail on RPC registration.
2. **Bootstrap fallback** — if the 857 KB agent.js fails transport, objection
   ADB-pushes a clean copy to `/data/local/tmp/agent.js` and loads it via
   `NativeFunction` syscalls (`open`/`read`/`lseek`/`close`).
3. **Catch widening** — catches `frida.InvalidArgumentError` alongside
   `TransportError` so `"malformed package"` triggers the bootstrap fallback.
4. **`identifier()` NaN fix** — `Number(Math.random().toString(36).substring(2,8))`
   → `Math.floor(Math.random() * 1e9)` (the old code could return `NaN` under
   Frida V8 strict mode, destroying job tracking).
5. **`normalizePattern()`** — converts `Class.method` → `Class!method` dot syntax
   for `search` and `watch` commands at the JS level.
6. **HackTricks tutorial syntax** — `android hooking search methods <pkg> <class>`
   and `android hooking watch class <class-name>` now work correctly.
   Multi-dot class names (e.g. `asvid.github.io.fridaapp.MainActivity`) are not
   mangled.

## Install

```bash
# Install all three components at pinned versions (objection 1.12.5, Frida 17.16.2, frida-tools 14.5.0)
pip install https://github.com/Aceproulx/objection/releases/download/v1.12.5-fixed/objection-1.12.5-py3-none-any.whl && pip install frida==17.16.2 frida-tools==14.5.0

# Verify
objection --version
```

## Usage

### 1. Patch your APK with Frida gadget

```bash
# Patch the APK to embed Frida gadget
objection patchapk -s app-release.apk

# Install the patched APK on device
adb install app-release.objection.apk
```

### 2. Launch the app on device and explore

```bash
# Attach by process name (recommended)
objection -n FridaApp explore

# Or connect via gadget (uses the gadget name from patchapk config)
objection -g apk explore
```

### 3. Commands inside the objection REPL

```
[usb] # env
[usb] # ping
[usb] # android hooking search classes asvid.github.io.fridaapp
[usb] # android hooking search methods asvid.github.io.fridaapp.MainActivity
[usb] # android hooking watch class asvid.github.io.fridaapp.MainActivity
[usb] # android hooking list classes
[usb] # android sslpinning disable
[usb] # android root disable
[usb] # memory list modules
```

### HackTricks tutorial syntax (these now work)

```
android hooking search methods asvid.github.io.fridaapp MainActivity
android hooking search classes asvid.github.io.fridaapp
android hooking watch class asvid.github.io.fridaapp.MainActivity
android hooking watch class_method com.example.app.util.NetUtilKt.getUUID
```

From [HackTricks - objection](https://book.hacktricks.wiki/en/mobile-pentesting/android/objection-tutorial/index.html).

## Build from source

```bash
git clone https://github.com/Aceproulx/objection.git
cd objection/agent
npm install && npm run build
cd ..
pip install build
python -m build --wheel .
pip install dist/objection-1.12.5-py3-none-any.whl
```

## License

GNU General Public License v3.0.
