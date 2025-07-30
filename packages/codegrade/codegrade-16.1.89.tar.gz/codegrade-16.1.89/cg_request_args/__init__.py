"""This module defines parsers and validators for JSON data.
"""

from ._set import Set
from ._base import Union, Parser, SimpleValue
from ._enum import EnumValue, StringEnum
from ._form import FormURLEncoded
from ._lazy import Lazy
from ._list import List, TwoTuple
from ._query import QueryParam
from ._convert import ConvertCtx, ConvertPriority, as_converter
from ._literal import LiteralBoolean
from ._mapping import (
    FixedMapping, LookupMapping, OnExtraAction, DefaultArgument,
    BaseFixedMapping, OptionalArgument, RequiredArgument, _DictGetter
)
from ._nullable import Nullable
from ._any_value import AnyValue
from ._multipart import (
    MultipartUploadWithData, MultipartUploadWithoutData,
    ExactMultipartUploadWithData
)
from .exceptions import ParseError, SimpleParseError, MultipleParseErrors
from ._rich_value import RichValue
from ._swaggerize import swaggerize
from ._parse_utils import Transform
from ._swagger_utils import OpenAPISchema
