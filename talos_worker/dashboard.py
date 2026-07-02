"""Minimal local web dashboard for the worker.

Shows live status and lets the user change the power allocation. Runs in the
same asyncio loop as the WebSocket client.
"""
from __future__ import annotations

from aiohttp import web

from .state import RuntimeState

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Talos worker</title>
<style>
  :root { color-scheme: light; }
  body { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background:#c4bab0; color:#111; margin:0; padding:2rem; }
  .card { max-width: 40rem; margin: 0 auto; background:#fff; border:1px solid rgba(0,0,0,.15); padding:1.5rem; }
  h1 { letter-spacing:.2em; margin:0 0 1rem; }
  .row { display:flex; justify-content:space-between; padding:.4rem 0; border-bottom:1px solid rgba(0,0,0,.08); }
  .dot { display:inline-block; width:.6rem; height:.6rem; border-radius:50%; }
  .on { background:#1a7f37; } .off { background:#888; }
  input[type=range]{ width:100%; }
  button { background:#111; color:#c4bab0; border:0; padding:.6rem 1rem; text-transform:uppercase; letter-spacing:.1em; cursor:pointer; }
</style>
</head>
<body>
  <div class="card">
    <h1>TALOS WORKER</h1>
    <div class="row"><span>Status</span><span><span id="dot" class="dot off"></span> <span id="conn">...</span></span></div>
    <div class="row"><span>GPU</span><span id="gpu">-</span></div>
    <div class="row"><span>Models</span><span id="models">-</span></div>
    <div class="row"><span>Uptime</span><span id="uptime">-</span></div>
    <div class="row"><span>Jobs handled</span><span id="jobs">-</span></div>
    <div class="row"><span>Tokens served</span><span id="tokens">-</span></div>
    <div class="row"><span>Active jobs</span><span id="active">-</span></div>
    <div style="margin-top:1.5rem">
      <label>Power allocation: <strong id="allocLabel">50%</strong></label>
      <input id="alloc" type="range" min="0" max="100" value="50" />
      <button id="save">Save</button>
      <span id="saved" style="margin-left:.5rem;color:#1a7f37"></span>
    </div>
  </div>
<script>
async function refresh() {
  const s = await (await fetch('/api/status')).json();
  document.getElementById('conn').textContent = s.connected ? 'Connected' : 'Offline';
  document.getElementById('dot').className = 'dot ' + (s.connected ? 'on' : 'off');
  document.getElementById('gpu').textContent = s.gpu || 'CPU only';
  document.getElementById('models').textContent = (s.models || []).join(', ') || 'none';
  document.getElementById('uptime').textContent = s.uptimeSeconds + 's';
  document.getElementById('jobs').textContent = s.jobsHandled;
  document.getElementById('tokens').textContent = s.tokensServed;
  document.getElementById('active').textContent = s.jobsActive;
}
const alloc = document.getElementById('alloc');
const label = document.getElementById('allocLabel');
alloc.addEventListener('input', () => label.textContent = alloc.value + '%');
document.getElementById('save').addEventListener('click', async () => {
  await fetch('/api/allocation', { method:'POST', headers:{'content-type':'application/json'},
    body: JSON.stringify({ allocation: Number(alloc.value) / 100 }) });
  const el = document.getElementById('saved'); el.textContent = 'saved'; setTimeout(()=>el.textContent='',1500);
});
refresh(); setInterval(refresh, 2000);
</script>
</body>
</html>"""


def build_app(state: RuntimeState) -> web.Application:
    app = web.Application()

    async def index(_req):
        return web.Response(text=PAGE, content_type="text/html")

    async def status(_req):
        return web.json_response(state.snapshot())

    async def set_allocation(req):
        data = await req.json()
        alloc = float(data.get("allocation", state.allocation))
        state.allocation = max(0.0, min(1.0, alloc))
        return web.json_response({"allocation": state.allocation})

    app.add_routes(
        [
            web.get("/", index),
            web.get("/api/status", status),
            web.post("/api/allocation", set_allocation),
        ]
    )
    return app


async def start_dashboard(state: RuntimeState, port: int) -> web.AppRunner:
    runner = web.AppRunner(build_app(state))
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", port)
    await site.start()
    return runner