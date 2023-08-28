from operator import methodcaller
from graphql import GraphQLError
import strawberry
import dateutil.parser
from typing import Callable
from datetime import datetime


def wrap_parser(parser: Callable, type_: str) -> Callable:
    def inner(value: str):
        try:
            return parser(value)
        except ValueError as e:
            raise GraphQLError(
                f'Value cannot represent a {type_}: "{value}". {e}')

    return inner


isoformat = methodcaller("isoformat")

DateTimeScalar = strawberry.scalar(
    datetime,
    name="DateTimeType",
    description="Date with time (isoformat)",
    serialize=isoformat,
    parse_value=wrap_parser(dateutil.parser.isoparse, "DateTime"),
)
