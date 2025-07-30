from functools import cached_property
from typing import Tuple
import dataclasses

@dataclasses.dataclass
class Color:
    argb: int

    @cached_property
    def rgba(self) -> Tuple[int, int, int, int]:
        a = (self.argb >> 24) & 0xFF
        r = (self.argb >> 16) & 0xFF
        g = (self.argb >> 8) & 0xFF
        b = self.argb & 0xFF
        return r, g, b, a

    @cached_property
    def alpha_float(self) -> float:
        return max(0.0, min(self.rgba[3] / 255.0, 1.0))

    @cached_property
    def hexa(self) -> str:
        r, g, b, a = self.rgba
        return f'#{r:02X}{g:02X}{b:02X}{a:02X}'

    @cached_property
    def hex(self) -> str:
        r, g, b, _a = self.rgba
        return f'#{r:02X}{g:02X}{b:02X}'

    @classmethod
    def from_argb_interger(cls, argb: int) -> 'Color':
        return cls(
            argb=argb
        )

    @classmethod
    def from_hexa(cls, hexa: str) -> 'Color':
        return cls(
            argb=int.from_bytes(bytes.fromhex(hexa))
        )

    @classmethod
    def from_rgba(cls, r: int, g: int, b: int, a: int) -> 'Color':
        return cls(
            argb=((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)
        )
