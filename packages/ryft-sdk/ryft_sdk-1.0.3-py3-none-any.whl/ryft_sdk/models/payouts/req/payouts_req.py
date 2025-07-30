from typing_extensions import Dict, NotRequired, TypedDict


class CreatePayoutRequest(TypedDict):
    amount: int
    currency: str
    payoutMethodId: str
    metadata: NotRequired[Dict[str, str]]
