from dataclasses import dataclass
from typing import Optional

from .CompleteFinancingPaymentMethodSpecificInput import (
    CompleteFinancingPaymentMethodSpecificInput,
)
from .CustomerDevice import CustomerDevice
from .Order import Order


@dataclass(kw_only=True)
class CompletePaymentRequest:
    financingPaymentMethodSpecificInput: Optional[
        CompleteFinancingPaymentMethodSpecificInput
    ] = None
    order: Optional[Order] = None
    device: Optional[CustomerDevice] = None
