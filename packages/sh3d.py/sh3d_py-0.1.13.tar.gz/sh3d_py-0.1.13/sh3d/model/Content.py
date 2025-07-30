import dataclasses
import zipfile
import hashlib
from functools import cached_property
from pathlib import Path

from .ContentDigest import ContentDigest
from ..enums.DigestHashEnum import DigestHashEnum


class IDataLoader:

    def load(self) -> bytes:
        raise NotImplementedError

    def digest(self) -> ContentDigest:
        raise NotImplementedError


class PathLoader(IDataLoader):
    path: Path

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> bytes:
        with self.path.open('rb') as f:
            return f.read()

    def digest(self) -> ContentDigest:
        return ContentDigest(self.path.name, DigestHashEnum.SHA_1, hashlib.sha1(self.load(), usedforsecurity=False).digest())


class ZipLoader(IDataLoader):
    enum_to_hash = {
        DigestHashEnum.SHA_1: hashlib.sha1
    }

    def __init__(self, zip_file: zipfile.ZipFile, content_digest: ContentDigest):
        self.zip_file = zip_file
        self.content_digest = content_digest

    def load(self) -> bytes:
        asset = self.zip_file.read(self.content_digest.name)
        calculated_digest = self.enum_to_hash.get(self.content_digest.digest_hash, hashlib.sha1)(asset).digest()
        if calculated_digest != self.content_digest.digest:
            raise ValueError('Incorrect digest')
        return asset

    def digest(self) -> ContentDigest:
        return self.content_digest


@dataclasses.dataclass(frozen=True)
class Content:
    data_loader: IDataLoader


    @cached_property
    def content_digest(self) -> ContentDigest:
        return self.data_loader.digest()

    @cached_property
    def data(self) -> bytes:
        return self.data_loader.load()

    @classmethod
    def from_content_digest(cls, zip_file: zipfile.ZipFile, content_digest: ContentDigest) -> 'Content':
        return cls(
            data_loader=ZipLoader(zip_file, content_digest),
        )

    @classmethod
    def from_path(cls, path: Path) -> 'Content':
        return cls(
            data_loader=PathLoader(path),
        )
