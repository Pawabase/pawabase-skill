# Storage and files

Buckets hold objects addressed by bucket and key. Bucket settings control visibility, allowed types, max size, and access rules for operations. Public read does not grant public upload/list/delete. For per-user files, include an owner or organization segment in the key and write a server rule against `$object.segments`; keep display names and ownership records in data tables where needed.

## Verified TypeScript pattern

```ts
const avatars = pb.storage.from("avatars");
await avatars.upload(`${userId}/me.png`, file);
const blob = await avatars.download(`${userId}/me.png`);
const { files, prefixes, cursor } = await avatars.list({ prefix: `${userId}/` });
await avatars.remove(`${userId}/old.png`);
```

The verified client also provides `getPublicUrl`, `createSignedUrl`, `createSignedUploadUrl`, and `uploadToSignedUrl`. A public URL works only for a public bucket. A signed URL grants temporary access within its scope; the signed upload URL itself is the upload credential, so do not attach a project key to that upload. Replacing an existing key overwrites the object; use unique keys or deliberate versioning when this matters.

The public OpenAPI snapshot includes `/storage/v1/object/{bucket}/{key}`, `/storage/v1/list/{bucket}`, `/storage/v1/sign/{bucket}/{key}`, `/storage/v1/files/{env}/{bucket}/{key}`, and share-token routes. Verify exact verbs, payloads, and upload form in the target OpenAPI. The verified Python 0.2.0 wheel has no storage namespace; use a newer compatible release or HTTP.

Files and records have separate lifecycles. Deleting a record does not automatically prove its referenced object was removed; design explicit cleanup if required. For large uploads, use a signed upload path when supported. Use expiring share links for access outside authenticated clients, and image transforms for derived sizes. Read `storage/buckets.mdx`, `storage/upload.mdx`, `storage/urls-and-links.mdx`, `storage/access.mdx`, and `storage/files-and-records.mdx` in the docs repo.

An environment backup does **not** include stored object bytes. A restore may bring back rows that point at files absent from the restored object store; plan separate object backup and recovery. Store object keys in rows rather than a gateway URL so environment/domain changes do not corrupt references. Replacing a file at the same key can leave a stale cached image; use versioned keys or cache-aware delivery when immediate updates matter.
