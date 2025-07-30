import zipfile
import base64
from pathlib import Path
from typing import Dict, Generator, Optional
from packaging.version import Version
from .model.Content import Content
from .model.ContentDigest import ContentDigest
from .enums.DigestHashEnum import DigestHashEnum

class AssetManager:
    _resources_path: Path
    _assets: Dict[str, Content]
    _textures: Dict[str, Path]
    _patterns: Dict[str, Path]

    def __init__(self, resources_path: Path):
        self._resources_path = resources_path
        self._assets = {}
        self._textures = {}
        self._patterns = {}

        self._preload_textures()
        self._preload_patterns()

    def _preload_textures(self) -> None:
        textures_path = self._resources_path.joinpath('textures/')
        for texture in textures_path.glob('*.jpg'):
            self._textures[texture.stem] = texture

    def _preload_patterns(self) -> None:
        textures_path = self._resources_path.joinpath('patterns/')
        for pattern in textures_path.glob('*.png'):
            self._patterns[pattern.stem] = pattern

    def _parse_content_digests(self, content_digests: bytes) -> Generator[ContentDigest, None, None]:
        content = content_digests.decode()
        header = 'ContentDigests-Version: '
        # File format check

        hash_to_enum = {
            'sha-1': DigestHashEnum.SHA_1
        }

        lines = content.split('\n')
        expecting_header = True
        current_block: Dict[str, str] = {}
        for line in lines:
            if expecting_header:
                if not line.startswith(header):
                    raise ValueError('Unknown file format')
                version = Version(line.replace(header, ''))
                if version < Version('1.0'):
                    raise ValueError('Unknown file format version {}'.format(version))
                expecting_header = False
            else:
                # Parse content
                if not line:
                    if current_block:
                        name = current_block.get('name')
                        digest = current_block.get('digest')
                        digest_hash = current_block.get('digest_hash')
                        if not name or not digest or not digest_hash:
                            raise ValueError
                        yield ContentDigest(
                            name=name,
                            digest_hash=hash_to_enum.get(digest_hash, DigestHashEnum.SHA_1),
                            digest=base64.b64decode(digest)
                        )
                        current_block = {}
                    continue

                key_raw, value = line.split(':')
                key = key_raw.strip().lower()
                if key.endswith('-digest'):
                    hash_string, digest = key.rsplit('-', 1)
                    current_block['digest'] = value.strip()
                    current_block['digest_hash'] = hash_string
                else:
                    current_block[key] = value.strip()

    def load_assets(self, zip_file: zipfile.ZipFile) -> None:
        for content_digest in self._parse_content_digests(zip_file.read('ContentDigests')):
            self._assets[content_digest.name] = Content.from_content_digest(zip_file, content_digest)

    def get_asset(self, asset_name: str) -> Optional[Content]:
        return self._assets.get(asset_name)

    def get_asset_by_uri(self, uri: str) -> Optional[Content]:
        if 'file:temp!/' in uri:
            uri = uri.replace('file:temp!/', '')
        return self._assets.get(uri)

    def get_texture(self, texture_name: str) -> Content:
        found = self._textures.get(texture_name)
        if not found:
            raise ValueError('Requested texture {} was not found'.format(texture_name))
        return Content.from_path(found)

    def get_pattern(self, pattern_name: str) -> Content:
        found = self._patterns.get(pattern_name)
        if not found:
            raise ValueError('Requested pattern {} was not found'.format(pattern_name))
        return Content.from_path(found)
