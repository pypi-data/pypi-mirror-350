'''
Utilities for working with bits

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
'''

def mask_shift(n: int, mask: int) -> int:
    '''
    Select the bits from n chosen by mask, least significant first.
    '''
    if mask == 0:
        return 0
    elif mask == -1:
        return n
    else:
        i = 0
        while mask & (1 << i) == 0:
            i += 1
        n >>= i
        mask >>= i
        o = 0
        while mask & (1 << o) == 1:
            o += 1
        return (n & ((1 << o) - 1)) | (mask_shift(n >> o, mask >> o) << o)

def count_ones(n: int) -> int:
    '''Count the number of one bits in a number.
    
    Negative numbers count the number of zeroes'''
    if n < 0:
        return ~count_ones(~n)
    ones = 0
    while n not in (-1, 0):
        ones += n & 1
        n >>= 1
    return ones

__all__ = ('count_ones', 'mask_shift')