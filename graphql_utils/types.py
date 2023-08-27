from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from config.authentication import Context

Info = _Info[Context, RootValueType]
