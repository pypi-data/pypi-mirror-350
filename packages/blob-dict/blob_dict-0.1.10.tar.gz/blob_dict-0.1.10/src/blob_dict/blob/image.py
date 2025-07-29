from __future__ import annotations

from pathlib import Path
from typing import Self, override

from extratools_image import bytes_to_image, image_to_bytes
from PIL.Image import Image

from . import BytesBlob


class ImageBlob(BytesBlob):
    def __init__(self, blob: bytes | Image) -> None:
        if isinstance(blob, Image):
            blob = image_to_bytes(blob)

        super().__init__(blob)

    def as_image(self) -> Image:
        return bytes_to_image(self._blob_bytes)

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(...)"

    @classmethod
    @override
    def load(cls: type[Self], f: Path | str) -> Self:
        f = Path(f).expanduser()
        img_format: str = f.suffix.lstrip('.').lower()
        img_bytes: bytes = f.read_bytes()

        if img_format == "png":
            return cls(img_bytes)

        return cls(bytes_to_image(img_bytes, _format=img_format))

    @override
    def dump(self, f: Path | str) -> None:
        f = Path(f).expanduser()
        if f.suffix.lower() != ".png":
            msg = "Only PNG file is supported."
            raise ValueError(msg)

        f.write_bytes(self.as_bytes())
