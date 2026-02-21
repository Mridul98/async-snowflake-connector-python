from pydantic import StringConstraints
from typing import Annotated

DatabaseRoleIdentifier = Annotated[
    str,
    StringConstraints(
        pattern=r'^"([^"]|"")+"|[a-zA-Z_][a-zA-Z0-9_$]*$'
    )
]
