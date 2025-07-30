from . import blsct
from .managed_obj import ManagedObj
from .keys.public_key import PublicKey
from .scalar import Scalar
from typing import Any, override, Self, Type

class Signature(ManagedObj):
  """
  Represents the signature of a transaction.

  >>> from blsct import PublicKey, Scalar, Signature
  >>> sk = Scalar()
  >>> pk = PublicKey.from_scalar(sk)
  >>> sig = Signature.generate(sk, 'navio')
  >>> sig.verify('navio', pk)
  True
  """
  @classmethod
  def generate(cls: Type[Self], priv_key: Scalar, msg: str) -> Self:
    """Generate a signature using a private key and a message."""
    sig = blsct.sign_message(priv_key.value(), msg)
    return cls(sig)

  def verify(self, msg: str, pub_key: PublicKey) -> bool:
    """Verify a signature using the public key corresponding to the private key that signed the transaction."""
    return blsct.verify_msg_sig(pub_key.value(), msg, self.value())

  @override
  def value(self) -> Any:
    return blsct.cast_to_signature(self.obj)

  @classmethod
  @override
  def default_obj(cls: Type[Self]) -> Self:
    raise NotImplementedError(f"Cannot create a Signature without required parameters.")

