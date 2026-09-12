# API Contract (TODO stubs live in Swagger — `GET /docs`)

Base: `/api/v1`. Working now: `GET /health`, `GET /health/db`, `GET /`.
Domain routes exist as TODO stubs (return `501` with a `TODO:` detail) so the
Swagger surface is reviewable before any store logic lands.

## Identifiers

- `id` (integer, autoincrement): system-level PK, FKs and joins only. Never
  exposed to clients.
- `public_id` (UUIDv7, unique + indexed): the only id clients see, in URLs
  and payloads. Chosen over random v4 GUIDs because v7 is time-ordered —
  sortable and index-friendly — while staying unguessable enough for public
  references. See `backend/app/core/ids.py` and `docs/DATABASE.md`.

## Entities (all carry `public_id`, FKs reference `public_id` client-side)

## Entities

### Venue
```json
{ "public_id": "uuidv7", "name": "GOR Senayan", "address": "..." }
```

### Court
```json
{ "public_id": "uuidv7", "venue_public_id": "uuidv7", "name": "Court A", "sport": "futsal|badminton", "price_weekday": 100000, "price_weekend": 150000, "is_active": true }
```

### Slot (Schedule)
```json
{ "public_id": "uuidv7", "court_public_id": "uuidv7", "starts_at": "2026-09-20T10:00:00Z", "ends_at": "2026-09-20T11:00:00Z", "price": 120000, "status": "available|held|booked|blocked" }
```
Rule: `ends_at > starts_at`. No overlap for same court unless `status=blocked` replaced.

### Booking
```json
{ "public_id": "uuidv7", "slot_public_id": "uuidv7", "customer_name": "...", "customer_contact": "...", "status": "pending|confirmed|cancelled", "created_at": "..." }
```
Rules:
- One active booking per slot (overlap/conflict guard backend-side, `409`).
- `pending` expires after TTL unless confirmed + deposit.

### Payment
```json
{ "public_id": "uuidv7", "booking_public_id": "uuidv7", "amount": 60000, "kind": "deposit|full", "status": "unpaid|paid|refunded" }
```

## Endpoints (TODO stubs — all `501` for now)

```text
GET    /venues /venues/{public_id}            POST /venues (manager)
PATCH  /venues/{public_id} (manager)          DELETE /venues/{public_id} (manager)
GET    /courts?venue_public_id=...            POST /courts (manager)
GET    /slots?court_public_id=&day=           POST /slots (manager, bulk)
POST   /bookings  (409 on conflict)           GET /bookings?customer_contact= (history)
POST   /bookings/{public_id}/confirm          POST /bookings/{public_id}/cancel
POST   /payments  (deposit|full)              POST /payments/{public_id}/mark-paid (manager)
GET    /manager/bookings?status=              GET /manager/occupancy?from_day=&to_day=
```

## Errors

```json
{ "detail": "slot already booked" }
```
- `409` for booking conflicts.
- `422` for validation.
- `404` for unknown ids.

Frontend must surface `detail` verbatim and refresh slot state after `409`.
