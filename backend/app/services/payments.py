from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.payment import Payment
from app.schemas.payment import PaymentKind


def get_by_public_id(db: Session, public_id: UUID) -> Payment | None:
    return db.scalars(select(Payment).where(Payment.public_id == public_id)).first()


def get_by_invoice(db: Session, invoice_number: str) -> Payment | None:
    return (
        db.scalars(select(Payment).where(Payment.invoice_number == invoice_number)).first()
    )


def list_by_booking_id(db: Session, booking_id: int) -> list[Payment]:
    stmt = select(Payment).where(Payment.booking_id == booking_id).order_by(Payment.id)
    return list(db.scalars(stmt).all())


def create_payment(
    db: Session,
    booking_id: int,
    amount: int,
    kind: PaymentKind,
    invoice_number: str,
) -> Payment:
    payment = Payment(
        booking_id=booking_id,
        amount=amount,
        kind=kind,
        invoice_number=invoice_number,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def mark_paid(db: Session, payment: Payment) -> Payment:
    """Mark paid and auto-confirm a pending booking (deposit rule)."""
    payment.status = "paid"
    booking = db.get(Booking, payment.booking_id)
    if booking is not None and booking.status == "pending":
        booking.status = "confirmed"
    db.commit()
    db.refresh(payment)
    return payment


def booking_public_id(db: Session, payment: Payment) -> UUID:
    return db.get(Booking, payment.booking_id).public_id
