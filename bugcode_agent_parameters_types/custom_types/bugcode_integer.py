from ..bugcode_agent_parameters_types import TypeSchema
from marshmallow import fields
from dataclasses import dataclass, field


@dataclass
class BugcodeInteger:
    data: int = int()
    class_name: str = field(default="integer", init=False)
    base: str = field(default="integer", init=False)


class BugcodeIntegerSchema(TypeSchema):
    data = fields.Integer()
    type = BugcodeInteger
