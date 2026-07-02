"""A tiny fake Ollama server for local testing without a real model.

Implements just enough of the Ollama API for the worker:
  GET  /api/tags   -> advertises one model
  POST /api/chat   -> streams a canned NDJSON response

Run: python tests/fake_ollama.py [port]
"""
from __future__ import annotations

import asyncio
import json
import sys

from aiohttp import web

MODEL = "llama3.1:8b"


async def tags(_req):
    return web.json_response({"models": [{"name": MODEL}]})


async def chat(req):
    body = await req.json()
    prompt = " ".join(m.get("content", "") for m in body.get("messages", []))
    reply = f"[fake-{body.get('model')}] you said: {prompt[:60]}"

    resp = web.StreamResponse(status=200, headers={"Content-Type": "application/x-ndjson"})
    await resp.prepare(req)
    for word in reply.split(" "):
        chunk = {"message": {"role": "assistant", "content": word + " "}, "done": False}
        await resp.write((json.dumps(chunk) + "\n").encode())
        await asyncio.sleep(0.02)
    done = {
        "message": {"role": "assistant", "content": ""},
        "done": True,
        "prompt_eval_count": len(prompt.split()),
        "eval_count": len(reply.split()),
    }
    await resp.write((json.dumps(done) + "\n").encode())
    await resp.write_eof()
    return resp


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 11434
    app = web.Application()
    app.add_routes([web.get("/api/tags", tags), web.post("/api/chat", chat)])
    print(f"fake ollama on :{port}")
    web.run_app(app, host="127.0.0.1", port=port, print=None)


if __name__ == "__main__":
    main()