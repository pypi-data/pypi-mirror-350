from . import blsct
from .keys.child_key_desc.tx_key_desc.spending_key import SpendingKey
from .managed_obj import ManagedObj
from .point import Point
from .scalar import Scalar
from .script import Script
from .sub_addr import SubAddr
from .token_id import TokenId
from typing import Any, Optional, Literal, override, Self, Type

TxOutputType = Literal["Normal", "StakedCommitment"]

class TxOut(ManagedObj):
  """
  Represents a transaction output in a confidential transaction.

  A standalone :class:`TxOut` object contains placeholder values.
  Refer to :class:`Tx` for examples of how its fields are populated in a full transaction.

  >>> from blsct import ChildKey, DoublePublicKey, PublicKey, SubAddr, SubAddrId, TxOut
  >>> view_key = ChildKey().to_tx_key().to_view_key()
  >>> spending_pub_key = PublicKey()
  >>> sub_addr = SubAddr.from_double_public_key(DoublePublicKey())
  >>> amount = 789
  >>> memo = "apple"
  >>> TxOut.generate(sub_addr, amount, memo)
  TxOut(<Swig Object of type 'void *' at 0x1015fa760>)  # doctest: +SKIP
  """
  @classmethod
  def generate(
    cls: Type[Self],
    sub_addr: SubAddr,
    amount: int,
    memo: str,
    token_id: Optional[TokenId] = None,
    output_type: TxOutputType = 'Normal',
    min_stake: int = 0,
  ) -> Self:
    """Generate a transaction output for a confidential transaction."""
    token_id = TokenId() if token_id is None else token_id

    rv = blsct.build_tx_out(
      sub_addr.value(),
      amount,
      memo,
      token_id.value(),
      blsct.Normal if output_type == "Normal" else blsct.StakedCommitment,
      min_stake
    )
    rv_result = int(rv.result)
    if rv_result != 0:
      blsct.free_obj(rv)
      raise ValueError(f"Failed to build TxOut. Error code = {rv_result}")

    obj = cls(rv.value)
    blsct.free_obj(rv)
    return obj

  def get_value(self) -> int:
    """Get the value of the transaction output."""
    return blsct.get_tx_out_value(self.value())

  def get_script_pub_key(self) -> Script:
    """Get the scriptPubKey of the transaction output."""
    obj = blsct.get_tx_out_script_pubkey(self.value())
    return Script(obj)

  def get_spending_key(self) -> Point:
    """Get the spending key of the transaction output."""
    obj = blsct.get_tx_out_spending_key(self.value())
    return Point(obj)

  def get_ephemeral_key(self) -> Point:
    """Get the ephemeral key of the transaction output."""
    obj = blsct.get_tx_out_ephemeral_key(self.value())
    return Point(obj)

  def get_blinding_key(self) -> Point:
    """Get the blinding key of the transaction output."""
    obj = blsct.get_tx_out_blinding_key(self.value())
    return Point(obj)

  def get_view_tag(self) -> int:
    """Get the view tag of the transaction output."""
    return blsct.get_tx_out_view_tag(self.value())

  def get_range_proof_A(self) -> Point:
    """Get the range proof element A associated with the transaction output."""
    obj = blsct.get_tx_out_range_proof_A(self.value())
    return Point(obj)

  def get_range_proof_B(self) -> Point:
    """Get the range proof element B associated with the transaction output."""
    obj = blsct.get_tx_out_range_proof_B(self.value())
    return Point(obj)

  def get_range_proof_r_prime(self) -> Scalar:
    """Get the range proof element r associated with the transaction output."""
    obj = blsct.get_tx_out_range_proof_r_prime(self.value())
    return Scalar(obj)

  def get_range_proof_s_prime(self) -> Scalar:
    """Get the range proof element s' associated with the transaction output."""
    obj = blsct.get_tx_out_range_proof_s_prime(self.value())
    return Scalar(obj)

  def get_range_proof_delta_prime(self) -> Scalar:
    """Get the range proof element delta' associated with the transaction output."""
    obj = blsct.get_tx_out_range_proof_delta_prime(self.value())
    return Scalar(obj)

  def get_range_proof_alpha_hat(self) -> Scalar:
    """Get the range proof element alpha hat associated with the transaction output."""
    obj = blsct.get_tx_out_range_proof_alpha_hat(self.value())
    return Scalar(obj)

  def get_range_proof_tau_x(self) -> Scalar:
    """Get the range proof element tau x associated with the transaction output."""
    obj = blsct.get_tx_out_range_proof_tau_x(self.value())
    return Scalar(obj)

  def get_token_id(self) -> TokenId:
    """Get the token ID of the transaction output."""
    obj = blsct.get_tx_out_token_id(self.value())
    return TokenId(obj)

  @override
  def value(self) -> Any:
    return blsct.cast_to_tx_out(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    raise NotImplementedError("Cannot create a TxOut without required parameters.")

