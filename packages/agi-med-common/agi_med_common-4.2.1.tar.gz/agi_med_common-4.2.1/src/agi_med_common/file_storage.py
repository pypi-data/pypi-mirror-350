import string
from hashlib import md5
from pathlib import Path

ResourceId = str
ASCII_DIGITS = set(string.ascii_lowercase + string.digits)


def _validate_exist(files_dir):
    if not files_dir.exists():
        err = f"Failed to access file-storage directory: {files_dir}"
        raise OSError(err)


def _validate_dtype(dtype: str):
    if all(map(ASCII_DIGITS.__contains__, dtype)):
        return
    raise ValueError(f'Bad dtype: {dtype}')


class FileStorage:
    def __init__(self, files_dir):
        self.files_dir = Path(files_dir)
        self.files_dir.mkdir(exist_ok=True, parents=True)
        _validate_exist(self.files_dir)

    def _generate_fname_path(self, content, dtype):
        fname_hash = md5(content).hexdigest()
        fname = f'{fname_hash}.{dtype}'
        fpath = self.files_dir / fname
        return fpath

    def upload_maybe(
        self,
        content: bytes | None,
        dtype: str,
    ) -> ResourceId | None:
        if not content:
            return None
        resource_id = self.upload(content, dtype)
        return resource_id

    def upload(self, content: bytes, dtype: str) -> ResourceId | None:
        _validate_dtype(dtype)
        fpath = self._generate_fname_path(content, dtype)
        fpath.write_bytes(content)
        return str(fpath)

    def download(self, rid: ResourceId) -> bytes:
        return Path(rid).read_bytes()

    def is_valid(self, rid: ResourceId) -> bytes:
        return Path(rid).exists() and Path(rid).is_file()
