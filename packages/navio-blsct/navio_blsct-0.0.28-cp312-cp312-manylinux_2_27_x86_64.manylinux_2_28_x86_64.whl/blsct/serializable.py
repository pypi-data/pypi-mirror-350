from typing import Protocol, runtime_checkable, Self, Type

@runtime_checkable
class Serializable(Protocol):
  def serialize(self) -> str: ...

  @classmethod
  def deserialize(cls: Type[Self], hex: str) -> Self: ...

