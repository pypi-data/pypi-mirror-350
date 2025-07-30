from . import blsct
from .keys.public_key import PublicKey
from .keys.child_key_desc.tx_key_desc.view_key import ViewKey
from .managed_obj import ManagedObj
from typing import Any, override, Self, Type

class HashId(ManagedObj):
  """
  Represents a hash ID consisting of a blinding public key, a spending public key, and a view key.

  >>> from blsct import ChildKey, HashId, PublicKey, ViewKey
  >>> HashId()
  HashId(23f95dc276b53d83b4f3d85b50cce9649240da0f)  # doctest: +SKIP
  >>> blinding_pub_key = PublicKey()
  >>> spending_pub_key = PublicKey()
  >>> view_key = ChildKey().to_tx_key().to_view_key()
  >>> hash_id = HashId.generate(blinding_pub_key, spending_pub_key, view_key)
  >>> hash_id.to_hex()
  '81fe3aefff3e90dcd9862aad1527dc034e5045d4'  # doctest: +SKIP
  """
  @classmethod
  def generate(
    cls: Type[Self],
    blinding_pub_key: PublicKey,
    spending_pub_key: PublicKey,
    view_key: ViewKey
  ) -> Self:
    """Generate a hash ID from blinding public key, spending public key and view key"""
    obj = blsct.calc_hash_id(
      blinding_pub_key.value(),
      spending_pub_key.value(),
      view_key.value()
    )
    return cls(obj)

  def to_hex(self) -> str:
    return blsct.get_key_id_hex(self.value())

  @override
  def value(self) -> Any:
    return blsct.cast_to_key_id(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    blinding_pub_key = PublicKey()
    spending_pub_key = PublicKey()
    view_key = ViewKey()

    return blsct.calc_hash_id(
      blinding_pub_key.value(),
      spending_pub_key.value(),
      view_key.value()
    )

