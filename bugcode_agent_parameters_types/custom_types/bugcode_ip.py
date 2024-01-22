from typing import Union
from ..bugcode_agent_parameters_types import TypeSchema
from marshmallow import fields
from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv6Address


@dataclass
class BugcodeIP:
    data: Union[IPv4Address, IPv6Address] = IPv4Address("127.0.0.1")
    class_name: str = field(default="ip", init=False)
    base: str = field(default="string", init=False)


class BugcodeIPSchema(TypeSchema):
    data = fields.IP()
    type = BugcodeIP
