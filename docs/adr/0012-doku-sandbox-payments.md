# ADR 0012: DOKU sandbox for third-party payments

- Status: Accepted
- Date: 2026-09-13
- Deciders: payment group

## Context

Bookings confirm automatically once a deposit is paid, so the backend must
take payments through a third party — sandbox only, since the scope
explicitly excludes a real gateway. Candidates were Xendit, Midtrans and
DOKU, all with Indonesian channels (VA, e-wallet, QRIS, cards) and free
test environments.

## Decision

Integrate DOKU's hosted Checkout in sandbox mode, with payment results
delivered via DOKU HTTP Notification (webhook) verified by HMAC-SHA256
signature.

## Rationale

- DOKU's demo site runs with no sign-up, so the payment flow is reviewable
  before any integration code exists — useful for demos to non-technical
  stakeholders.
- The sandbox Simulator covers every channel plus notification replay, so
  the full loop (checkout → simulator → webhook → auto-confirm) is testable
  without moving money.
- The non-SNAP signature scheme (Client-Id/Request-Id/Timestamp/Digest) is
  more work than Xendit's basic auth, but it is fully offline-testable and
  the verification logic doubles as webhook authentication — no extra
  secret-sharing needed.
- Hosted checkout keeps card data off our servers, so there is no PCI
  scope for a student project.

## Consequences

- Positive: `POST /payments` returns a real sandbox checkout URL;
  `POST /payments/webhook/doku` accepts only correctly signed
  notifications and maps `SUCCESS` to `paid`.
- Negative: DOKU docs are split across two portals; `docs/PAYMENTS.md`
  pins the exact pages and URLs used.
- Keys stay in `backend/.env` (gitignored); missing keys keep the `501`
  stubs, so CI needs no secrets.

## Alternatives considered

- Xendit test mode — rejected: simpler auth, but the team preferred
  DOKU's no-signup demo for stakeholder review.
- Midtrans Snap sandbox — rejected: most tutorials of the three, but the
  popup flow fits our redirect-and-webhook design less cleanly.
- No third party (manual transfer proof) — rejected: cannot drive the
  required automatic confirmation on deposit.
