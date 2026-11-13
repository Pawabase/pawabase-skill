# Flows, routes, events, jobs, webhooks, and mail

Choose the mechanism by how work starts and whether a caller waits for a result:

| Need | Mechanism |
| --- | --- |
| Return a computed answer to an app | Named HTTP-triggered flow, custom route, or deployed function |
| React to a record/user/business event | Event subscription to a flow or channel |
| Run on a timer | Schedule starting a flow or emitting an event |
| Tell another service | Outbound signed webhook |
| Receive a partner event | Verified inbound hook |
| Run slow work | Background job or queued flow |
| Send email | Mail template and flow/mail action, with delivery log |

A flow is a sequence of blocks with inputs, branches, integrations, data access, and output. A route maps an HTTP method/path to a flow. In verified TypeScript 0.1.0, `pb.flows.run(name, input)` calls a named flow and `pb.routes` calls a custom route; `pb.functions.invoke(name, input)` calls a deployed function. Verify which form exists in the target environment. A route flow is addressed by its method/path rather than by the named-flow call.

Resource writes emit `<table>.created`, `.updated`, and `.deleted`. Event subscriptions connect those events to flows or channel publishes. Schedules create clock-driven work. Inbound hooks verify a source before emitting/starting work; outbound webhooks sign payloads and retain deliveries. Read webhook signature configuration before implementing a receiver. Events and reactions are at least once and do not have fixed order. Make handlers idempotent, especially payment, mail, and external mutation steps.

Retry policies differ: flow steps, background jobs, outbound webhooks, and mail do not share one retry count. A caller's POST can time out after server work succeeded; do not enable idempotent retry on a charge/email without an application idempotency key and duplicate detection. Inspect Activity's event, flow run, job, and webhook delivery records independently. Failed jobs may be retried or replayed after diagnosis.

The Python 0.2.0 kit adds author/test/emulate/deploy functions, distinct from visual flows. It exposes `invoke_function`, `invoke_flow`, `emit_event`, and related flat client methods. The product docs may describe newer SDK namespaces; check the installed version. Read `logic/flows.mdx`, `logic/routes.mdx`, `automation/events.mdx`, `automation/jobs.mdx`, `automation/webhooks.mdx`, `automation/webhook-signatures.mdx`, `automation/reliability.mdx`, and `mail/overview.mdx` in the docs repo.
