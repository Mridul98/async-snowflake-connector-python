from typing import Annotated , Literal
from pydantic import StringConstraints

AccountName = Annotated[
    str,
    StringConstraints(pattern=r'^"([^"]|"")+"|[a-zA-Z_][a-zA-Z0-9_$]*$')
]

AccountEdition = Literal["STANDARD", "ENTERPRISE", "BUSINESS_CRITICAL"]