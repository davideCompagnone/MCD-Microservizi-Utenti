"""Application implementation - exceptions."""

from .http import (
    HTTPException,
    http_exception_handler,
)

from .dynamo import (
    DynamoTableDoesNotExist,
    DynamoTableAlreadyExists,
    UserNotFound,
    EmptyTable,
)

__all__ = (
    "HTTPException",
    "http_exception_handler",
    "DynamoTableDoesNotExist",
    "DynamoTableAlreadyExists",
    "UserNotFound",
    "EmptyTable",
)
