# Cursor

Cursor supports OpenAI-compatible endpoints with a custom base URL.

1. Open **Cursor Settings -> Models**.
2. Under **OpenAI API Key**, paste your Talos key (`talos_...`).
3. Enable **Override OpenAI Base URL** and set it to:

   ```
   https://api.talos.ai/v1
   ```

   (In development: `http://localhost:8080/v1`.)

4. In the model list, add a custom model named exactly:

   ```
   talos-auto
   ```

   You can also add open models like `talos-llama-3.1-8b`.

5. Click **Verify**. Select `talos-auto` in the chat/model picker.

See [`talos.env`](./talos.env) for the three values above in one place to
copy from.

## Quick check

Run [`verify.sh`](./verify.sh) to confirm your key and the gateway work
before wiring up Cursor:

```bash
export TALOS_API_KEY=talos_YOUR_KEY
bash verify.sh
```

For a runnable client instead of curl, see [`openai_sdk.py`](./openai_sdk.py)
(same script as `examples/python/`).

Notes:

- Cursor sends OpenAI `chat/completions` requests; the gateway streams
  responses back in the same format.
- If Verify fails, confirm the key is active on your dashboard and the base URL
  ends with `/v1`.