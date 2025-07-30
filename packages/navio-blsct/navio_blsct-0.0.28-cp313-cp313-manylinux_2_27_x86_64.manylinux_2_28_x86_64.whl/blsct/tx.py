from . import blsct
from .managed_obj import ManagedObj
from .serializable import Serializable
from .tx_id import TxId
from .tx_in import TxIn
from .tx_out import TxOut
from typing import Any, override, Self, Type

# stores serialized tx represented as uint8_t*
class Tx(ManagedObj, Serializable):
  """
  Represents a confidential transaction.

  >>> from blsct import ChildKey, DoublePublicKey, OutPoint, PublicKey, SpendingKey, SubAddr, SubAddrId, TokenId, TX_ID_SIZE, Tx, TxId, TxIn, TxOut
  >>> import secrets
  >>> num_tx_in = 1
  >>> num_tx_out = 1
  >>> default_fee = 200000
  >>> fee = (num_tx_in + num_tx_out) * default_fee
  >>> out_amount = 10000
  >>> in_amount = fee + out_amount
  >>> tx_id = TxId.from_hex(secrets.token_hex(32))
  >>> out_index = 0
  >>> out_point = OutPoint.generate(tx_id, out_index)
  >>> gamma = 100
  >>> spending_key = SpendingKey()
  >>> token_id = TokenId()
  >>> tx_in = TxIn.generate(in_amount, gamma, spending_key, token_id, out_point)
  >>> sub_addr = SubAddr.from_double_public_key(DoublePublicKey())
  >>> tx_out = TxOut.generate(sub_addr, out_amount, 'navio')
  >>> tx = Tx.generate([tx_in], [tx_out])
  >>> for tx_in in tx.get_tx_ins(): 
  ...   print(f"prev_out_hash: {tx_in.get_prev_out_hash()}")
  ...   print(f"prev_out_n: {tx_in.get_prev_out_n()}")
  ...   print(f"script_sig: {tx_in.get_script_sig().to_hex()}")
  ...   print(f"sequence: {tx_in.get_sequence()}")
  ...   print(f"script_witness: {tx_in.get_script_witness().to_hex()}")
  ...   
  prev_out_hash: TxId(b1166eabed80a211639e07c9382b905706123e51f35088d7b9ccfb768161adce)  # doctest: +SKIP
  prev_out_n: 0  # doctest: +SKIP
  script_sig: 00000000000000000000000000000000000000000000000000000000  # doctest: +SKIP
  sequence: 4294967295  # doctest: +SKIP
  script_witness: 00000000000000000000000000000000000000000000000000000000  # doctest: +SKIP
  >>> for tx_out in tx.get_tx_outs():
  ...   print(f"value: {tx_out.get_value()}")
  ...   print(f"script_pub_key: {tx_out.get_script_pub_key().to_hex()}")
  ...   print(f"token_id: token={tx_out.get_token_id().token()}, subid={tx_out.get_token_id().subid()}")
  ...   print(f"spending_key: {tx_out.get_spending_key()}")
  ...   print(f"ephemeral_key: {tx_out.get_ephemeral_key()}")
  ...   print(f"blinding_key: {tx_out.get_blinding_key()}")
  ...   print(f"view_tag: {tx_out.get_view_tag()}")
  ...   print(f"range_proof.A: {tx_out.get_range_proof_A().to_hex()}")
  ...   print(f"range_proof.B: {tx_out.get_range_proof_B().to_hex()}")
  ...   print(f"range_Proof.r_prime: {tx_out.get_range_proof_r_prime()}")
  ...   print(f"range_proof.s_prime: {tx_out.get_range_proof_s_prime()}")
  ...   print(f"range_proof.delta_prime: {tx_out.get_range_proof_delta_prime()}")
  ...   print(f"range_proof.alpha_hat: {tx_out.get_range_proof_alpha_hat()}")
  ...   print(f"range_proof.tau_x: {tx_out.get_range_proof_tau_x()}")
  ...   
  value: 0  # doctest: +SKIP
  script_pub_key: 51000000000000000000000000000000000000000000000000000000  # doctest: +SKIP
  token_id: token=0, subid=18446744073709551615  # doctest: +SKIP
  spending_key: Point(1 43c0386c...)  # doctest: +SKIP
  ephemeral_key: Point(1 dbb5418...)  # doctest: +SKIP
  blinding_key: Point(1 11bfe3...)  # doctest: +SKIP
  view_tag: 43421  # doctest: +SKIP
  range_proof.A: 1 d1a9ec...# doctest: +SKIP
  range_proof.B: 1 7f5c8c...# doctest: +SKIP
  range_Proof.r_prime: Point(0)  # doctest: +SKIP
  range_proof.s_prime: Point(0)  # doctest: +SKIP
  range_proof.delta_prime: Point(0)  # doctest: +SKIP
  range_proof.alpha_hat: Point(0)  # doctest: +SKIP
  range_proof.tau_x: Scalar(707fe053abde7620ba50206b52c94f57d8301a70230c97fb0c9bbc10f6660a18)  # doctest: +SKIP
  value: 0  # doctest: +SKIP
  script_pub_key: 51000000000000000000000000000000000000000000000000000000  # doctest: +SKIP
  token_id: token=0, subid=18446744073709551615  # doctest: +SKIP
  spending_key: Point(1 187232...)  # doctest: +SKIP
  ephemeral_key: Point(1 f307fb...)  # doctest: +SKIP
  blinding_key: Point(0)  # doctest: +SKIP
  view_tag: 21881  # doctest: +SKIP
  range_proof.A: 1 731fba...# doctest: +SKIP
  range_proof.B: 1 af830e...# doctest: +SKIP
  range_Proof.r_prime: Point(0)  # doctest: +SKIP
  range_proof.s_prime: Point(0)  # doctest: +SKIP
  range_proof.delta_prime: Point(0)  # doctest: +SKIP
  range_proof.alpha_hat: Point(0)  # doctest: +SKIP
  range_proof.tau_x: Scalar(4193251795eaf35243e68c9fef5dd7cafd3c34bcc0422c5c5b8f825c56767546)  # doctest: +SKIP
  value: 292125  # doctest: +SKIP
  script_pub_key: 6a000000000000000000000000000000000000000000000000000000  # doctest: +SKIP
  token_id: token=0, subid=18446744073709551615  # doctest: +SKIP
  spending_key: Point(0)  # doctest: +SKIP
  ephemeral_key: Point(0)  # doctest: +SKIP
  blinding_key: Point(0)  # doctest: +SKIP
  view_tag: 0  # doctest: +SKIP
  range_proof.A: 0  # doctest: +SKIP
  range_proof.B: 0  # doctest: +SKIP
  range_Proof.r_prime: Point(0)  # doctest: +SKIP
  range_proof.s_prime: Point(0)  # doctest: +SKIP
  range_proof.delta_prime: Point(0)  # doctest: +SKIP
  range_proof.alpha_hat: Point(0)  # doctest: +SKIP
  range_proof.tau_x: Scalar(0)  # doctest: +SKIP
  >>> ser_tx = tx.serialize()
  >>> tx.deserialize(ser_tx)
  Tx(<swig object of type 'unsigned char *' at 0x102529080>)  # doctest: +SKIP
  """

  def __init__(self, obj: Any, obj_size: int):
    self.obj_size = obj_size
    super().__init__(obj)

  @classmethod
  def generate(
    cls: Type[Self],
    tx_ins: list[TxIn],
    tx_outs: list[TxOut]
  ) -> Self:
    """generate a confidential transaction from a list of inputs and outputs."""

    tx_in_vec = blsct.create_tx_in_vec()
    for tx_in in tx_ins:
      blsct.add_tx_in_to_vec(tx_in_vec, tx_in.value())

    tx_out_vec = blsct.create_tx_out_vec()
    for tx_out in tx_outs:
      blsct.add_tx_out_to_vec(tx_out_vec, tx_out.value())

    rv = blsct.build_tx(tx_in_vec, tx_out_vec)
    rv_result = int(rv.result)

    if rv_result == blsct.BLSCT_IN_AMOUNT_ERROR:
      blsct.free_obj(rv)
      raise ValueError(f"Failed to build transaction. tx_ins[{rv.in_amount_err_index}] has an invalid amount")


    if rv_result == blsct.BLSCT_OUT_AMOUNT_ERROR:
      blsct.free_obj(rv)
      raise ValueError(f"Failed to build transaciton. tx_outs[{rv.out_amount_err_index}] has an invalid amount")

    if rv_result != 0:
      blsct.free_obj(rv)
      raise ValueError(f"building tx failed. Error code = {rv_result}")

    obj = cls(rv.ser_tx, rv.ser_tx_size)
    blsct.free_obj(rv)
    return obj

  def get_tx_id(self) -> TxId:
    """Get the transaction ID."""
    tmp_tx = blsct.deserialize_tx(self.value(), self.obj_size)
    tx_id_hex = blsct.get_tx_id(tmp_tx)
    blsct.free_obj(tmp_tx)
    return TxId.deserialize(tx_id_hex)

  def get_tx_ins(self) -> list[TxIn]:
    """Get the transaction inputs."""
    # returns cmutabletransaction*
    blsct_tx = blsct.deserialize_tx(self.value(), self.obj_size)

    blsct_tx_ins = blsct.get_tx_ins(blsct_tx)
    tx_ins_size = blsct.get_tx_ins_size(blsct_tx_ins)

    tx_ins = []
    for i in range(tx_ins_size):
      rv = blsct.get_tx_in(blsct_tx_ins, i)
      tx_in = TxIn(rv.value)
      tx_ins.append(tx_in)
      blsct.free_obj(rv)
    blsct.free_obj(blsct_tx)

    return tx_ins

  def get_tx_outs(self) -> list[TxOut]:
    """Get the transaction outputs."""
    # returns cmutabletransaction*
    blsct_tx = blsct.deserialize_tx(self.value(), self.obj_size)

    blsct_tx_outs = blsct.get_tx_outs(blsct_tx)
    tx_outs_size = blsct.get_tx_outs_size(blsct_tx_outs)

    tx_outs = []
    for i in range(tx_outs_size):
      rv = blsct.get_tx_out(blsct_tx_outs, i)
      tx_out = TxOut(rv.value)
      tx_outs.append(tx_out)
      blsct.free_obj(rv)
    blsct.free_obj(blsct_tx)

    return tx_outs

  @override
  def serialize(self) -> str:
    """Serialize the transaction to a hexadecimal string."""
    return blsct.to_hex(
      blsct.cast_to_uint8_t_ptr(self.value()),
      self.obj_size
    )

  @classmethod
  @override
  def deserialize(cls: Type[Self], hex: str) -> Self:
    """Deserialize a transaction from a hexadecimal string."""
    obj = blsct.hex_to_malloced_buf(hex)
    obj_size = int(len(hex) / 2)
    inst = cls(obj, obj_size) 
    return inst

  @override
  def value(self) -> Any:
    # self.obj is uint8_t*
    return blsct.cast_to_uint8_t_ptr(self.obj)

  @classmethod
  @override
  def default_obj(cls) -> Any:
    raise NotImplementedError("Cannot create a Tx without required parameters.")

