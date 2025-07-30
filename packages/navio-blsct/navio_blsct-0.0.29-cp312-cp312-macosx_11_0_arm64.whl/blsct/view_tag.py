from . import blsct
from .keys.child_key_desc.tx_key_desc.view_key import ViewKey
from .keys.public_key import PublicKey
from .scalar import Scalar
from typing import Any, Self, Type

class ViewTag():
  """
  Represents a view tag derived from a blinding public key and a view key.

  >>> from blsct import ChildKey, PublicKey, TxKey, ViewTag
  >>> ViewTag()
  ViewTag(0x102cb0c20)  # doctest: +SKIP
  >>> blinding_pub_key = PublicKey()
  >>> view_key = ChildKey().to_tx_key().to_view_key()
  >>> ViewTag.generate(blinding_pub_key, view_key)
  12212  # doctest: +SKIP
  """

  @classmethod
  def generate(
    cls: Type[Self],
    blinding_pub_key: PublicKey,
    view_key: ViewKey
  ) -> Self:
    """Generate a view tag from blinding public key and view key"""
    return blsct.calc_view_tag(
      blinding_pub_key.value(),
      view_key.value()
    )

  def __str__(self):
    name = self.__class__.__name__
    return f"{name}({hex(id(self))})"

  def __repr__(self):
    return self.__str__()

  @classmethod
  def default_obj(cls: Type[Self]) -> Any:
    blinding_pub_key = PublicKey()
    view_key = Scalar.random()

    return blsct.calc_view_tag(
      blinding_pub_key.value(),
      view_key.value()
    )

