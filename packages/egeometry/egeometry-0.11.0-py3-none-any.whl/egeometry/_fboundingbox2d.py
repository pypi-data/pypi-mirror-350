# generated from codegen/templates/_boundingbox2d.py

from __future__ import annotations

__all__ = ["FBoundingBox2d", "FBoundingBox2dOverlappable", "HasFBoundingBox2d"]

from typing import TYPE_CHECKING
from typing import Iterable
from typing import Protocol
from typing import overload

from emath import FVector2

if TYPE_CHECKING:
    from ._fcircle import FCircle
    from ._frectangle import FRectangle
    from ._ftriangle2d import FTriangle2d


class FBoundingBox2dOverlappable(Protocol):
    def overlaps_f_bounding_box_2d(self, other: FBoundingBox2d) -> bool: ...


class HasFBoundingBox2d(Protocol):
    @property
    def bounding_box(self) -> FBoundingBox2d: ...


class FBoundingBox2d:
    __slots__ = ["_extent", "_position", "_size"]

    @overload
    def __init__(self, position: FVector2, size: FVector2) -> None: ...

    @overload
    def __init__(self, *, shapes: Iterable[HasFBoundingBox2d | FVector2]) -> None: ...

    def __init__(
        self,
        position: FVector2 | None = None,
        size: FVector2 | None = None,
        *,
        shapes: Iterable[HasFBoundingBox2d | FVector2] | None = None,
    ):
        if shapes is not None:
            if position is not None:
                raise TypeError("position cannot be supplied with shapes argument")
            if size is not None:
                raise TypeError("size cannot be supplied with shapes argument")
            accum_position: FVector2 | None = None
            accum_extent: FVector2 | None = None
            for s in shapes:
                if isinstance(s, FVector2):
                    p = e = s
                else:
                    p = s.bounding_box.position
                    e = s.bounding_box.extent
                if accum_position is None:
                    accum_position = p
                else:
                    accum_position = FVector2(
                        min(p.x, accum_position.x), min(p.y, accum_position.y)
                    )
                if accum_extent is None:
                    accum_extent = e
                else:
                    accum_extent = FVector2(max(e.x, accum_extent.x), max(e.y, accum_extent.y))
            if accum_position is None:
                position = FVector2(0)
                size = FVector2(0)
            else:
                assert accum_extent is not None
                position = accum_position
                size = accum_extent - accum_position

        assert position is not None
        assert size is not None
        if size < FVector2(0):
            raise ValueError("each size dimension must be >= 0")
        self._position = position
        self._size = size
        self._extent = self._position + self._size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FBoundingBox2d):
            return False
        return self._position == other._position and self._size == other._size

    def __repr__(self) -> str:
        return f"<BoundingBox2d position={self._position} size={self._size}>"

    def overlaps(self, other: FVector2 | FBoundingBox2dOverlappable) -> bool:
        if isinstance(other, FVector2):
            return self.overlaps_f_vector_2(other)
        try:
            other_overlaps = other.overlaps_f_bounding_box_2d
        except AttributeError:
            raise TypeError(other)
        return other_overlaps(self)

    def overlaps_f_circle(self, other: FCircle) -> bool:
        return other.overlaps_f_bounding_box_2d(self)

    def overlaps_f_rectangle(self, other: FRectangle) -> bool:
        return other.overlaps_f_bounding_box_2d(self)

    def overlaps_f_triangle_2d(self, other: FTriangle2d) -> bool:
        return other.overlaps_f_bounding_box_2d(self)

    def overlaps_f_bounding_box_2d(self, other: FBoundingBox2d) -> bool:
        return not (
            self._position.x >= other._extent.x
            or self._extent.x <= other._position.x
            or self._position.y >= other._extent.y
            or self._extent.y <= other._position.y
        )

    def overlaps_f_vector_2(self, other: FVector2) -> bool:
        return (
            other.x >= self._position.x
            and other.x < self._extent.x
            and other.y >= self._position.y
            and other.y < self._extent.y
        )

    def translate(self, translation: FVector2) -> FBoundingBox2d:
        return FBoundingBox2d(self._position + translation, self._size)

    @property
    def bounding_box(self) -> FBoundingBox2d:
        return self

    @property
    def extent(self) -> FVector2:
        return self._extent

    @property
    def position(self) -> FVector2:
        return self._position

    @property
    def size(self) -> FVector2:
        return self._size
