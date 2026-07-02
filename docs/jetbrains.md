# JetBrains AI Assistant

JetBrains AI Assistant (IntelliJ IDEA, PyCharm, WebStorm, and the rest of the
JetBrains IDEs) supports custom OpenAI-compatible endpoints through its
third-party provider settings.

1. Open **Settings -> Tools -> AI Assistant -> Models**.
2. Under **Third-party AI providers**, add a custom OpenAI-compatible service.
3. Set:
   - **URL**: `https://api.talos.ai/v1`
   - **API key**: your Talos key (`talos_...`)
   - **Model name**: `talos-auto`
4. Apply, then pick the new provider in the AI Assistant chat model dropdown.

For local development, use `http://localhost:8080/v1` as the URL instead.

Notes:

- Some JetBrains versions place this under **Settings -> Tools -> AI
  Assistant -> Third-party AI providers** directly rather than under Models.
- If the connection test fails, confirm the URL ends with `/v1` and the key is
  active on your dashboard.