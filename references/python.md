# Python client and function kit

The verified `pawabase` 0.2.0 wheel requires Python 3.11+ and `httpx`. It provides a flat synchronous/async client plus function authoring, local emulation, testing, and deployment. It does **not** provide the `pb.auth`, `pb.from_`, `pb.realtime`, `pb.storage`, `pb.ai`, and `pb.manage` namespaces shown in some newer product docs. The current runtime inventory says functions are not a current product area, so verify that the target deployment accepts function routes before using this kit for new server logic. Check `pawabase.__version__` and `dir(Pawabase)` before adapting a docs example.

```python
from pawabase import Pawabase

with Pawabase(url, secret_key, project="acme", environment="production") as pb:
    orders = pb.list("orders", sort="-created_at", limit=20)
    order = pb.create("orders", {"total": 12.5})
    result = pb.invoke_function("hello", {"name": "Ada"})
```

The verified client also has `get`, `update`, `delete`, `invoke_flow`, `emit_event`, `events`, deployment and function inspection methods. `AsyncPawabase` has the same surface with awaited calls. Use context managers to close connections. `PawabaseError` exposes status/code/message and `problems`; inspect the installed class for exact field names. Always specify the environment: the current Python client defaults to `development` and a key from another environment can be refused.

The newer docs may be correct for a different release. When a needed namespace is absent, use a verified HTTP endpoint through the client's `request` method or `httpx`, preserving `apikey` and the user bearer token. For user-facing server calls, use a publishable key and the actual user token so policies apply. Keep a secret key for server-only administration.

## Custom functions

```python
from pawabase.functions import FunctionError, function

@function("hello", policy="public", input_fields=[{"name": "name", "type": "string"}])
async def hello(ctx):
    name = ctx.input.get("name") or "world"
    if not isinstance(name, str):
        raise FunctionError("Invalid name", status=422, code="invalid_name")
    ctx.log("greeting", name=name)
    return {"message": f"Hello, {name}!"}
```

`FakeRuntime` and `call` from `pawabase.testing` run a function in tests without a server and record side effects. The function context can use `ctx.runtime` for data, events, mail, HTTP, and storage according to the installed kit. Test the actual side effect or error behavior, not merely the decorator.

For a compatible function deployment, the kit's CLI sequence is `pawabase init`, `pawabase link`, set `PAWABASE_URL` and `PAWABASE_API_KEY` in local secrets, `pawabase test`, `pawabase emulate --watch`, then `pawabase deploy`. `pawabase.toml` holds project/environment, never the key. `deploy --dry-run` previews; `invoke`, `trigger`, `functions`, `deployments`, `rollback`, `branches`, and `logs` cover operation. This is **not** the `pawabase-iac` deployment workflow even though both use a `pawabase` executable. Read the installed CLI's `--help` before using flags in automation.
