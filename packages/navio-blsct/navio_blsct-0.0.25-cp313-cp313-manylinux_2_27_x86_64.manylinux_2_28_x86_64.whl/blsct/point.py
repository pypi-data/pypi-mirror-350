from . import blsct
from .managed_obj import ManagedObj
from .serializable import Serializable
from .pretty_printable import PrettyPrintable
from typing import Any, override, Self, Type

class Point(ManagedObj, Serializable, PrettyPrintable):
  """
  Represents an element in the BLS12-381 G1 curve group.
  A wrapper of MclG1Point_ in navio-core.

  .. _MclG1Point: https://github.com/nav-io/navio-core/blob/master/src/blsct/arith/mcl/mcl_g1point.h

  Instantiating a Point object without a parameter returns the base point of the BLS12-381 G1 curve.

  >>> from blsct import Point
  >>> a = Point()
  >>> a.serialize()
  '1 124c3c9dc6eb46cf8bcddc64559c05717d49730c9e474230dfd75e76c7ac07f954bfcf60432a9175d1eb0d54e502301b 2cbaf...'  # doctest: +SKIP
  >>> b = Point.base_point()
  >>> a.serialize() == b.serialize()
  True
  >>> a.is_valid()
  True
  >>> Point.random().serialize()
  '1 124c3c9dc6eb46cf8bcddc64559c05717d49730c9e474230dfd75e76c7ac07f954bfcf60432a9175d1eb0d54e502301b 2cbaf...'  # doctest: +SKIP
  """

  @classmethod
  def random(cls: Type[Self]) -> Self:
    """Generate a random point"""
    rv = blsct.gen_random_point()
    point = cls.from_obj(rv.value)
    blsct.free_obj(rv)
    return point

  @classmethod
  def base(cls: Type[Self]) -> Self:
    """Get the base point of the BLS12-381 G1 curve"""
    rv = blsct.gen_base_point()
    point = cls.from_obj(rv.value)
    blsct.free_obj(rv)
    return point

  def is_valid(self) -> bool:
    """Check if the point is valid"""
    return blsct.is_valid_point(self.value())

  @override
  def serialize(self) -> str:
    """Serialize the point to a hexadecimal string"""
    return blsct.point_to_hex(self.value())

  @classmethod
  @override
  def deserialize(cls, hex: str) -> Self:
    """Deserialize the point from a hexadecimal string"""
    rv = blsct.hex_to_point(hex)
    rv_result = int(rv.result)
    if rv_result != 0:
      blsct.free_obj(rv)
      raise RuntimeError(f"Deserializaiton failed. Error code = {rv_result}")  # pragma: no co
    return cls.from_obj(rv.value)

  @override
  def value(self) -> Any:
    return blsct.cast_to_point(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    rv = blsct.gen_base_point()
    obj = rv.value
    blsct.free_obj(rv)
    return obj 
 
  def pretty_print(self) -> str:
    """Convert the point to a string representation"""
    return blsct.point_to_str(self.value())

  @override
  def __eq__(self, other: object) -> bool:
    if isinstance(other, Point):
      return bool(blsct.is_point_equal(self.value(), other.value()))
    else:
      return False

