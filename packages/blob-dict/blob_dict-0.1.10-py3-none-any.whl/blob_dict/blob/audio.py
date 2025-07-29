from __future__ import annotations

from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import NamedTuple, Self, override

import numpy
import soundfile
from moviepy.audio.AudioClip import AudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from . import BytesBlob


class AudioData(NamedTuple):
    data: numpy.ndarray
    sample_rate: int


class AudioBlob(BytesBlob):
    __IN_MEMORY_FILE_NAME: str = "file.mp3"

    def __init__(self, blob: bytes | AudioClip | AudioData) -> None:
        if isinstance(blob, AudioClip):
            if (
                isinstance(blob, AudioFileClip)
                # Need to check whether `filename` is `str`` as it can also be sound array
                and isinstance(blob.filename, str)
                and blob.filename.lower().endswith(".mp3")
            ):
                blob = Path(blob.filename).read_bytes()
            else:
                with NamedTemporaryFile(suffix=".mp3", delete_on_close=False) as f:
                    blob.write_audiofile(f.name)

                    f.close()

                    blob = Path(f.name).read_bytes()
        elif isinstance(blob, AudioData):
            bio = BytesIO()
            bio.name = AudioBlob.__IN_MEMORY_FILE_NAME
            soundfile.write(bio, AudioData.data, AudioData.sample_rate)
            blob = bio.getvalue()

        super().__init__(blob)

    def as_audio(self, filename: str) -> AudioFileClip:
        Path(filename).write_bytes(self._blob_bytes)

        return AudioFileClip(filename)

    def as_audio_data(self) -> AudioData:
        bio = BytesIO(self._blob_bytes)
        bio.name = AudioBlob.__IN_MEMORY_FILE_NAME
        return AudioData(*soundfile.read(bio))

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(...)"

    @classmethod
    @override
    def load(cls: type[Self], f: Path | str) -> Self:
        f = Path(f).expanduser()

        if f.suffix.lower() == ".mp3":
            return cls(f.read_bytes())

        clip = AudioFileClip(str(f))
        blob = cls(clip)
        clip.close()

        return blob

    @override
    def dump(self, f: Path | str) -> None:
        f = Path(f).expanduser()
        if f.suffix.lower() != ".mp3":
            msg = "Only MP3 file is supported."
            raise ValueError(msg)

        f.write_bytes(self.as_bytes())
