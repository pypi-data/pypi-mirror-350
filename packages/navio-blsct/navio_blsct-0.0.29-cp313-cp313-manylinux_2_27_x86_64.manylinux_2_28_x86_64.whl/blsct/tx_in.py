from . import blsct
from .keys.child_key_desc.tx_key_desc.spending_key import SpendingKey
from .managed_obj import ManagedObj
from .out_point import OutPoint
from .script import Script
from .token_id import TokenId
from .tx_id import TxId
from typing import Any, override, Self, Type

class TxIn(ManagedObj):
  """
  Represents a transaction input in a confidential transaction.
  
  >>> from blsct import OutPoint, SpendingKey, TokenId, TxId, TxIn, TX_ID_SIZE
  >>> import secrets
  >>> amount = 123
  >>> gamma = 100
  >>> spending_key = SpendingKey()
  >>> token_id = TokenId()
  >>> tx_id = TxId.from_hex(secrets.token_hex(TX_ID_SIZE))
  >>> out_point = OutPoint.generate(tx_id, 0)
  >>> tx_in = TxIn.generate(amount, gamma, spending_key, token_id, out_point)
  >>> tx_in.get_prev_out_hash()
  TxId(7b0000000000000064000000000000003ff98b71ff7189fb12d4b93704139753)  # doctest: +SKIP
  >>> tx_in.get_prev_out_n()
  37194817  # doctest: +SKIP
  >>> tx_in.get_script_sig()
  Script(341a3e3e18b462d20000000000000000000000000000000000000000)  # doctest: +SKIP
  >>> tx_in.get_sequence()
  0  # doctest: +SKIP
  >>> tx_in.get_script_witness()
  Script(ffffffffffffffff1b585a44e980f30b16ef75db34f7a6d56fe7cee4)  # doctest: +SKIP
  """
  @classmethod
  def generate(
    cls: Type[Self],
    amount: int,
    gamma: int,
    spending_key: SpendingKey,
    token_id: TokenId,
    out_point: OutPoint,
    rbf: bool = False,
  ) -> Self:
    """Generate a transaction input for a confidential transaction."""
    rv = blsct.build_tx_in(
      amount,
      gamma,
      spending_key.value(),
      token_id.value(),
      out_point.value(),
      rbf
    )
    rv_result = int(rv.result)
    if rv_result != 0:
      blsct.free_obj(rv)
      raise ValueError(f"Failed to build TxIn. Error code = {rv_result}")

    obj = cls(rv.value)
    blsct.free_obj(rv)
    return obj

  def get_prev_out_hash(self) -> TxId:
    """Get the transaction ID of the previous output being spent."""
    tx_id = blsct.get_tx_in_prev_out_hash(self.value())
    return TxId(tx_id)

  def get_prev_out_n(self) -> int:
    """Get the output index of the previous output being spent."""
    return blsct.get_tx_in_prev_out_n(self.value())

  def get_script_sig(self) -> Script:
    """Get the scriptSig used to unlock the previous output."""
    script_sig = blsct.get_tx_in_script_sig(self.value())
    return Script(script_sig)

  def get_sequence(self) -> int:
    """Get the sequence field of the transaction input."""
    return blsct.get_tx_in_sequence(self.value())

  def get_script_witness(self) -> Script:
    """Get the scriptWitness for the transaction input."""
    script_witness = blsct.get_tx_in_script_witness(self.value())
    return Script(script_witness)

  @override
  def value(self) -> Any:
    return blsct.cast_to_tx_in(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    raise NotImplementedError("Cannot create a TxIn without required parameters.")

