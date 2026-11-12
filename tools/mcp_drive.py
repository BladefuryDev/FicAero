"""Drive the Craft Anything MCP server over stdio for one job.

Usage: python -u mcp_drive.py calls.json [extra server args...]

calls.json is a list of {"tool": name, "args": {...}} run in order inside ONE
server session, so the private browser that web_site_open starts stays open
for the capture tools that follow. The server is started with --allow-run for
this process only; the Claude Code registration is left untouched.

Each result is printed as one JSON line; screenshot base64 is replaced by its
length so the output stays readable.
"""
import json
import subprocess
import sys

CLI = r"C:\Program Files\Craft Anything\craft-anything-cli.exe"


def trim(o):
    """Replace big base64 strings with their length."""
    if isinstance(o, dict):
        return {k: ("<%d chars>" % len(v)) if k in ("base64", "png_base64") and isinstance(v, str) else trim(v)
                for k, v in o.items()}
    if isinstance(o, list):
        return [trim(x) for x in o]
    return o


def main():
    calls = json.load(open(sys.argv[1], encoding="utf-8"))
    extra = sys.argv[2:]
    proc = subprocess.Popen([CLI, "mcp", "--allow-run", *extra], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            text=True, encoding="utf-8", bufsize=1)
    counter = [0]

    def send(method, params=None, notify=False):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        if not notify:
            counter[0] += 1
            msg["id"] = counter[0]
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()
        if notify:
            return None
        while True:
            line = proc.stdout.readline()
            if not line:
                raise SystemExit("server closed")
            m = json.loads(line)
            if m.get("id") == counter[0]:
                return m

    send("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                        "clientInfo": {"name": "ffnet-drive", "version": "0"}})
    send("notifications/initialized", notify=True)
    for c in calls:
        r = send("tools/call", {"name": c["tool"], "arguments": c.get("args", {})})
        out = r.get("result", r.get("error"))
        shown = out
        if isinstance(out, dict) and "content" in out:
            txt = "\n".join(p.get("text", "") for p in out["content"] if p.get("type") == "text")
            try:
                shown = json.loads(txt)
            except Exception:
                shown = txt
        print(json.dumps({"tool": c["tool"], "result": trim(shown)}, ensure_ascii=False), flush=True)
    proc.stdin.close()
    proc.wait(timeout=30)


if __name__ == "__main__":
    main()
