"""
Bugcode Penetration Test IDE
Copyright (C) 2019  Threatcode LLC (https://threatcode.github.io/bugcode/)
See the file 'doc/LICENSE' for the license information
"""


def remove_null_characters(string):
    string = string.replace('\x00', '')
    string = string.replace('\00', '')
    string = string.replace('\0', '')
    return string
