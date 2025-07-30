"""
Utilities for Flask-RestX

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from typing import Mapping
from flask_restx import Api as _Api

class Api(_Api):
    """
    Fix Api() class by remapping .message to .error
    """
    def handle_error(self, e):
        res = super().handle_error(e)
        if isinstance(res, Mapping) and 'message' in res:
            res['error'] = res['message']
            del res['message']
        return res

__all__ = ('Api',)