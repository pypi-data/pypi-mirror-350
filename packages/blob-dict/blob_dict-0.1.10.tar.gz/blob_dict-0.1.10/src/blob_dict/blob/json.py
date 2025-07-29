from __future__ import annotations

import json
from typing import Any, override

import yaml
from pydantic import BaseModel

from . import StrBlob


class JsonDictBlob(StrBlob):
    def __init__(self, blob: bytes | str | dict[str, Any]) -> None:
        if isinstance(blob, dict):
            blob = json.dumps(blob)

        super().__init__(blob)

    def as_dict(self) -> dict[str, Any]:
        return json.loads(self._blob_bytes)

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.as_dict().__repr__()})"


class YamlDictBlob(StrBlob):
    def __init__(self, blob: bytes | str | dict[str, Any]) -> None:
        if isinstance(blob, dict):
            blob = yaml.safe_dump(blob)

        super().__init__(blob)

    def as_dict(self) -> dict[str, Any]:
        return yaml.safe_load(self._blob_bytes)

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.as_dict().__repr__()})"


class JsonModelBlob(JsonDictBlob):
    __MISSING_MODEL_CLASS_ERROR_MESSAGE = "Must specify Pydantic model class if specified blob is not a model object"  # noqa: E501
    __BAD_MODEL_CLASS_ERROR_MESSAGE = "Must specify Pydantic model class that inherits from `BaseModel`"  # noqa: E501

    def __init__(
        self,
        blob: bytes | str | dict[str, Any] | BaseModel,
        *,
        model_class: type[BaseModel] | None = None,
    ) -> None:
        if not isinstance(blob, BaseModel) and not model_class:
            raise ValueError(JsonModelBlob.__MISSING_MODEL_CLASS_ERROR_MESSAGE)

        if model_class == BaseModel:
            raise ValueError(JsonModelBlob.__BAD_MODEL_CLASS_ERROR_MESSAGE)

        self.__model_class: type[BaseModel]
        if isinstance(blob, BaseModel):
            self.__model_class = type(blob)
            blob = blob.model_dump_json()
        elif model_class:
            self.__model_class = model_class

        super().__init__(blob)

    def as_model(self) -> BaseModel:
        return self.__model_class.model_validate_json(self._blob_bytes)

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.as_model().__repr__()})"
