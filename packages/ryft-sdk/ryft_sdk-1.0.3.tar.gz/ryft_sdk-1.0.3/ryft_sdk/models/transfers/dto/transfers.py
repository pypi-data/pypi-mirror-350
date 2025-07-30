from typing_extensions import Dict, List, NotRequired, TypedDict


class TransferDestination(TypedDict):
    accountId: str


class TransferError(TypedDict):
    code: str
    description: str


class Transfer(TypedDict):
    id: str
    status: str
    amount: int
    currency: str
    reason: NotRequired[str]
    source: NotRequired[TransferDestination]
    destination: NotRequired[TransferDestination]
    errors: NotRequired[List[TransferError]]
    metadata: NotRequired[Dict[str, str]]
    createdTimestamp: int
    lastUpdatedTimestamp: int


class Transfers(TypedDict):
    items: List[Transfer]
    paginationToken: NotRequired[str]
