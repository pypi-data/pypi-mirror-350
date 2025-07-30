"""
Utilities for SQLAlchemy

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from __future__ import annotations

from typing import Callable
import warnings
from sqlalchemy import CheckConstraint, Date, ForeignKey, LargeBinary, Column, MetaData, SmallInteger, String, text
from sqlalchemy.orm import DeclarativeBase, declarative_base as _declarative_base

from suou.itertools import kwargs_prefix

from .signing import UserSigner
from .codecs import StringCase
from .functools import deprecated
from .iding import SiqType, SiqCache
from .classtools import Incomplete, Wanted

# SIQs are 14 bytes long. Storage is padded for alignment
# Not to be confused with SiqType.
IdType = LargeBinary(16)


def sql_escape(s: str, /, dialect: str) -> str:
    """
    Escape a value for SQL embedding, using SQLAlchemy's literal processors.
    Requires a dialect argument.
    """
    if isinstance(s, str):
        return String().literal_processor(dialect=dialect)(s)
    raise TypeError('invalid data type')

def id_column(typ: SiqType, *, primary_key: bool = True):
    """
    Marks a column which contains a SIQ.
    """
    def new_id_factory(owner: DeclarativeBase) -> Callable:
        domain_name = owner.metadata.info['domain_name']
        idgen = SiqCache(domain_name, typ)
        def new_id() -> bytes:
            return idgen.generate().to_bytes()
        return new_id
    if primary_key:
        return Incomplete(Column, IdType, primary_key = True, default = Wanted(new_id_factory))
    else:
        return Incomplete(Column, IdType, unique = True, nullable = False, default = Wanted(new_id_factory))


def match_constraint(col_name: str, regex: str, /, dialect: str = 'default', constraint_name: str | None = None) -> CheckConstraint:
    """
    Shorthand for a check constraint. Several dialects are supported.
    """
    return CheckConstraint(text(match_constraint.TEXT_DIALECTS.get(dialect, match_constraint.TEXT_DIALECTS['default'])).bindparams(n=col_name, re=regex),
            name=constraint_name)

match_constraint.TEXT_DIALECTS = {
    'default': ':n ~ :re',
    'postgresql': ':n ~ :re',
    'mariadb': ':n RLIKE :re'
}

def match_column(length: int, regex: str, /, case: StringCase = StringCase.AS_IS, *args, constraint_name: str | None = None, **kwargs):
    """
    Syntactic sugar to create a String() column with a check constraint matching the given regular expression.

    TODO application side validation
    """
    if case != StringCase.AS_IS: # TODO
        warnings.warn('case arg is currently not working', FutureWarning)
    return Incomplete(Column, String(length), Wanted(lambda x, n: match_constraint(n, regex, #dialect=x.metadata.engine.dialect.name,
            constraint_name=constraint_name or f'{x.__tablename__}_{n}_valid'), *args, **kwargs))


def declarative_base(domain_name: str, master_secret: bytes, metadata: dict | None = None, **kwargs):
    """
    Drop-in replacement for sqlalchemy.orm.declarative_base()
    taking in account requirements for SIQ generation (i.e. domain name).
    """
    if not isinstance(metadata, dict):
        metadata = dict()
    if 'info' not in metadata:
        metadata['info'] = dict()
    metadata['info'].update(
        domain_name = domain_name,
        secret_key = master_secret
    )
    Base = _declarative_base(metadata=MetaData(**metadata), **kwargs)
    return Base
entity_base = deprecated('use declarative_base() instead')(declarative_base)


def token_signer(id_attr: Column | str, secret_attr: Column | str) -> Incomplete[UserSigner]:
    """
    Generate a user signing function.

    Requires a master secret (taken from Base.metadata), a user id (visible in the token)
    and a user secret.
    """
    if isinstance(id_attr, Column):
        id_val = Wanted(id_attr.key)
    elif isinstance(id_attr, str):
        id_val = Wanted(id_attr)
    if isinstance(secret_attr, Column):
        secret_val = Wanted(secret_attr.key)
    elif isinstance(secret_attr, str):
        secret_val = Wanted(secret_attr)
    return Incomplete(UserSigner, Wanted(lambda x, n: x.metadata.info['secret_key']), id_val, secret_val)

def author_pair(fk_name: str, *, id_type: type = IdType, sig_type: type | None = None, nullable: bool = False, sig_length: int | None = 2048, **ka) -> tuple[Column, Column]:
    """
    Return an owner ID/signature column pair, for authenticated values.
    """
    id_ka = kwargs_prefix(ka, 'id_')
    sig_ka = kwargs_prefix(ka, 'sig_')
    id_col = Column(id_type, ForeignKey(fk_name), nullable = nullable, **id_ka)
    sig_col = Column(sig_type or LargeBinary(sig_length), nullable = nullable, **sig_ka)
    return (id_col, sig_col)

def age_pair(*, nullable: bool = False, **ka) -> tuple[Column, Column]:
    """
    Return a SIS-compliant age representation, i.e. a date and accuracy pair.

    Accuracy is represented by a small integer:
    0 = exact
    1 = month and day
    2 = year and month
    3 = year
    4 = estimated year
    """
    date_ka = kwargs_prefix(ka, 'date_')
    acc_ka = kwargs_prefix(ka, 'acc_')
    date_col = Column(Date, nullable = nullable, **date_ka)
    acc_col = Column(SmallInteger, nullable = nullable, **acc_ka)
    return (date_col, acc_col)


__all__ = (
    'IdType', 'id_column', 'entity_base', 'declarative_base', 'token_signer', 'match_column', 'match_constraint',
    'author_pair', 'age_pair'
)