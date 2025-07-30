"""
Utilities for signing/integrity, on top of ItsDangerous.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from itsdangerous import TimestampSigner

from suou.iding import Siq

class UserSigner(TimestampSigner):
    """
    Instance itsdangerous.TimestampSigner() from a user ID.

    XXX UNTESTED!!!
    """
    user_id: int
    def __init__(self, master_secret: bytes, user_id: int, user_secret: bytes, **kwargs):
        super().__init__(master_secret + user_secret, salt=Siq(user_id).to_bytes(), **kwargs)
        self.user_id = user_id
    def token(self) -> str:
        return self.sign(Siq(self.user_id).to_base64()).decode('ascii')

