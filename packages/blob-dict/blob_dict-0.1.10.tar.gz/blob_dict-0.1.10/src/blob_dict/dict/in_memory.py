from collections.abc import Iterator, MutableMapping
from datetime import timedelta
from typing import Any, Literal, override

from ttl_dict import TTLDict

from ..blob import BytesBlob
from . import BlobDictBase


class InMemoryBlobDict(BlobDictBase):
    __EXTERNAL_DICT_TTL_ERROR_MESSAGE: str = "Cannot specify `ttl` for external `data_dict`"

    def __init__(
        self,
        data_dict: MutableMapping[str, BytesBlob] | None = None,
        *,
        ttl: timedelta | None = None,
    ) -> None:
        super().__init__()

        if data_dict is not None and ttl is not None:
            raise ValueError(InMemoryBlobDict.__EXTERNAL_DICT_TTL_ERROR_MESSAGE)

        self.__dict: MutableMapping[str, BytesBlob] = (
            (
                {} if ttl is None
                else TTLDict[str, BytesBlob](ttl)
            ) if data_dict is None
            else data_dict
        )

    @override
    def __len__(self) -> int:
        return len(self.__dict)

    @override
    def __contains__(self, key: Any) -> bool:
        return str(key) in self.__dict

    @override
    def get[T: Any](
        self,
        key: str,
        /,
        default: BytesBlob | T = None,
    ) -> BytesBlob | T:
        return self.__dict.get(key, default)

    @override
    def __getitem__(self, key: str, /) -> BytesBlob:
        return self.__dict[key]

    @override
    def __iter__(self) -> Iterator[str]:
        yield from (
            key for key in self.__dict
        )

    @override
    def clear(self) -> None:
        self.__dict.clear()

    @override
    def pop[T: Any](
        self,
        key: str,
        /,
        default: BytesBlob | T | Literal["__DEFAULT"] = "__DEFAULT",
    ) -> BytesBlob | T:
        if default == "__DEFAULT":
            return self.__dict.pop(key)

        return self.__dict.pop(key, default)

    @override
    def __delitem__(self, key: str, /) -> None:
        del self.__dict[key]

    @override
    def __setitem__(self, key: str, blob: BytesBlob, /) -> None:
        self.__dict[key] = blob
