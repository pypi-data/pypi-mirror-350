from . import blsct
from .managed_obj import ManagedObj
from typing import Any, override, Self, Type

class TokenId(ManagedObj):
  """
  Represents a token ID. A token ID consists of two parameters: token and subid, both of which are optional. When omitted, default values are used instead of random values.

  >>> from blsct import TokenId
  >>> TokenId()
  TokenId(<Swig Object of type 'void *' at 0x101738e10>)  # doctest: +SKIP
  >>> TokenId.from_token(123)
  TokenId(<Swig Object of type 'void *' at 0x10063ced0>)  # doctest: +SKIP
  >>> token_id = TokenId.from_token_and_subid(123, 456)
  >>> token_id.token()
  123
  >>> token_id.subid()
  456
  """
  @classmethod
  def from_token(cls: Type[Self], token: int) -> Self:
    """Generate a token ID from a given token."""
    rv = blsct.gen_token_id(token);
    token_id = cls(rv.value)
    blsct.free_obj(rv)
    return token_id
 
  @classmethod
  def from_token_and_subid(
    cls: Type[Self],
    token: int,
    subid: int,
  ) -> Self:
    """Generate a token ID from a given token and subid."""
    rv = blsct.gen_token_id_with_subid(token, subid) 
    token_id = cls(rv.value)
    blsct.free_obj(rv)
    return token_id

  def token(self) -> int:
    """Get the token from the token ID."""
    return blsct.get_token_id_token(self.value())

  def subid(self) -> int:
    """Get the subid from the token ID."""
    return blsct.get_token_id_subid(self.value())

  @override
  def value(self):
    return blsct.cast_to_token_id(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    rv = blsct.gen_default_token_id()
    obj = rv.value
    blsct.free_obj(rv)
    return obj

