from .. import blsct
from ..scalar import Scalar
from .child_key_desc.blinding_key import BlindingKey
from .child_key_desc.token_key import TokenKey
from .child_key_desc.tx_key import TxKey
from typing import Type, Self

class ChildKey(Scalar):
  """
  Represents a child key. A child key is a Scalar and introduces no new functionality; it serves purely as a semantic alias. BlindingKey, TokenKey and TxKey are exclusively derived from a ChildKey.

  >>> from blsct import ChildKey, Scalar
  >>> ChildKey()
  ChildKey(3b45fa12345e2d095b5bc0ac0e01edcbb975963897bb5e64b3f9da77b31954d)  # doctest: +SKIP
  >>> s = Scalar()
  >>> k = ChildKey.from_scalar(s)
  >>> k.to_blinding_key()
  BlindingKey(6f4500aab9afcddd48b3e4863529037ec5803b88d36df8c73e231244f5601784)  # doctest: +SKIP
  >>> k.to_token_key()
  TokenKey(672df4f7131c165a9eecf079c45364ff07562fc614b9692daecb58ea6fe54b32)  # doctest: +SKIP
  >>> k.to_tx_key()
  TxKey(3d454890fefe84506a44e6400f38991e884c3d5884cc2b6bed0e41fc62f0d168)  # doctest: +SKIP
  """
  @classmethod
  def from_scalar(
    cls: Type[Self],
    seed: Scalar,
  ) -> Self:
    """create a child key from a scalar"""
    obj = blsct.from_seed_to_child_key(seed.value())
    return cls(obj)

  def to_blinding_key(self) -> BlindingKey:
    """derive a blinding key from the child key"""
    obj = blsct.from_child_key_to_blinding_key(self.value())
    return BlindingKey(obj)

  def to_token_key(self) -> TokenKey:
    """derive a token key from the child key"""
    obj = blsct.from_child_key_to_token_key(self.value())
    return TokenKey(obj)

  def to_tx_key(self) -> TxKey:
    """derive a tx key from the child key"""
    obj = blsct.from_child_key_to_tx_key(self.value())
    return TxKey(obj)

