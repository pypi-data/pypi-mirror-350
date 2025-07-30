from typing_extensions import Dict, List, NotRequired, TypedDict


class File(TypedDict):
    id: str
    name: str
    type: str
    category: str
    metadata: NotRequired[Dict[str, str]]
    createdTimestamp: int
    lastUpdatedTimestamp: int
    sizeInBytes: NotRequired[int]


class Files(TypedDict):
    items: List[File]
    paginationToken: NotRequired[str]
