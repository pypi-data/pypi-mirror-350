from .. import blsct
from ..scalar import Scalar
from .child_key_desc.tx_key_desc.view_key import ViewKey
from .child_key_desc.tx_key_desc.spending_key import SpendingKey
from .public_key import PublicKey
from typing import Self, Type

class PrivSpendingKey(Scalar):
  """
  Represents a private spending key. A private spending key is a Scalar and introduces no new functionality; it serves purely as a semantic alias.

  >>> from blsct import PrivSpendingKey
  >>> PrivSpendingKey()
  PrivSpendingKey(b75c8edb30507818cb0d4211dd57b09830e1395da700d9b4b43ac360329a908)  # doctest: +SKIP
  """
  @classmethod
  def generate(
    cls: Type[Self],
    blinding_pub_key: PublicKey,
    view_key: ViewKey,
    spending_key: SpendingKey,
    account: int,
    address: int
  ) -> Self:
    blsct_psk = blsct.calc_priv_spending_key(
      blinding_pub_key.value(),
      view_key.value(),
      spending_key.value(),
      account,
      address
    )
    return cls(blsct_psk)

