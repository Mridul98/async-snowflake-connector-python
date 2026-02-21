from pydantic import StringConstraints
from typing import Annotated, Literal

DatabaseName = Annotated[
    str,
    StringConstraints(
        pattern=r'^"([^"]|"")+"|[a-zA-Z_][a-zA-Z0-9_$]*$'
    )
]

DatabaseKind = Literal["PERMANENT", "TRANSIENT"]

TraceLevel = Literal["ALWAYS", "ON_EVENT", "OFF"]

Role =  Literal["ROLE", "DATABASE_ROLE"]