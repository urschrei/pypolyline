from collections.abc import Sequence

from typing_extensions import Buffer

def encode_coordinates(
    coords: Buffer | Sequence[Sequence[float]], precision: int
) -> bytes: ...
def decode_polyline(polyline: bytes | str, precision: int) -> list[list[float]]: ...
