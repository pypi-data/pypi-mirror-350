from . import blsct
from .managed_obj import ManagedObj
from typing import Any, override, Self, Type

class SubAddrId(ManagedObj):
  """
  Represents a sub-address ID.

  >>> from blsct import SubAddrId
  >>> SubAddrId.generate(123, 456)
  SubAddrId(<Swig Object of type 'BlsctSubAddrId *' at 0x1017194d0>)
  """
  @classmethod
  def generate(
    cls: type[Self],
    account: int,
    address: int
  ) -> Self:
    """Generate a sub-address ID from an account and an address"""
    obj = blsct.gen_sub_addr_id(account, address);
    return cls(obj)

  @override
  def value(self) -> Any:
    return blsct.cast_to_sub_addr_id(self.obj)

  @classmethod
  @override
  def default_obj(cls: Type[Self]) -> Self:
    raise NotImplementedError(f"Cannot create a SubAddrId without required parameters.")

