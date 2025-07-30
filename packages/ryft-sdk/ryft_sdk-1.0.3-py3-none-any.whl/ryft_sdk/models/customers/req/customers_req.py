from typing_extensions import Dict, NotRequired, TypedDict


class CreateCustomerRequest(TypedDict):
    email: str
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    homePhoneNumber: NotRequired[str]
    mobilePhoneNumber: NotRequired[str]
    metadata: NotRequired[Dict[str, str]]


class UpdateCustomerRequest(TypedDict):
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    homePhoneNumber: NotRequired[str]
    mobilePhoneNumber: NotRequired[str]
    metadata: NotRequired[Dict[str, str]]
    defaultPaymentMethod: NotRequired[str]
