import json
from datetime import datetime
from random import randint
from typing import Any
from typing import Union

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_serializer
from pydantic import field_validator
from pydantic import model_serializer

param_value_type_hint = Union[
    int, str, list, tuple, "WavelengthParameterValue", "RawFileParameterValue"
]
multi_str_type = Union[str, "MultipleParameterValues"]
multi_file_type = Union["RawFileParameterValue", "MultipleParameterValues"]
multi_wave_type = Union["WavelengthParameterValue", "MultipleParameterValues"]


class ParameterValue(BaseModel):
    """A single parameterValue entry"""

    parameterValue: param_value_type_hint
    parameterValueId: int = Field(default_factory=lambda: randint(1000, 2000))
    parameterValueStartDate: datetime = datetime(1946, 11, 20)

    @field_serializer("parameterValue")
    def json_parameter_value(self, parameter_value: param_value_type_hint) -> str:
        """Encode the actual value in a JSON string."""
        try:
            parameter_value = parameter_value.model_dump()
        except:
            # If the value is just a basic type (i.e., not a `BaseModel`)
            pass
        return json.dumps(parameter_value)

    @field_serializer("parameterValueStartDate")
    def datetime_iso_format(self, start_datetime: datetime) -> str:
        """Encode the start date as an ISO-formatted string."""
        return start_datetime.isoformat()


class MultipleParameterValues(BaseModel):
    """
    Container for a list of parameterValues.

    This exists to be different than a raw `list`, which is a valid `parameterValue.parameterValue` type
    """

    parameter_value_list: list[ParameterValue]

    @field_validator("parameter_value_list", mode="before")
    @classmethod
    def ensure_list_of_parameter_values(cls, input_list: list) -> list[ParameterValue]:
        """Convert any raw types to `ParameterValue` objects."""
        output_list = []
        for parameter_value in input_list:
            if not isinstance(parameter_value, ParameterValue):
                parameter_value = ParameterValue(parameterValue=parameter_value)

            output_list.append(parameter_value)

        return output_list

    @field_validator("parameter_value_list")
    @classmethod
    def no_repeat_start_dates(
        cls, parameter_value_list: list[ParameterValue]
    ) -> list[ParameterValue]:
        """Fail validation if any of the `ParameterValues` have the same `parameterValueStartDate."""
        start_dates = [pv.parameterValueStartDate for pv in parameter_value_list]
        if len(set(start_dates)) != len(start_dates):
            raise ValueError(
                f"parameterValueStartDates must be unique. Got {set(start_dates)} over {len(start_dates)} parameters."
            )

        return parameter_value_list

    @model_serializer
    def parameter_value_list(self):
        """Return just the list of `ParameterValues`."""
        return self.parameter_value_list


class WavelengthParameterValue(BaseModel):
    values: tuple
    wavelength: tuple = (1.0, 2.0, 3.0)


class RawFileParameterValue(BaseModel):
    """
    For parameters that are files on disk.

    "Raw" in the sense that it still has the `__file__`-level dictionary.
    """

    objectKey: str
    bucket: str = "doesn't_matter"

    @model_serializer
    def file_dict(self) -> dict:
        """Wrap the input values in a `__file__` dict."""
        return {"__file__": dict(self)}


class TestParameterValues(BaseModel):
    test_random_data: multi_file_type = RawFileParameterValue(objectKey="")
    test_wavelength_category: multi_wave_type = WavelengthParameterValue(
        values=("one", "two", "three")
    )
    test_message: multi_str_type = "Weird?"
    test_message_file: multi_file_type = RawFileParameterValue(objectKey="")

    model_config = ConfigDict(validate_default=True)

    @field_validator("*")
    @classmethod
    def ensure_parameter_value_lists(cls, parameter: Any) -> MultipleParameterValues:
        """Convert all values to `MultipleParameterValues`, if they aren't already."""
        if not isinstance(parameter, MultipleParameterValues):
            return MultipleParameterValues(parameter_value_list=[parameter])

        return parameter

    @model_serializer
    def input_dataset_document_parameters_part(self) -> list:
        """Place all parameters into higher-level dictionaries required by the input dataset document."""
        return [{"parameterName": f, "parameterValues": v} for f, v in self]
