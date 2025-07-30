from . import blsct
from .managed_obj import ManagedObj
from .serializable import Serializable
from .pretty_printable import PrettyPrintable
from typing import Any, Optional, override, Self 

class Scalar(ManagedObj, Serializable, PrettyPrintable):
  """
  Represents an element of the finite field :math:`\\mathbb{F}_r`, where :math:`r` is the order of the generator point of the BLS12-381 G1 group.

  A wrapper of MclScalar_ in navio-core.

  .. _MclScalar: https://github.com/nav-io/navio-core/blob/master/src/blsct/arith/mcl/mcl_scalar.h

  Instantiating a Scalar without a parameter is equivalent to calling Scalar.random().

  >>> from blsct import Scalar
  >>> a = Scalar(123)
  >>> a.to_int()
  123
  >>> a.to_hex()
  '7b'
  >>> b = Scalar.random()
  >>> b.to_hex()  # doctest: +SKIP
  '2afe6b2a5222bf5768ddbdbe3e5ea71e964d5312a2761a165395ad231b710edd'
  >>> Scalar().to_hex()
  '5e6efdcf00ce467de29a970adf3a09f8c93e51dc7f1405bbe9dffeeabf952fbe'
  >>> Scalar.zero().to_hex()
  '0'
  >>> c = Scalar(0x1234567890)
  >>> c
  Scalar(1234567890)
  >>> Scalar.deserialize(c.serialize())
  Scalar(1234567890)
  >>> a == b
  False
  >>> a == a
  True
  """
  def __init__(self, value: Optional[Any] = None):
    if isinstance(value, int):
      rv = blsct.gen_scalar(value)
      super().__init__(rv.value)
    elif value is None:
      super().__init__()
    elif isinstance(value, object):
      super().__init__(value)
    else:
      raise ValueError(f"Scalar can only be instantiated with int, but got '{type(value).__name__}'")

  def serialize(self) -> str:
    """Serialize the scalar to a hexadecimal string"""
    return blsct.scalar_to_hex(self.value())
    
  @classmethod
  def deserialize(cls, hex: str) -> Self:
    """Deserialize the scalar from a hexadecimal string"""
    if len(hex) % 2 != 0:
      hex = f"0{hex}"
    rv = blsct.hex_to_scalar(hex)
    rv_result = int(rv.result)
    if rv_result != 0:
      blsct.free_obj(rv)
      raise RuntimeError(f"Deserializaiton failed. Error code = {rv_result}")  # pragma: no co
    return cls.from_obj(rv.value)

  @classmethod
  def random(cls) -> Self:
    """Generate a random scalar"""
    rv = blsct.gen_random_scalar()
    scalar = cls(rv.value)
    blsct.free_obj(rv)
    return scalar

  def to_int(self) -> int:
    """Convert the scalar to an integer"""
    return  blsct.scalar_to_uint64(self.value())

  def pretty_print(self) -> str:
    """Convert the scalar to a string representation"""
    return blsct.scalar_to_str(self.value())

  @override
  def __eq__(self, other: object) -> bool:
    if isinstance(other, Scalar):
      return bool(blsct.is_scalar_equal(self.value(), other.value()))
    else:
      return False

  @classmethod
  def zero(cls) -> Self:
    """Return a zero scalar"""
    return cls(0)

  @override
  def value(self) -> Any:
    return blsct.cast_to_scalar(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    rv = blsct.gen_random_scalar()
    obj = rv.value
    blsct.free_obj(rv)
    return obj

