from typing_extensions import Dict, List, NotRequired, TypedDict, Union


class EventCustomer(TypedDict):
    id: NotRequired[str]


class PaymentMethodTokenizedDetails(TypedDict):
    id: str
    stored: bool


class PaymentMethod(TypedDict):
    tokenizedDetails: PaymentMethodTokenizedDetails


class EventData(TypedDict):
    id: str
    accountId: NotRequired[str]
    paymentTransactionId: NotRequired[str]
    amount: NotRequired[int]
    platformFee: NotRequired[Union[str, int]]
    currency: NotRequired[str]
    metadata: NotRequired[Dict[str, str]]
    status: NotRequired[str]
    email: NotRequired[str]
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    defaultPaymentMethod: NotRequired[str]
    customer: NotRequired[EventCustomer]
    paymentMethod: PaymentMethod
    createdTimestamp: int


class EventEndpoint(TypedDict):
    webhookId: str
    acknowledged: bool
    attempts: int


class Event(TypedDict):
    id: str
    eventType: str
    data: EventData
    endpoints: List[EventEndpoint]
    accountId: NotRequired[str]
    createdTimestamp: int


class Events(TypedDict):
    items: List[Event]


class PausePaymentDetail(TypedDict):
    reason: NotRequired[str]
    resumeAtTimestamp: NotRequired[int]
    pausedAtTimestamp: int
