# API Contract (live — browse it at `GET /docs`)

Base: `/v1`. All domain routes are wired to the store; the only
`501` left is `POST /payments` (and the webhook) when DOKU keys are missing.

## Auth

- Customer reads + booking flow: open.
- Manager writes (`POST/PATCH/DELETE` venues & courts, slot create/update,
  booking confirm, payment mark-paid, all of `/manager/*`):
  header `X-Manager-Token` must match `MANAGER_TOKEN`
  (empty in local dev = open). Wrong/missing → `401`.

## Identifiers

- `id` (integer, autoincrement): system-level PK, FKs and joins only. Never
  exposed to clients.
- `public_id` (UUIDv7, unique + indexed): the only id clients see, in URLs
  and payloads. Chosen over random v4 GUIDs because v7 is time-ordered —
  sortable and index-friendly — while staying unguessable enough for public
  references. See `backend/app/core/ids.py` and `docs/DATABASE.md`.

## Entities (all carry `public_id`, FKs reference `public_id` client-side)

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
{ "public_id": "uuidv7", "booking_public_id": "uuidv7", "amount": 60000, "kind": "deposit|full", "status": "unpaid|paid|refunded", "invoice_number": "MAF-..." }
```
`invoice_number` links the row to the DOKU sandbox checkout (see `docs/PAYMENTS.md`).

## Endpoints

```text
GET    /venues /venues/{public_id}            POST /venues (manager)
PATCH  /venues/{public_id} (manager)          DELETE /venues/{public_id} (manager)
GET    /courts?venue_public_id=...            POST /courts (manager)
PATCH  /courts/{public_id} (manager)          DELETE /courts/{public_id} (manager, deactivates)
GET    /slots?court_public_id=&day=           POST /slots (manager, bulk)
PATCH  /slots/{public_id} (manager, open/close)
POST   /bookings  (409 on conflict)           GET /bookings?customer_contact= (history)
POST   /bookings/{public_id}/confirm (manager)  POST /bookings/{public_id}/cancel
POST   /payments  → {invoice_number, checkout_url}   GET /payments?booking_public_id=
POST   /payments/{public_id}/mark-paid (manager, auto-confirms booking)
POST   /payments/webhook/doku (DOKU signed notification → paid + auto-confirm)
GET    /manager/bookings?booking_status=      GET /manager/occupancy?from_day=&to_day=
```

Booking also flips `slot.status` (`available`→`booked` on create,
back to `available` on cancel), so the availability calendar never shows
a taken slot as free.

## Errors

```json
{ "detail": "slot is booked" }
```
- `409` for booking conflicts (`slot is booked`, or `slot already booked`
  on a write race).
- `422` for validation.
- `404` for unknown ids.
- `401` for manager routes without a valid token.

Frontend must surface `detail` verbatim and refresh slot state after `409`.
