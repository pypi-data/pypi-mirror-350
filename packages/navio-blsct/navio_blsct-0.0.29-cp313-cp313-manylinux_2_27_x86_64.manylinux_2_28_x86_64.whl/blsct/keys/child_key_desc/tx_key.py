from ... import blsct
from ...scalar import Scalar
from .tx_key_desc.spending_key import SpendingKey
from .tx_key_desc.view_key import ViewKey

class TxKey(Scalar):
  """
  Represents a tx key. A tx key is a Scalar and introduces no new functionality; it serves purely as a semantic alias. Both SpendingKey and ViewKey are exclusively derived from a TxKey.

  >>> from blsct import TxKey
  >>> k = TxKey()
  >>> k.to_spending_key()
  SpendingKey(5a3d7d4b7e50866f179a4041d5f1cd4e30c28367eb588f227ca41f4418e3087e)  # doctest: +SKIP
  >>> k.to_view_key()
  ViewKey(39fe0f1ec3d1704e1cf4261e0b827cb903800ba60e43bd706e44b749e53d8c0f)  # doctest: +SKIP
  """
  def to_spending_key(self) -> SpendingKey:
    """derive a spending key from the tx key"""
    obj = blsct.from_tx_key_to_spending_key(self.value())
    return SpendingKey(obj)

  def to_view_key(self) -> ViewKey:
    """derive a view key from the tx key"""
    obj = blsct.from_tx_key_to_view_key(self.value())
    return ViewKey(obj)

