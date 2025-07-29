from collections.abc import Mapping, MutableMapping
from typing import override

from ..blob import BytesBlob


class ImmutableBlobDictBase(Mapping[str, BytesBlob]):
    @override
    def __len__(self) -> int:
        return sum(1 for _ in self)


class BlobDictBase(ImmutableBlobDictBase, MutableMapping[str, BytesBlob]):
    ...
