from app.db.session import SessionLocal
from app.tools.schemas import InvoiceOut
from app.models.invoice import Invoice


def get_invoices_by_customer(customer_id: int) -> list[InvoiceOut]:
    """Fetch all invoices of a customer"""

    db = SessionLocal()

    try:
        invoices = db.query(Invoice).filter(Invoice.customer_id == customer_id).all()

        return [ InvoiceOut(id=i.id, amount=i.amount, status=i.status, description=i.description) for i in invoices ]

    finally:
        db.close()