from . import blsct
from .managed_obj import ManagedObj
from .scalar import Scalar
from .keys.child_key_desc.tx_key_desc.view_key import ViewKey
from .keys.double_public_key import DoublePublicKey
from .keys.public_key import PublicKey
from .sub_addr_id import SubAddrId
from typing import Any, override, Self, Type

class SubAddr(ManagedObj):
  """
  Represents a sub-address.

  >>> from blsct import ChildKey, DoublePublicKey, PublicKey, SubAddr, SubAddrId
  >>> view_key = ChildKey().to_tx_key().to_view_key()
  >>> spending_pub_key = PublicKey()
  >>> sub_addr_id = SubAddrId.generate(123, 456)
  >>> SubAddr.generate(view_key, spending_pub_key, sub_addr_id)
  SubAddr(<Swig Object of type 'BlsctSubAddr *' at 0x101738e40>)  # doctest: +SKIP
  >>> dpk = DoublePublicKey()
  >>> SubAddr.from_double_public_key(dpk)
  SubAddr(<Swig Object of type 'void *' at 0x101152760>)  # doctest: +SKIP
  """
  @classmethod
  def generate(
    cls: Type[Self],
    view_key: ViewKey,
    spending_pub_key: PublicKey,
    sub_addr_id: SubAddrId,
  ) -> Self:
    """Derive a sub-address from a view key, a spending public key, and a sub-address ID"""
    obj = blsct.derive_sub_address(
      view_key.value(),
      spending_pub_key.value(),
      sub_addr_id.value(),
    )
    return cls(obj)

  @classmethod
  def from_double_public_key(
      cls: Type[Self],
      dpk: DoublePublicKey,
    ) -> Self:
    """Derive a sub-address from a DoublePublicKey"""
    rv = blsct.dpk_to_sub_addr(dpk.value())
    inst = cls(rv.value)
    blsct.free_obj(rv)
    return inst

  @override
  def value(self) -> Any:
    return blsct.cast_to_sub_addr(self.obj)

  @classmethod
  @override
  def default_obj(cls: Type[Self]) -> Self:
    raise NotImplementedError(f"Cannot create a SubAddr without required parameters.")

