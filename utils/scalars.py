from collections.abc import Callable
from datetime import datetime
from operator import methodcaller

import dateutil.parser
import strawberry
from graphql import GraphQLError


def wrap_parser(parser: Callable, type_: str) -> Callable:
    def inner(value: str):
        try:
            return parser(value)
        except ValueError as e:
            raise GraphQLError(f'Value cannot represent a {type_}: "{value}". {e}') from e

    return inner


isoformat = methodcaller("isoformat")

DateTimeScalar = strawberry.scalar(
    datetime,
    name="DateTimeType",
    description="Date with time (isoformat)",
    serialize=isoformat,
    parse_value=wrap_parser(dateutil.parser.isoparse, "DateTime"),
)
