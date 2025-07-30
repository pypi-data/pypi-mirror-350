from dataclasses import dataclass
from typing import Optional

from .PaymentProduct3391SpecificInput import PaymentProduct3391SpecificInput


@dataclass(kw_only=True)
class CompletePaymentMethodSpecificInput:
    paymentProduct3391SpecificInput: Optional[PaymentProduct3391SpecificInput] = None
