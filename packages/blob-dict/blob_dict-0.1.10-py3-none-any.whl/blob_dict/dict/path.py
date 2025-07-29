import shutil
from abc import abstractmethod
from collections.abc import Iterator
from mimetypes import guess_type
from pathlib import Path
from typing import Any, Literal, Protocol, override

from extratools_core.typing import PathLike

from ..blob import BytesBlob, StrBlob
from ..blob.json import JsonDictBlob, YamlDictBlob
from . import BlobDictBase


class LocalPath(Path):
    def rmtree(self) -> None:
        shutil.rmtree(self)


class ExtraPathLike(PathLike, Protocol):
    @abstractmethod
    def rmtree(self) -> None:
        ...


class PathBlobDict(BlobDictBase):
    def __init__(
        self,
        path: ExtraPathLike | None = None,
        *,
        compression: bool = False,
        blob_class: type[BytesBlob] = BytesBlob,
        blob_class_args: dict[str, Any] | None = None,
    ) -> None:
        super().__init__()

        if path is None:
            path = LocalPath(".")

        if isinstance(path, Path):
            path = path.expanduser()

        self.__path: ExtraPathLike = path

        self.__compression: bool = compression

        self.__blob_class: type[BytesBlob] = blob_class
        self.__blob_class_args: dict[str, Any] = blob_class_args or {}

    def create(self) -> None:
        self.__path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def delete(self) -> None:
        self.__path.rmtree()

    @override
    def __contains__(self, key: object) -> bool:
        return (self.__path / str(key)).is_file()

    def __get_blob_class(self, key: str) -> type[BytesBlob]:  # noqa: PLR0911
        mime_type: str | None
        mime_type, _ = guess_type(self.__path / key)

        match mime_type:
            case "application/json":
                return JsonDictBlob
            case "application/octet-stream":
                return BytesBlob
            case "application/yaml":
                return YamlDictBlob
            case "audo/mpeg":
                # Import here as it has optional dependency
                from ..blob.audio import AudioBlob  # noqa: PLC0415

                return AudioBlob
            case "image/png":
                # Import here as it has optional dependency
                from ..blob.image import ImageBlob  # noqa: PLC0415

                return ImageBlob
            case (
                "text/css"
                 | "text/csv"
                 | "text/html"
                 | "text/javascript"
                 | "text/markdown"
                 | "text/plain"
                 | "text/xml"
            ):
                return StrBlob
            case "video/mp4":
                # Import here as it has optional dependency
                from ..blob.video import VideoBlob  # noqa: PLC0415

                return VideoBlob
            case _:
                return self.__blob_class

    def _get(self, key: str, blob_bytes: bytes) -> BytesBlob:
        blob: BytesBlob = BytesBlob.from_bytes(blob_bytes, compression=self.__compression)
        return blob.as_blob(
            self.__get_blob_class(key),
            self.__blob_class_args,
        )

    @override
    def __getitem__(self, key: str, /) -> BytesBlob:
        if key not in self:
            raise KeyError

        return self._get(key, (self.__path / key).read_bytes())

    @override
    def __iter__(self) -> Iterator[str]:
        # The concept of relative path does not exist for `CloudPath`,
        # and each walked path is always absolute for `CloudPath`.
        # Therefore, we extract each key by removing the path prefix.
        # In this way, the same logic works for both absolute and relative path.
        prefix_len: int = (
            len(str(self.__path.absolute()))
            # Extra 1 is for separator `/` between prefix and filename
            + 1
        )

        for parent, _, files in self.__path.walk():
            for filename in files:
                yield str((parent / filename).absolute())[prefix_len:]

    @override
    def clear(self) -> None:
        for parent, dirs, files in self.__path.walk(top_down=False):
            for filename in files:
                (parent / filename).unlink()
            for dirname in dirs:
                (parent / dirname).rmdir()

    def __cleanup(self, key: str) -> None:
        (self.__path / key).unlink()

        for parent in (self.__path / key).parents:
            if parent == self.__path:
                return

            if parent.is_dir() and next(iter(parent.iterdir()), None) is None:
                parent.rmdir()

    @override
    def pop[T: Any](
        self,
        key: str,
        /,
        default: BytesBlob | T | Literal["__DEFAULT"] = "__DEFAULT",
    ) -> BytesBlob | T:
        blob: BytesBlob | None = self.get(key)
        if blob:
            self.__cleanup(key)

        if blob is not None:
            return blob

        if default == "__DEFAULT":
            raise KeyError

        return default

    @override
    def __delitem__(self, key: str, /) -> None:
        if key not in self:
            raise KeyError

        self.__cleanup(key)

    __BAD_BLOB_CLASS_ERROR_MESSAGE: str = "Must specify blob that is instance of {blob_class}"

    @override
    def __setitem__(self, key: str, blob: BytesBlob, /) -> None:
        if not isinstance(blob, self.__blob_class):
            raise TypeError(PathBlobDict.__BAD_BLOB_CLASS_ERROR_MESSAGE.format(
                blob_class=self.__blob_class,
            ))

        (self.__path / key).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        blob_bytes: bytes = blob.as_bytes(compression=self.__compression)
        (self.__path / key).write_bytes(blob_bytes)
