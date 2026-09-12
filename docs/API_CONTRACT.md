# API Contract (planned — NOT implemented in foundation)

Base: `/api/v1`. Implemented now: `GET /health`, `GET /`.

## Entities

### Venue
```json
{ "id": "uuid", "name": "GOR Senayan", "address": "...", "manager_id": "uuid" }
```

### Court
```json
{ "id": "uuid", "venue_id": "uuid", "name": "Court A", "sport": "futsal|badminton", "price_per_hour": 120000, "is_active": true }
```

### Slot (Schedule)
```json
{ "id": "uuid", "court_id": "uuid", "starts_at": "2026-09-20T10:00:00Z", "ends_at": "2026-09-20T11:00:00Z", "status": "available|held|booked|blocked" }
```
Rule: `ends_at > starts_at`. No overlap for same `court_id` unless `status=blocked` replaced.

### Booking
```json
{ "id": "uuid", "slot_id": "uuid", "customer_name": "...", "customer_contact": "...", "status": "pending|confirmed|cancelled", "created_at": "..." }
```
Rules:
- One active booking per slot (overlap/conflict guard backend-side).
- `pending` expires after TTL unless confirmed + deposit.

### Payment
```json
{ "id": "uuid", "booking_id": "uuid", "amount": 60000, "kind": "deposit|full", "status": "unpaid|paid|refunded" }
```

## Planned endpoints

```text
GET    /venues /venues/{id}            POST /venues (manager)
GET    /courts?venue_id=...            POST /courts (manager)
GET    /slots?court_id=&from=&to=      POST /slots (manager, bulk create allowed)
POST   /bookings                       POST /bookings/{id}/confirm (manager)
POST   /bookings/{id}/cancel
GET    /bookings?slot_id=&status=
POST   /payments                       POST /payments/{id}/mark-paid (manager)
```

## Errors

```json
{ "detail": "slot already booked" }
```
- `409` for booking conflicts.
- `422` for validation.
- `404` for unknown ids.

Frontend must surface `detail` verbatim and refresh slot state after `409`.
