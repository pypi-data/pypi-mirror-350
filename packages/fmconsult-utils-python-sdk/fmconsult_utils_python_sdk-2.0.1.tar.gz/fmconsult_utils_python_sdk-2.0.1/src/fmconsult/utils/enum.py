from enum import Enum

class CustomEnum(Enum):
  @classmethod
  def from_value(cls, value):
    for item in cls:
      if item.value == value:
        return item
    raise ValueError(f"{value} is not a valid value for {cls.__name__}")