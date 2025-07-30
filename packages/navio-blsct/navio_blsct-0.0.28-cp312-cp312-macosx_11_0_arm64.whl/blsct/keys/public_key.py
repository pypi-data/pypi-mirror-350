from .. import blsct
from ..managed_obj import ManagedObj
from ..point import Point
from ..scalar import Scalar
from ..serializable import Serializable
from ..pretty_printable import PrettyPrintable
from .child_key_desc.tx_key_desc.view_key import ViewKey
from typing import Any, override, Self, Type

class PublicKey(ManagedObj, Serializable, PrettyPrintable):
  """
  Represents an element in the BLS12-381 G1 curve group that is used as a public key.

  >>> from blsct import Point, PublicKey, Scalar, ViewKey
  >>> s = Scalar.random()
  >>> PublicKey.from_scalar(s)
  PublicKey(<Swig Object of type 'BlsctPubKey *' at 0x100a52d60>)  # doctest: +SKIP 
  >>> p = Point.random()
  >>> PublicKey.from_point(p)
  PublicKey(<Swig Object of type 'BlsctPubKey *' at 0x100a52d60>)  # doctest: +SKIP 
  >>> PublicKey.random()
  PublicKey(<Swig Object of type 'void *' at 0x100af72a0>)  # doctest: +SKIP
  >>> pk = PublicKey.random()
  >>> pk.pretty_print()
  '1 ef5c80c516...  $ doctest +SKIP
  >>> vk = ViewKey()
  >>> PublicKey.generate_nonce(pk, vk)
  PublicKey(<Swig Object of type 'BlsctPubKey *' at 0x10120fba0>)  # doctest: +SKIP
  >>> PublcKey.random().get_point()
  Point(1 e0e85458a6a7a...)  # doctest: +SKIP
  >>> pk2 = PublicKey.random()
  >>> pk == pk2
  False
  >>> pk == pk
  True
  >>> pk.deserialize(pk.serialize())
  PublicKey('1 16ddc1d...29dc3da')
  """
  def get_point(self) -> Point:
    """Return the underlying point of the public key."""
    blsct_point = blsct.get_public_key_point(self.value())
    return Point.from_obj(blsct_point)

  @classmethod
  def random(cls: Type[Self]) -> Self:
    """Get a random public key"""
    rv = blsct.gen_random_public_key()
    pk = cls(rv.value)
    blsct.free_obj(rv)
    return pk

  @classmethod
  def from_point(cls: Type[Self], point: Point) -> Self:
    """Convert a point to a public key"""
    blsct_pub_key = blsct.point_to_public_key(point.value())
    return cls(blsct_pub_key)

  @classmethod
  def from_scalar(cls: Type[Self], scalar: Scalar) -> Self:
    """Convert a scalar to a public key"""
    blsct_pub_key = blsct.scalar_to_pub_key(scalar.value())
    return cls(blsct_pub_key)

  @classmethod
  def generate_nonce(
    cls: Type[Self],
    blinding_pub_key: Self,
    view_key: ViewKey
  ) -> Self:
   """Generate a nonce PublicKey from blinding public key and view key"""
   blsct_nonce = blsct.calc_nonce(
     blinding_pub_key.value(),
     view_key.value()
   )
   return cls(blsct_nonce)

  @override
  def value(self):
    return blsct.cast_to_pub_key(self.obj)

  @classmethod
  @override
  def default_obj(cls) -> Any:
    rv = blsct.gen_random_public_key()
    obj = rv.value
    blsct.free_obj(rv)
    return obj

  @override
  def serialize(self) -> str:
    """Serialize the PublicKey to a hexadecimal string"""
    return self.get_point().serialize()

  @classmethod
  @override
  def deserialize(cls, hex: str) -> Self:
    """Deserialize the PublicKey from a hexadecimal string"""
    p = Point.deserialize(hex)
    return cls.from_point(p)

  @override
  def pretty_print(self) -> str:
    """Convert the PublicKey to a human-readable string representation"""
    return self.get_point().pretty_print()

  @override
  def __eq__(self, other: object) -> bool:
    if isinstance(other, PublicKey):
      return self.get_point() == other.get_point()
    else:
      return False

