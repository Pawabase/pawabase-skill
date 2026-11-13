# Authentication, keys, and access rules

## Request identity

Every request supplies `apikey`. A signed-in user also supplies `Authorization: Bearer <access_token>`. The gateway validates key ownership, expiration, allowed origins/IPs/routes, scopes, rate limits, and quotas. The server then resolves the user, roles, organization, assurance level, and policy facts. A publishable `pb_pk_` key can live in a browser or mobile app; it is subject to access rules. A `pb_sk_` secret key bypasses rules and may carry management scopes. Never put one in a client bundle. Each key belongs to one environment.

Scopes use `family:read`, `family:write`, or `family:*` (and `*` for all). Application families include `data`, `storage`, `auth`, `flows`, `ai`, and `realtime`. Management families such as `resources`, `users`, `keys`, `secrets`, `backups`, and `monitoring` require secret keys. No scopes means the key is not narrowed by scope; rules and key type still matter. Read `reference/keys-and-security.mdx` in the docs repo for the full scope map.

## Sessions and sign-in

Auth can support email/password, links/codes, social/company login, passkeys, MFA, sessions, devices, guest users, roles, organizations, invitations, and machine identities. Their availability depends on environment configuration and client version. In the verified TypeScript 0.1.0 client, `auth.signInWithPassword` may return `mfa_required`; complete that branch before calling protected resources. The client refreshes and persists sessions; for SSR use `asUser(token)` per incoming request. Refresh tokens rotate, so avoid parallel refresh attempts and never log them.

Token profiles issue separate tokens for other services; they do not replace the Pawabase session. A receiver validates the profile token's signature, audience, issuer, and expiry against the environment JWKS. User metadata is editable by the user: use server-controlled roles or app metadata for authority.

For guest users, upgrade the existing guest identity when they register so guest-owned rows remain attached. For organizations, check that an active organization is selected before using `$auth.org` in a rule; a signed-in user can still have no active organization. A user API key acts as that person and ends with their authority, while a machine identity acts as itself and has its own roles. OAuth, password reset, invitations, and verification links need environment-specific redirect allowlists. See `auth/guests.mdx`, `auth/organizations.mdx`, `auth/machines.mdx`, and `auth/redirect-urls.mdx`.

## Policy evaluation

Access rules are attached to individual resource operations, bucket actions, flows, routes, channels, agents, and models. Rules can inspect `$auth`, `$record`, `$input`, `$request`, `$credential`, `$object`, `$event`, and `$now`. Common policies include public, authenticated, record owner, role/permission, organization, scope, and custom conditions. A secret key always passes policy, which makes it a poor credential for testing user access.

For list operations, a rule can constrain rows in the query; the result may be empty and `total` may be unknown. A get can return `404` whether the record is absent or hidden. Create/update/delete each have separate policy checks. An update rule that depends on a field such as `owner_id` protects that field from a user changing it to escape the rule. Relations and realtime record changes apply their own read rules.

When implementing a feature, define the actual actor and expected operations, configure rules server side, then exercise anonymous, owner, other-user, and server credentials. A hidden UI control is not authorization. For details read the docs repo's `auth/how-auth-works.mdx`, `auth/sessions.mdx`, `policies/how-rules-work.mdx`, `policies/how-rules-are-evaluated.mdx`, and `policies/testing.mdx`.
