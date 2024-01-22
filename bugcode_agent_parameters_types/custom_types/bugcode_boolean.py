from ..bugcode_agent_parameters_types import TypeSchema
from marshmallow import fields
from dataclasses import dataclass, field


@dataclass
class BugcodeBoolean:
    data: bool = bool()
    class_name: str = field(default="boolean", init=False)
    base: str = field(default="boolean", init=False)


class BugcodeBooleanSchema(TypeSchema):
    data = fields.Boolean()
    type = BugcodeBoolean
