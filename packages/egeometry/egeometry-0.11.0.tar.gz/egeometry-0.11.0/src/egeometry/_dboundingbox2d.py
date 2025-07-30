# generated from codegen/templates/_boundingbox2d.py

from __future__ import annotations

__all__ = ["DBoundingBox2d", "DBoundingBox2dOverlappable", "HasDBoundingBox2d"]

from typing import TYPE_CHECKING
from typing import Iterable
from typing import Protocol
from typing import overload

from emath import DVector2

if TYPE_CHECKING:
    from ._dcircle import DCircle
    from ._drectangle import DRectangle
    from ._dtriangle2d import DTriangle2d


class DBoundingBox2dOverlappable(Protocol):
    def overlaps_d_bounding_box_2d(self, other: DBoundingBox2d) -> bool: ...


class HasDBoundingBox2d(Protocol):
    @property
    def bounding_box(self) -> DBoundingBox2d: ...


class DBoundingBox2d:
    __slots__ = ["_extent", "_position", "_size"]

    @overload
    def __init__(self, position: DVector2, size: DVector2) -> None: ...

    @overload
    def __init__(self, *, shapes: Iterable[HasDBoundingBox2d | DVector2]) -> None: ...

    def __init__(
        self,
        position: DVector2 | None = None,
        size: DVector2 | None = None,
        *,
        shapes: Iterable[HasDBoundingBox2d | DVector2] | None = None,
    ):
        if shapes is not None:
            if position is not None:
                raise TypeError("position cannot be supplied with shapes argument")
            if size is not None:
                raise TypeError("size cannot be supplied with shapes argument")
            accum_position: DVector2 | None = None
            accum_extent: DVector2 | None = None
            for s in shapes:
                if isinstance(s, DVector2):
                    p = e = s
                else:
                    p = s.bounding_box.position
                    e = s.bounding_box.extent
                if accum_position is None:
                    accum_position = p
                else:
                    accum_position = DVector2(
                        min(p.x, accum_position.x), min(p.y, accum_position.y)
                    )
                if accum_extent is None:
                    accum_extent = e
                else:
                    accum_extent = DVector2(max(e.x, accum_extent.x), max(e.y, accum_extent.y))
            if accum_position is None:
                position = DVector2(0)
                size = DVector2(0)
            else:
                assert accum_extent is not None
                position = accum_position
                size = accum_extent - accum_position

        assert position is not None
        assert size is not None
        if size < DVector2(0):
            raise ValueError("each size dimension must be >= 0")
        self._position = position
        self._size = size
        self._extent = self._position + self._size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DBoundingBox2d):
            return False
        return self._position == other._position and self._size == other._size

    def __repr__(self) -> str:
        return f"<BoundingBox2d position={self._position} size={self._size}>"

    def overlaps(self, other: DVector2 | DBoundingBox2dOverlappable) -> bool:
        if isinstance(other, DVector2):
            return self.overlaps_d_vector_2(other)
        try:
            other_overlaps = other.overlaps_d_bounding_box_2d
        except AttributeError:
            raise TypeError(other)
        return other_overlaps(self)

    def overlaps_d_circle(self, other: DCircle) -> bool:
        return other.overlaps_d_bounding_box_2d(self)

    def overlaps_d_rectangle(self, other: DRectangle) -> bool:
        return other.overlaps_d_bounding_box_2d(self)

    def overlaps_d_triangle_2d(self, other: DTriangle2d) -> bool:
        return other.overlaps_d_bounding_box_2d(self)

    def overlaps_d_bounding_box_2d(self, other: DBoundingBox2d) -> bool:
        return not (
            self._position.x >= other._extent.x
            or self._extent.x <= other._position.x
            or self._position.y >= other._extent.y
            or self._extent.y <= other._position.y
        )

    def overlaps_d_vector_2(self, other: DVector2) -> bool:
        return (
            other.x >= self._position.x
            and other.x < self._extent.x
            and other.y >= self._position.y
            and other.y < self._extent.y
        )

    def translate(self, translation: DVector2) -> DBoundingBox2d:
        return DBoundingBox2d(self._position + translation, self._size)

    @property
    def bounding_box(self) -> DBoundingBox2d:
        return self

    @property
    def extent(self) -> DVector2:
        return self._extent

    @property
    def position(self) -> DVector2:
        return self._position

    @property
    def size(self) -> DVector2:
        return self._size
