from typing import Annotated

from annotated_types import Gt, Ge
from pydantic import BaseModel, Field


class BcpOptions(BaseModel):
    """
    Represents options you can pass to the bcp command.
    default to no options.

    If you have an option you want to be supported, see https://gitlab.com/noamfisher/simple_bcp/-/issues/?label_name%5B%5D=support%20bcp%20option
    """
    batch_size: Annotated[int, Gt(0)] | None = Field(
        default=None,
        description="The number of rows per batch of downloaded data")
    packet_size: Annotated[int, Gt(0)] | None = Field(
        default=None,
        description="the number of bytes, per network packet, sent to and from the server")
    errors_tolerance: Annotated[int, Ge(0)] | None = Field(
        default=0,
        description="The number of errors allowed before stopping. errors_tolerance=1 means 1 error is OK, 2 is not. defaults to 0 errors, None means use bcp default",
    )

    @property
    def command_options(self) -> dict[str, str | None]:
        command_options: dict[str, str] = {}
        if self.batch_size is not None:
            command_options["-b"] = str(self.batch_size)
        if self.packet_size is not None:
            command_options["-a"] = str(self.packet_size)
        if self.errors_tolerance is not None:
            # bcp documentation is misleading here
            # "Specifies the maximum number of syntax errors that can occur *before* the bcp operation is canceled".
            # This is not the case in practice. instead, `-m 0` tolerate infinitesimal number of errors,
            # and `-m 1` fails on the first error.
            command_options["-m"] = str(self.errors_tolerance + 1)
        return command_options
