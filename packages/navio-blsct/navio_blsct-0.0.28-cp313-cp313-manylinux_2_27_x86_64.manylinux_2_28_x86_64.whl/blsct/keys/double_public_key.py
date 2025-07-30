from .. import blsct
from ..managed_obj import ManagedObj
from .public_key import PublicKey
from ..scalar import Scalar
from typing import override, Self, Type

class DoublePublicKey(ManagedObj):
  """
  The unique source from which an address is derived.

  Instantiating a DoublePublicKey object without a parameter returns a DoublePublicKey consisting of two randomly generated PublicKeys.

  >>> from blsct import DoublePublicKey
  >>> DoublePublicKey()
  DoublePublicKey(<Swig Object of type 'void *' at 0x1011cb960>)  # doctest: +SKIP
  """
  def __init__(self, obj=None):
    super().__init__(obj)

  @classmethod
  def from_public_keys(
    cls: Type[Self],
    pk1: PublicKey,
    pk2: PublicKey,
  ) -> Self:
    """Create a DoublePublicKey from two PublicKeys."""
    rv = blsct.gen_double_pub_key(pk1.value(), pk2.value())
    dpk = cls(rv.value)
    blsct.free_obj(rv)
    return dpk

  @classmethod
  def from_keys_and_acct_addr(
    cls: Type[Self],
    view_key: Scalar,
    spending_pub_key: PublicKey,
    account: int,
    address: int
  ) -> Self:
    """Create a DoublePublicKey from a view key, spending public key, account, and address."""
    obj = blsct.gen_dpk_with_keys_and_sub_addr_id(
      view_key.value(),
      spending_pub_key.value(),
      account,
      address
    )
    return cls(obj) 

  @override
  def value(self):
    return blsct.cast_to_dpk(self.obj)

  @override
  @classmethod
  def default_obj(cls: Type[Self]) -> Self:
    pk1 = PublicKey()
    pk2 = PublicKey()
    tmp = DoublePublicKey.from_public_keys(pk1, pk2)
    obj = tmp.move()
    return obj

