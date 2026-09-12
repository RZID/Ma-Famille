# Payments via DOKU (sandbox only)

No real money moves anywhere in this project. All calls default to
`https://api-sandbox.doku.com`; production URLs must never appear in code.

## Setup

1. Register at `https://sandbox.doku.com`, grab **Client ID** + **Secret Key**.
2. Copy them into `backend/.env` (never commit real keys):
   ```bash
   DOKU_CLIENT_ID=MCH-xxxx
   DOKU_SECRET_KEY=SK-xxxx
   DOKU_BASE_URL=https://api-sandbox.doku.com
   ```
3. Without keys, `POST /payments` and the webhook answer `501` — the TODO
   stubs stay intact.

## Test flow (no real payment)

1. `POST /api/v1/payments` with `booking_public_id` + `amount` → returns
   `checkout_url` (a `sandbox.doku.com` page).
2. Open the URL, pick any channel, then pay via the DOKU **Simulator**
   (`Sandbox dashboard → Settings → Simulator`).
3. DOKU POSTs the result to the Notification URL below.

No DOKU account yet? Preview the same flow with no sign-up at
`https://sandbox.doku.com/demo`.

## Webhook

- Path (fixed — DOKU signs it as Request-Target):
  `POST /api/v1/payments/webhook/doku`
- The endpoint recomputes `Digest` + `HMACSHA256` signature from
  `app/services/doku.py` and rejects mismatches with `401`.
- `transaction.status: SUCCESS` maps to `paid`, anything else to
  `pending`/`failed`. Matching the invoice to a payment row is still TODO
  (lands with the Payment model); the endpoint currently acks with the
  parsed invoice + status.
- Local dev: expose the API publicly first (e.g. `ngrok http 8000`), then
  paste `https://<you>.ngrok.io/api/v1/payments/webhook/doku` as the
  Notification URL in the DOKU sandbox dashboard.

## Layout

```text
app/services/doku.py   # signature, digest, checkout client, invoice numbers
app/api/v1/payments.py # POST /payments, POST /payments/webhook/doku
```
