## Introduction

This library allows you to access blobs via Pythonic `dict`-like interface.
Note that due to the nature of blob, not all `dict` methods are implemented.
Therefore, it is not a subclass of [`MutableMapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping) type.

## Supported Blob Dict Methods

Specifically, for a blob dict `d`, the following methods are available:

- `len(d)`
- `key in d`
- `d.get(key, default)`
- `d[key]`
- `for key in d:`
- `d.pop(key, default)`
- `del d[key]`
- `d[key] = blob`

## Supported Blob Dict Types

There are different blob dict implementations:

- `InMemoryBlobDict` for in-memory storage, with optional TTL
- `PathBlobDict` for specified folder on file system as storage, with relative file path as key
  - It supports local file systems via `PathLib`
    - Ideally use provided `LocalPath` class (which is a subclass of `Path`) for full support
  - It also supports cloud file systems (like AWS S3 (and competible Cloudflare R2), Azure Blob Storage, and Google Cloud Storage) via [`CloudPathLib`](https://cloudpathlib.drivendata.org/stable/)
- `GitBlobDict` for specified Git repo on file system as storage, with relative file path as key
  - It auto commits any add/update/delete
  - It auto syncs with remote if enabled
  - Optionally, key can be tuple where the second part is version:
    - `str` for version at specified commit/tag, like `HEAD~2`
    - `int` for relative version (same way of Python sequence index) of file, like `0` for first version and `-2` for previous version
    - `datetime` for latest version before specified date/time
    - `timedelta` for latest version of specified duration before now
- `VulkeyBlobDict` for Vulkey/Redis-based storage, with optional TTL
- Specially, `MultiReplicaBlobDict` for utilizing multiple blob dicts underneath
  - For example, you can use in-memory or local file system blob dict as cache layer, while any cloud file system blob dict as storage

## Supported Blob Types

There as many types of blobs with following class hierarchy relationship:

- `BytesBlob` for any data
  - `StrBlob` for any string
    - `JsonDictBlob` for any JSON `dict` object
    - `JsonModelBlob` for any [Pydantic](https://docs.pydantic.dev/) model object
  - `AudioBlob` for any [SoundFile](https://github.com/bastibe/python-soundfile) audio data
  - `ImageBlob` for any [PIL/Pillow](https://python-pillow.github.io/) image data
  - `VideoBlob` for any [MoviePy](https://zulko.github.io/moviepy/) video clip data

Ultimately, all data are persisted as bytes.
