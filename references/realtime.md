# Realtime

Realtime channels use names such as `chat:lobby`, `order:42`, or `resource:tasks`. A Studio channel rule matches the name and separately controls subscribe, publish, presence, history, and limits. Authentication uses the environment key and, when applicable, the user's access token. A private channel's history is not public just because a URL exists.

## Verified TypeScript 0.1.0

```ts
const room = pb.realtime.channel<{ text: string }>("chat:lobby", {
  presence: { name: "Ada" }, replay: 50,
});
const stop = room.onEvent("message", ({ payload, from }) => render(from, payload.text));
await room.subscribe();
await room.send("message", { text: "hello" });
await room.track({ name: "Ada" });
const recent = await room.history(50);
stop();
await room.unsubscribe();
```

The client opens a WebSocket on first subscription, heartbeats, reconnects with backoff, rejoins channels, and replays bounded history when requested. It updates an open socket after token refresh. `on("message")` gets every channel message, while `onEvent(name)` filters the event. The sender also receives its message; render delivered messages and deduplicate by id. Check `realtime.status` and `onStatusChange` to show reconnect state. The verified 0.1.0 SDK also has HTTP `publish`, `presence`, and `history` methods, but no `stream`/SSE method; raw SSE may be used against a verified deployment. On older Node without global WebSocket, inject one in realtime options.

## Wire and other languages

The public OpenAPI snapshot includes `POST /realtime/v1/publish`, `GET /realtime/v1/channels/{channel}/history`, `GET /realtime/v1/channels/{channel}/presence`, and `GET /realtime/v1/sse`. WebSocket is the full duplex protocol; SSE is listen only and publishing remains an HTTP call. The docs list MQTT, MQTT over WebSocket, HTTP streaming, and long polling as unavailable. Inspect target OpenAPI and realtime connection docs for precise parameters, frame shapes, and limits. The verified Python 0.2.0 wheel has no realtime namespace; use a compatible newer client or the wire protocol.

## Live records, presence, and history

Enable a resource's **Broadcast changes** setting, then subscribe to `resource:<table>` for `created`, `updated`, and `deleted` events containing `payload.record`. Changes made outside the API need the separate capture setting. Row read rules decide who receives each change; apps cannot publish to `resource:` channels. A presence-enabled rule exposes members and join/leave changes; presence metadata should not contain secrets.

Ephemeral channels do not preserve disconnected messages. History depth holds a bounded backlog; durable channels store messages until retention expires. Replay is bounded by that backlog. For chat, subscribe, load history, deduplicate by id, and keep durable messages as records if they must remain available. For a live list, merge by record id and reload records after a possible gap. Use Studio's Realtime Playground, Connections, and Activity to diagnose key, rule, connection, and history failures.

Current docs also describe **live queries** that rerun a filtered result when records change. The checked TypeScript 0.1.0 and Python 0.2.0 packages do not expose the documented live-query method. Before choosing it, verify both target deployment and installed SDK; otherwise use record-change subscriptions plus a refetch. For listen-only dashboards, use SSE where the target supports it. For collaborative cursors or typing, use ephemeral channel events/presence and avoid writing every movement to a durable table. See `realtime/record-changes.mdx` and `realtime/patterns.mdx`.

For the first live-list load, avoid a read/subscribe gap: subscribe before trusting the initial list, then read or refetch immediately after subscribing. On reconnect, deduplicate by id and refetch when history may not cover the disconnection. A live query, when supported, handles this differently by returning the whole filtered result again; check its `limit` and per-client resource cost.
