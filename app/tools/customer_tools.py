from app.db.session import SessionLocal
from app.models.customer import Customer
from app.tools.schemas import ToolError, CustomerOut


def get_customer_by_email(email: str) -> CustomerOut | ToolError:
    """Look for a customer by email. Returns ToolError if not found -- never raises to the caller."""

    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.email == email).first()
        if customer is None:
            return ToolError(error=f"No customer found with email: {email}")

        return CustomerOut(id=customer.id, name=customer.name, email=customer.email)
    
    finally:
        db.close()


def create_customer(name: str, email: str) -> CustomerOut | ToolError:
    """Create a customer with given name and email. Returns ToolError if customer with given email already exists."""

    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.email == email).first()
        if customer is None:
            new_customer = Customer(name=name, email=email)
            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)
            return CustomerOut(id=new_customer.id, name=new_customer.name, email=new_customer.email)
        
        return ToolError(error=f"Customer already exists with email: {email}")
    finally:
        db.close()