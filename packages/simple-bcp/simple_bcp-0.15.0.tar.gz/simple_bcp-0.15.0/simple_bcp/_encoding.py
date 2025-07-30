import enum
import os
from typing import Annotated

from pydantic import BaseModel, model_validator, StringConstraints


class FieldEncodingType(enum.Enum):
    NATIVE = "-n"
    NATIVE_UNICODE = "-N"
    CHAR = "-c"
    UNICODE = "-w"


class BcpEncodingSettings(BaseModel):
    """
    Represents encoding settings to be used by bcp.
    default to `-N` - native Unicode.

    :param field_encoding_type: Specifies the encoding mode of the downloaded data fields.
    :param field_delimiter: the field delimiter of the downloaded data. Defaults to bcp default which is `\t`.
        not supported if `field_encoding_type` is `FieldEncodingMode.NATIVE` or `FieldEncodingMode.NATIVE_UNICODE`.
    :param row_terminator: the row terminator of the downloaded data. Defaults to bcp default which is `\n`.
        not supported if `field_encoding_type` is `FieldEncodingMode.NATIVE` or `FieldEncodingMode.NATIVE_UNICODE`.
    """
    field_encoding_type: FieldEncodingType = FieldEncodingType.NATIVE_UNICODE
    field_delimiter: Annotated[str, StringConstraints(min_length=1)] | None = None
    row_terminator: Annotated[str, StringConstraints(min_length=1)] | None = None

    @model_validator(mode='after')
    def __validate(self):
        if self.field_encoding_type in (FieldEncodingType.NATIVE, FieldEncodingType.NATIVE_UNICODE) and (
                self.field_delimiter is not None or self.row_terminator is not None):
            raise ValueError(
                "field_delimiter and row_terminator are not supported when field_encoding_type is `FieldEncodingMode.NATIVE`")
        return self

    @property
    def command_options(self) -> dict[str, str | None]:
        command_options: dict[str, str | None] = {
            self.field_encoding_type.value: None,
        }
        if self.field_delimiter is not None:
            command_options["-t"] = self.field_delimiter
        if self.row_terminator is not None:
            command_options["-r"] = self.row_terminator
        return command_options

    @classmethod
    def csv_settings(cls) -> 'BcpEncodingSettings':
        return cls(
            field_encoding_type=FieldEncodingType.CHAR,
            field_delimiter=',',
            row_terminator=os.linesep,
        )
