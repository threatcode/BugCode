from ..bugcode_agent_parameters_types import TypeSchema
from marshmallow import fields, ValidationError, validates
from dataclasses import dataclass, field


@dataclass
class BugcodeList:
    data: list = field(default_factory=list)
    class_name: str = field(default="list", init=False)
    base: str = field(default="list", init=False)


class BugcodeListSchema(TypeSchema):
    data = fields.List(fields.Raw())
    type = BugcodeList
    _composed_list = []

    @validates("data")
    def validate_length_characters(self, items):
        for item in items:
            if not isinstance(item, self._composed_list):
                raise ValidationError("Item not valid in list")
