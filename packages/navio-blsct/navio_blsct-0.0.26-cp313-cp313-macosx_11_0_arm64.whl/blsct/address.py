from . import blsct
from .address_encoding import AddressEncoding
from .keys.double_public_key import DoublePublicKey

class Address():
  """
  Encode and decode address strings from DoublePublicKey objects.

  This class provides static methods to convert between DoublePublicKey objects and their string representations using a specified encoding.

  >>> from blsct import DoublePublicKey, Address, AddressEncoding
  >>> dpk = DoublePublicKey()
  >>> addr = Address.encode(dpk, AddressEncoding.Bech32M)
  >>> addr
  'nv14u7r0xx4n3gca6tm5glcqj54vd9zu8lcj4evscrpv9ujyst4hx9r4d9rtq2r3pmvvn0r05pfs7q6lqh50fp2x0fgt2sa54cc624wplty3qvmgtralvdcujgw6258zffxyn9eex6lvrk9nezguwgztr6xqyn7w6j5wc'  # doctest: +SKIP
  >>> Address.decode(addr)
  DoublePublicKey(<Swig Object of type 'void *' at 0x1005e17d0>)  # doctest: +SKIP
   """
  @staticmethod
  def encode(dpk: DoublePublicKey, encoding: AddressEncoding):
    """Encode a DoublePublicKey to an address string using the specified encoding""" 

    blsct_encoding = None
    if encoding == AddressEncoding.Bech32:
      blsct_encoding = blsct.Bech32
    elif encoding == AddressEncoding.Bech32M:
      blsct_encoding = blsct.Bech32M
    else:
      raise ValueError(f"Unknown encoding: {encoding}")

    dpk = blsct.cast_to_dpk(dpk.obj)
    rv = blsct.encode_address(dpk, blsct_encoding)
    rv_result = int(rv.result)

    if rv_result != 0:
      blsct.free_obj(rv)
      raise ValueError(f"Failed to encode address. Error code = {rv_result}")

    enc_addr = blsct.as_string(rv.value)
    blsct.free_obj(rv)
    return enc_addr

  @staticmethod
  def decode(addr: str):
    """Decode an address string to a DoublePublicKey"""

    rv = blsct.decode_address(addr)
    rv_result = int(rv.result)

    if rv_result != 0:
      blsct.free_obj(rv)
      raise ValueError(f"Failed to decode address. Error code = {rv_result}")

    # move rv.value (blsct_dpk) to DoublePublicKey
    dpk = DoublePublicKey.from_obj(rv.value)
    blsct.free_obj(rv)

    return dpk
