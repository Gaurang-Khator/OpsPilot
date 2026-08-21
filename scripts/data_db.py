import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    

from app.db.session import SessionLocal
from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.conversation import Conversation

db = SessionLocal()
# db.add(Invoice(customer_id=12, amount=59.78, status="paid", description="Monthly subscription"))
# db.add(Invoice(customer_id=12, amount=1200, status="unpaid", description="emi"))
db.add(Conversation(customer_id=12, status="open"))
db.commit()