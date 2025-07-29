from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Self, override

from moviepy.editor import VideoClip, VideoFileClip

from . import BytesBlob


class VideoBlob(BytesBlob):
    def __init__(self, blob: bytes | VideoClip) -> None:
        if isinstance(blob, VideoClip):
            if (
                isinstance(blob, VideoFileClip)
                and blob.filename.lower().endswith(".mp4")
            ):
                blob = Path(blob.filename).read_bytes()
            else:
                with NamedTemporaryFile(suffix=".mp4", delete_on_close=False) as f:
                    blob.write_videofile(f.name)

                    f.close()

                    blob = Path(f.name).read_bytes()

        super().__init__(blob)

    def as_video(self, filename: str) -> VideoFileClip:
        Path(filename).write_bytes(self._blob_bytes)

        return VideoFileClip(filename)

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(...)"

    @classmethod
    @override
    def load(cls: type[Self], f: Path | str) -> Self:
        f = Path(f).expanduser()

        if f.suffix.lower() == ".mp4":
            return cls(f.read_bytes())

        clip = VideoFileClip(str(f))
        blob = cls(clip)
        clip.close()

        return blob

    @override
    def dump(self, f: Path | str) -> None:
        f = Path(f).expanduser()
        if f.suffix.lower() != ".mp4":
            msg = "Only MP4 file is supported."
            raise ValueError(msg)

        f.write_bytes(self.as_bytes())
