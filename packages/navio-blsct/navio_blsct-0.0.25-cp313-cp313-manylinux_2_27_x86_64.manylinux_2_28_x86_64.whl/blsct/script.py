from . import blsct
from .managed_obj import ManagedObj
from typing import Any, Self, override

class Script(ManagedObj):
  """
  Represents a script, which may be a scriptPubKey, scriptSig, or scriptWitness.

  A :class:`Script` appears as an attribute of :class:`TxOut` (scriptPubKey) or :class:`TxIn` (scriptSig and scriptWitness), and is not meant to be instantiated directly.
  """

  def to_hex(self) -> str:
    """Convert the script to a hexadecimal string."""
    buf = blsct.cast_to_uint8_t_ptr(self.value())
    return blsct.to_hex(buf, blsct.SCRIPT_SIZE)

  @override
  def value(self):
    return blsct.cast_to_uint8_t_ptr(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    raise NotImplementedError("Cannot directly instantiate create a Script without required parameters.")

