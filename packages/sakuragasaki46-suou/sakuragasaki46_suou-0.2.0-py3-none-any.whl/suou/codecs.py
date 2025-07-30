"""
Coding/decoding utilities (e.g. Base64).

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

import base64
import enum
import re

from suou.functools import not_implemented

B32_TO_CROCKFORD = str.maketrans(
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
    '0123456789ABCDEFGHJKMNPQRSTVWXYZ',
    '=')

CROCKFORD_TO_B32 = str.maketrans(
    '0123456789ABCDEFGHJKMNPQRSTVWXYZ',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
    '=')

def cb32encode(val: bytes) -> str:
    '''
    Encode bytes in Crockford Base32.
    '''
    return base64.b32encode(val).decode('ascii').translate(B32_TO_CROCKFORD)


def cb32decode(val: bytes | str) -> str:
    '''
    Decode bytes from Crockford Base32.
    '''
    if isinstance(val, str):
        val = val.encode('ascii')
    return base64.b32decode(val.upper().translate(CROCKFORD_TO_B32) + b'=' * ((5 - len(val) % 5) % 5))

def b32lencode(val: bytes) -> str:
    '''
    Encode bytes as a lowercase base32 string, with trailing '=' stripped.
    '''
    return base64.b32encode(val).decode('ascii').rstrip('=').lower()

def b32ldecode(val: bytes | str) -> bytes:
    '''
    Decode a lowercase base32 encoded byte sequence. Padding is managed automatically.
    '''
    if isinstance(val, str):
        val = val.encode('ascii')
    return base64.b32decode(val.upper() + b'=' * ((5 - len(val) % 5) % 5))

def b64encode(val: bytes, *, strip: bool = True) -> str:
    '''
    Wrapper around base64.urlsafe_b64encode() which also strips trailing '=' and leading 'A'.
    '''
    b = base64.urlsafe_b64encode(val).decode('ascii')
    return b.lstrip('A').rstrip('=') if strip else b

def b64decode(val: bytes | str) -> bytes:
    '''
    Wrapper around base64.urlsafe_b64decode() which deals with padding.
    '''
    if isinstance(val, str):
        val = val.encode('ascii')
    return base64.urlsafe_b64decode(val.replace(b'/', b'_').replace(b'+', b'-') + b'=' * ((4 - len(val) % 4) % 4))

class StringCase(enum.Enum):
    """
    Enum values used by regex validators and storage converters.

    AS_IS = case sensitive
    LOWER = case insensitive, force lowercase
    UPPER = case insensitive, force uppercase
    IGNORE = case insensitive, leave as is, use lowercase in comparison
    IGNORE_UPPER = same as above, but use uppercase il comparison
    """
    AS_IS = 0
    LOWER = FORCE_LOWER = 1
    UPPER = FORCE_UPPER = 2
    ## difference between above and below is in storage and representation.
    IGNORE_LOWER = IGNORE = 3
    IGNORE_UPPER = 4

    def transform(self, s: str) -> str:
        match self:
            case self.AS_IS:
                return s
            case self.LOWER | self.IGNORE_LOWER:
                return s.lower()
            case self.UPPER | self.IGNORE_UPPER:
                return s.upper()

    def compile(self, exp: str) -> re.Pattern:
        r_flags = 0
        if self in (self.IGNORE, self.IGNORE_UPPER):
            r_flags |= re.IGNORECASE
        return re.compile(exp, r_flags)
        

__all__ = (
    'cb32encode', 'cb32decode', 'b32lencode', 'b32ldecode', 'b64encode', 'b64decode',
    'StringCase'
)