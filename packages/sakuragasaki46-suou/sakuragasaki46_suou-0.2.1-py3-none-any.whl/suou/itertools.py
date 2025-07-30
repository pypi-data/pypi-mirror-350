'''
Iteration utilities.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
'''

from typing import Any, Iterable


def makelist(l: Any) -> list:
    '''
    Make a list out of an iterable or a single value.
    '''
    if isinstance(l, (str, bytes, bytearray)):
        return [l]
    elif isinstance(l, Iterable):
        return list(l)
    elif l in (None, NotImplemented, Ellipsis):
        return []
    else:
        return [l]

def kwargs_prefix(it: dict[str, Any], prefix: str) -> dict[str, Any]:
    '''
    Subset of keyword arguments. Useful for callable wrapping.
    '''
    return {k.removeprefix(prefix): v for k, v in it.items() if k.startswith(prefix)}



__all__ = ('makelist', 'kwargs_prefix')
