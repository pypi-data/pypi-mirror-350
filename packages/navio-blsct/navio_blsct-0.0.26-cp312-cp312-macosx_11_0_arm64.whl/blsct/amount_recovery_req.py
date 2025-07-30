from __future__ import annotations
from .point import Point
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .range_proof import RangeProof

class AmountRecoveryReq:
  """
  A request for recovering a single amount from a non-aggregated range proof.

  Refer to :class:`RangeProof` for a usage example.
  """
  def __init__(
    self,
    range_proof: "RangeProof",
    nonce: Point,
  ):
    self.range_proof = range_proof
    self.nonce = nonce

