import dataclasses
from ..enums.DigestHashEnum import DigestHashEnum

@dataclasses.dataclass
class ContentDigest:
    name: str
    digest_hash: DigestHashEnum
    digest: bytes
