from ..bugcode_agent_parameters_types import TypeSchema
from marshmallow import fields, ValidationError, validates
from dataclasses import dataclass, field


@dataclass
class BugcodeString:
    data: str = str()
    class_name: str = field(default="string", init=False)
    base: str = field(default="string", init=False)


class BugcodeStringSchema(TypeSchema):
    data = fields.String()
    type = BugcodeString

    @validates("data")
    def validate_length_characters(self, text):
        if len(text) > 256:
            raise ValidationError(f"Max length 256. Your text {len(text)}")
