from dataclasses import dataclass, asdict

@dataclass
class CustomObject(object):
  def to_dict(self):
    return asdict(self)