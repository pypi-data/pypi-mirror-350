import json
from datetime import datetime

import numpy as np
import pytest
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetParameterValue

from dkist_processing_test.models.parameters import TestParameters


@pytest.fixture(scope="session")
def array_file_parameter(
    tmp_path_factory, random_parameter_hdulist, array_parameter_file_object_key
) -> tuple[InputDatasetParameterValue, float, float, float]:
    hdul, mu, std, const = random_parameter_hdulist
    file_path = tmp_path_factory.mktemp("parameters") / array_parameter_file_object_key
    hdul.writeto(file_path)

    value = {
        "bucket": "raw",
        "objectKey": array_parameter_file_object_key,
        "param_path": file_path,
        "is_file": True,
    }

    parameter_value = InputDatasetParameterValue(
        parameter_value_id=1,
        parameter_value=value,
        parameter_value_start_date=datetime(1946, 11, 20),
    )
    return parameter_value, mu, std, const


@pytest.fixture(scope="session")
def message_file_parameter(
    tmp_path_factory, early_file_message_str, early_json_parameter_file_object_key
):

    file_path = tmp_path_factory.mktemp("parameters") / early_json_parameter_file_object_key
    with open(file_path, "w") as f:
        json.dump(early_file_message_str, f)

    value = {
        "bucket": "raw",
        "objectKey": early_json_parameter_file_object_key,
        "param_path": file_path,
        "is_file": True,
    }

    parameter_value = InputDatasetParameterValue(
        parameter_value_id=2,
        parameter_value=value,
        parameter_value_start_date=datetime(1946, 11, 20),
    )
    return parameter_value


@pytest.fixture(scope="session")
def message_parameter(early_value_message_str):

    parameter_value = InputDatasetParameterValue(
        parameter_value_id=3,
        parameter_value=early_value_message_str,
        parameter_value_start_date=datetime(1946, 11, 20),
    )

    return parameter_value


@pytest.fixture(scope="session")
def wavelength_parameter() -> InputDatasetParameterValue:
    value = {"wavelength": [1.0, 2.0, 3.0], "values": ["one", "two", "three"]}

    parameter_value = InputDatasetParameterValue(
        parameter_value_id=4,
        parameter_value=value,
        parameter_value_start_date=datetime(1946, 11, 20),
    )
    return parameter_value


@pytest.fixture(scope="session")
def parameter_dict_with_path(
    array_file_parameter, message_file_parameter, message_parameter, wavelength_parameter
):
    """Enough of an input dataset parameters part to exercise file loading parameters."""
    file_parameter_value, _, _, _ = array_file_parameter

    param_dict = {
        "test_random_data": [file_parameter_value],
        "test_message": [message_parameter],
        "test_message_file": [message_file_parameter],
        "test_wavelength_category": [wavelength_parameter],
    }

    return param_dict


@pytest.fixture(scope="session")
def task_with_parameters(parameter_dict_with_path):
    class TaskWithParameters(WorkflowTaskBase):
        def __init__(
            self,
            recipe_run_id: int,
            workflow_name: str,
            workflow_version: str,
        ):
            super().__init__(
                recipe_run_id=recipe_run_id,
                workflow_name=workflow_name,
                workflow_version=workflow_version,
            )
            self.parameters = TestParameters(
                parameter_dict_with_path, wavelength=2.0, obs_ip_start_time="2024-06-11T12:00:00"
            )

        def run(self):
            """Do stuff."""
            pass

    task = TaskWithParameters(
        recipe_run_id=0,
        workflow_name="do_stuff",
        workflow_version="VX.Y",
    )

    return task


def test_parameter(
    task_with_parameters,
    array_file_parameter,
    early_file_message_str,
    early_value_message_str,
):
    """
    Given: A task with parameters that depend on files
    When: Accessing those parameters
    Then: The correct values are returned
    """
    task = task_with_parameters
    _, mu, std, const = array_file_parameter

    assert type(task.parameters.randomness) is tuple
    np.testing.assert_allclose(np.array(task.parameters.randomness), np.array([mu, std]), rtol=1)

    assert task.parameters.constant == const
    assert task.parameters.wavelength_category == "two"
    assert task.parameters.value_message == early_value_message_str
    assert task.parameters.file_message == early_file_message_str
