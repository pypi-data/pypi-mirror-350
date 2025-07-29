from collections.abc import Iterator
from datetime import timedelta
from typing import Any, Literal, cast, override

from valkey import Valkey

from ..blob import BytesBlob, StrBlob
from . import BlobDictBase


class ValkeyBlobDict(BlobDictBase):
    def __init__(
        self,
        *,
        ttl: timedelta | None = None,
        str_blob_only: bool = False,
        client_kwargs: dict[str, Any] | None = None,
    ) -> None:
        super().__init__()

        self.__client: Valkey = Valkey(
            **(client_kwargs or {}),
            decode_responses=True,
        )

        self.__ttl_ms: int | None = int(ttl.total_seconds() * 1_000) if ttl else None

        self.__str_blob_only: bool = str_blob_only

    @override
    def __len__(self) -> int:
        return cast("int", self.__client.dbsize())

    @override
    def __contains__(self, key: object) -> bool:
        return cast("int", self.__client.exists(str(key))) == 1

    @override
    def get[T: Any](self, key: str, /, default: BytesBlob | T = None) -> BytesBlob | T:
        response: Any = self.__client.get(key)
        if not response:
            return default

        s: str = cast("str", response)
        return (
            StrBlob(s) if self.__str_blob_only
            else BytesBlob.from_b64_str(s)
        )

    @override
    def __getitem__(self, key: str, /) -> BytesBlob:
        blob: BytesBlob | None = self.get(key)
        if blob is None:
            raise KeyError

        return blob

    @override
    def __iter__(self) -> Iterator[str]:
        for key in self.__client.scan_iter(_type="STRING"):
            yield cast("str", key)

    @override
    def clear(self) -> None:
        self.__client.flushdb()

    @override
    def pop[T: Any](
        self,
        key: str,
        /,
        default: BytesBlob | T | Literal["__DEFAULT"] = "__DEFAULT",
    ) -> BytesBlob | T:
        if response := self.get(key):
            self.__client.delete(key)
            return response

        if default == "__DEFAULT":
            raise KeyError

        return default

    @override
    def __delitem__(self, key: str, /) -> None:
        number_deleted: int = cast("int", self.__client.delete(key))
        if number_deleted == 0:
            raise KeyError

    __BAD_BLOB_CLASS_ERROR_MESSAGE: str = "Must specify blob of type `StrBlob`"

    @override
    def __setitem__(self, key: str, blob: BytesBlob, /) -> None:
        if self.__str_blob_only and not isinstance(blob, StrBlob):
            raise TypeError(self.__BAD_BLOB_CLASS_ERROR_MESSAGE)

        self.__client.set(
            key,
            (
                cast("StrBlob", blob).as_str() if self.__str_blob_only
                else blob.as_b64_str()
            ),
            px=self.__ttl_ms,
        )
