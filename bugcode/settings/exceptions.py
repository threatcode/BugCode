"""
Bugcode Penetration Test IDE
Copyright (C) 2021  Threatcode LLC (https://threatcode.github.io/bugcode/)
See the file 'doc/LICENSE' for the license information
"""


class MissingConfigurationError(Exception):
    """Raised when setting configuration is missing"""
    pass


class InvalidConfigurationError(Exception):
    """Raised when setting configuration is invalid"""
    pass
