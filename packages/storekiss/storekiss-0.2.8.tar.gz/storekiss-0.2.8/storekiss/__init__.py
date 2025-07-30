"""
storekiss - A CRUD interface library with SQLite storage.

This library provides a simple interface for storing and retrieving data
using SQLite as the physical storage mechanism, with LiteStore-like indexing
and query capabilities.
"""

__version__ = "0.2.8"

import warnings
from storekiss.crud import (
    LiteStore as _LiteStore,
    Collection,
    Document,
    QueryBuilder,
    SERVER_TIMESTAMP,
)
from storekiss.exceptions import (
    StorekissError,
    ValidationError,
    NotFoundError,
    DatabaseError,
)
from storekiss.validation import (
    FieldValidator,
    StringField,
    NumberField,
    BooleanField,
    DateTimeField,
    ListField,
    MapField,
    BytesField,
    GeoPointField,
    ReferenceField,
    Schema,
)
from storekiss.geopoint import GeoPoint
from storekiss.reference import Reference, reference

from storekiss import litestore
from storekiss.litestore import DELETE_FIELD


class LiteStore(_LiteStore):
    """
    Deprecated: Use litestore.client() instead.

    This class is deprecated and will be removed in a future version.
    Please use the following pattern instead:

    from storekiss import litestore
    db = litestore.client()
    """

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "Direct LiteStore class import is deprecated. "
            "Use 'from storekiss import litestore' and 'db = litestore.client()' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


__all__ = [
    "LiteStore",  # Deprecated
    "Collection",
    "Document",
    "QueryBuilder",
    "SERVER_TIMESTAMP",
    "StorekissError",
    "ValidationError",
    "NotFoundError",
    "DatabaseError",
    "FieldValidator",
    "StringField",
    "NumberField",
    "BooleanField",
    "DateTimeField",
    "ListField",
    "MapField",
    "BytesField",
    "GeoPointField",
    "ReferenceField",
    "Schema",
    "GeoPoint",
    "Reference",
    "reference",
    "litestore",
    "DELETE_FIELD",
]
