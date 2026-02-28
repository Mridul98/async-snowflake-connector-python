from typing import Annotated, Literal
from pydantic import StringConstraints

IdentifierType = Annotated[
    str,
    StringConstraints(
        pattern=r'^"([^"]|"")+"|[a-zA-Z_][a-zA-Z0-9_$]*$'
    )
]

CopyRegexType = Annotated[
    str,
    StringConstraints(
        pattern=r'(?i)^COPY INTO .*'
    )
]

AccountEdition = Literal["STANDARD", "ENTERPRISE", "BUSINESS_CRITICAL"]
LogLevel = Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "OFF"]

DatabaseKind = Literal["PERMANENT", "TRANSIENT"]

TraceLevel = Literal["ALWAYS", "ON_EVENT", "OFF"]

Role = Literal["ROLE", "DATABASE_ROLE", ""]

