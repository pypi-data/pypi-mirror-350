"""
Tests for the tasks defined in this repo
"""
import json
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import is_dataclass
from datetime import datetime
from datetime import timedelta
from random import randint
from uuid import uuid4

import numpy as np
import pytest
from astropy.io import fits
from dkist_data_simulator.spec122 import Spec122Dataset
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_hdu_decoder
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.codecs.json import json_encoder
from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.constants import ConstantsBase
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_common.tasks import TransferTrialData
from dkist_processing_common.tests.conftest import FakeGQLClient
from dkist_service_configuration.logging import logger

from dkist_processing_test.models.parameters import TestParameters
from dkist_processing_test.tasks import TestQualityL0Metrics
from dkist_processing_test.tasks.exercise_numba import ExerciseNumba
from dkist_processing_test.tasks.fail import FailTask
from dkist_processing_test.tasks.fake_science import GenerateCalibratedData
from dkist_processing_test.tasks.movie import AssembleTestMovie
from dkist_processing_test.tasks.movie import MakeTestMovieFrames
from dkist_processing_test.tasks.noop import NoOpTask
from dkist_processing_test.tasks.write_l1 import WriteL1Data
from dkist_processing_test.tests.conftest import generate_214_l0_fits_frame
from dkist_processing_test.tests.conftest import S122Headers
from dkist_processing_test.tests.parameter_models import MultipleParameterValues
from dkist_processing_test.tests.parameter_models import ParameterValue
from dkist_processing_test.tests.parameter_models import RawFileParameterValue
from dkist_processing_test.tests.parameter_models import TestParameterValues


@dataclass
class FakeConstantDb:
    NUM_DSPS_REPEATS: int = 2
    OBS_IP_START_TIME: str = "1990-06-12T12:00:00"
    INSTRUMENT: str = "TEST"
    AVERAGE_CADENCE: float = 10.0
    MINIMUM_CADENCE: float = 10.0
    MAXIMUM_CADENCE: float = 10.0
    VARIANCE_CADENCE: float = 0.0
    STOKES_PARAMS: tuple[str] = (
        "I",
        "Q",
        "U",
        "V",
    )  # A tuple because lists aren't allowed on dataclasses
    CONTRIBUTING_PROPOSAL_IDS: tuple[str] = ("abc", "def")
    CONTRIBUTING_EXPERIMENT_IDS: tuple[str] = ("ghi", "jkl")


@pytest.fixture()
def noop_task():
    return NoOpTask(recipe_run_id=1, workflow_name="noop", workflow_version="VX.Y")


def test_noop_task(noop_task):
    """
    Given: A NoOpTask
    When: Calling the task instance
    Then: No errors raised
    """
    noop_task()


@pytest.fixture()
def fail_task():
    return FailTask(recipe_run_id=1, workflow_name="fail", workflow_version="VX.Y")


def test_fail_task(fail_task):
    """
    Given: A FailTask
    When: Calling the task instance
    Then: Runtime Error raised
    """
    with pytest.raises(RuntimeError):
        fail_task()


@pytest.fixture()
def generate_calibrated_data_task(
    tmp_path,
    recipe_run_id,
    assign_input_dataset_doc_to_task,
    link_constants_db,
    array_parameter_file_object_key,
    random_parameter_hdulist,
    early_json_parameter_file_object_key,
    early_file_message_str,
    late_json_parameter_file_object_key,
    late_file_message_str,
    early_or_late,
    late_date,
):
    number_of_frames = 10
    if early_or_late == "early":
        obs_ip_start_time_str = (datetime.fromisoformat(late_date) - timedelta(days=30)).isoformat()
    elif early_or_late == "late":
        obs_ip_start_time_str = (datetime.fromisoformat(late_date) + timedelta(days=30)).isoformat()
    link_constants_db(
        recipe_run_id=recipe_run_id,
        constants_obj=FakeConstantDb(
            NUM_DSPS_REPEATS=number_of_frames, OBS_IP_START_TIME=obs_ip_start_time_str
        ),
    )
    with GenerateCalibratedData(
        recipe_run_id=recipe_run_id, workflow_name="GenerateCalibratedData", workflow_version="VX.Y"
    ) as task:
        # configure input data
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        input_frame_set = Spec122Dataset(
            instrument="vbi",
            dataset_shape=(number_of_frames, 512, 512),
            array_shape=(1, 512, 512),
            time_delta=10,
        )
        # load input data
        for idx, input_frame in enumerate(input_frame_set):
            hdu = input_frame.hdu()
            hdu.data = (
                np.ones(hdu.data.shape, dtype=int) * 10
            )  # Because input data will be ints in test system
            hdu.header["DSPSNUM"] = 1
            hdul = fits.HDUList([hdu])
            file_name = f"input_{idx}.fits"
            task.write(
                data=hdul, tags=Tag.input(), relative_path=file_name, encoder=fits_hdulist_encoder
            )

        # Write parameter files
        hdul = random_parameter_hdulist[0]
        task.write(
            data=hdul,
            tags=Tag.parameter(array_parameter_file_object_key),
            encoder=fits_hdulist_encoder,
        )
        task.write(
            data=early_file_message_str,
            tags=Tag.parameter(early_json_parameter_file_object_key),
            encoder=json_encoder,
        )
        task.write(
            data=late_file_message_str,
            tags=Tag.parameter(late_json_parameter_file_object_key),
            encoder=json_encoder,
        )

        # This needs to be after we've written and tagged the parameter files
        assign_input_dataset_doc_to_task(task, obs_ip_start_time=task.constants.obs_ip_start_time)

        # result
        yield task, number_of_frames
        # teardown
        task._purge()
    # disconnect


@pytest.fixture(scope="session")
def input_dataset_document_parameters_part_json(
    array_parameter_file_object_key,
    early_json_parameter_file_object_key,
    late_json_parameter_file_object_key,
    early_value_message_str,
    late_value_message_str,
    early_date,
    late_date,
):

    message_file_values = MultipleParameterValues(
        parameter_value_list=[
            ParameterValue(
                parameterValue=RawFileParameterValue(
                    objectKey=early_json_parameter_file_object_key
                ),
                parameterValueStartDate=early_date,
            ),
            ParameterValue(
                parameterValue=RawFileParameterValue(objectKey=late_json_parameter_file_object_key),
                parameterValueStartDate=late_date,
            ),
        ]
    )
    message_value_values = MultipleParameterValues(
        parameter_value_list=[
            ParameterValue(
                parameterValue=early_value_message_str,
                parameterValueStartDate=early_date,
            ),
            ParameterValue(
                parameterValue=late_value_message_str,
                parameterValueStartDate=late_date,
            ),
        ]
    )
    parameters_obj = TestParameterValues(
        test_random_data=RawFileParameterValue(objectKey=array_parameter_file_object_key),
        test_message_file=message_file_values,
        test_message=message_value_values,
    )

    part_json_str = parameters_obj.model_dump_json()

    return part_json_str


@pytest.fixture(scope="session")
def assign_input_dataset_doc_to_task(
    input_dataset_document_parameters_part_json,
):
    def update_task(task, obs_ip_start_time=None):
        doc_path = task.scratch.workflow_base_path / "dataset_parameters.json"
        with open(doc_path, "w") as f:
            f.write(input_dataset_document_parameters_part_json)
        task.tag(doc_path, Tag.input_dataset_parameters())
        task.parameters = TestParameters(
            task.input_dataset_parameters, wavelength=2.0, obs_ip_start_time=obs_ip_start_time
        )

    return update_task


@pytest.fixture
def link_constants_db():
    return constants_linker


def constants_linker(recipe_run_id: int, constants_obj):
    """Take a dataclass (or dict) containing a constants DB and link it to a specific recipe run id."""
    if is_dataclass(constants_obj):
        constants_obj = asdict(constants_obj)
    constants = ConstantsBase(recipe_run_id=recipe_run_id, task_name="test")
    constants._purge()
    constants._update(constants_obj)
    return


@pytest.mark.parametrize("early_or_late", [pytest.param("early"), pytest.param("late")])
def test_generate_calibrated_data(
    generate_calibrated_data_task,
    early_file_message_str,
    late_file_message_str,
    early_value_message_str,
    late_value_message_str,
    early_or_late,
    mocker,
):
    """
    Given: A GenerateCalibratedData task
    When: Calling the task instance
    Then: Output files are generated for each input file with appropriate tags
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, number_of_frames = generate_calibrated_data_task
    task()
    # Then
    calibrated_frame_hdus = list(
        task.read(tags=[Tag.calibrated(), Tag.frame()], decoder=fits_hdu_decoder)
    )

    if early_or_late == "early":
        expected_file_message = early_file_message_str
        expected_value_message = early_value_message_str
    elif early_or_late == "late":
        expected_file_message = late_file_message_str
        expected_value_message = late_value_message_str

    # Verify frames
    assert len(calibrated_frame_hdus) == number_of_frames
    for hdu in calibrated_frame_hdus:
        assert "VBINMOSC" in hdu.header
        assert "VBICMOSC" in hdu.header

        # Verify correct date params were used
        assert hdu.header["CAM_ID"] == expected_file_message
        assert hdu.header["CAMERA"] == expected_value_message

    # Verify debug frame was written
    debug_frame_paths = list(task.read(tags=[Tag.debug(), Tag.frame()]))
    assert len(debug_frame_paths) == 1
    assert debug_frame_paths[0].exists()


class CommonDataset(Spec122Dataset):
    # NOTE: We use ViSP data for unit tests because ViSP can be polarimetric
    # **BUT** in actual integration tests `*-procesing-test` processes VBI data
    def __init__(self):
        super().__init__(
            array_shape=(1, 10, 10),
            time_delta=1,
            dataset_shape=(2, 10, 10),
            instrument="visp",
            start_time=datetime(2020, 1, 1, 0, 0, 0),
        )

        self.add_constant_key("TELEVATN", 6.28)
        self.add_constant_key("TAZIMUTH", 3.14)
        self.add_constant_key("TTBLANGL", 1.23)
        self.add_constant_key("VISP_012", "bar")
        self.add_constant_key("DKIST004", "observe")
        self.add_constant_key("ID___005", "ip id")
        self.add_constant_key("PAC__004", "Sapphire Polarizer")
        self.add_constant_key("PAC__005", "31.2")
        self.add_constant_key("PAC__006", "clear")
        self.add_constant_key("PAC__007", "6.66")
        self.add_constant_key("PAC__008", "DarkShutter")
        self.add_constant_key("INSTRUME", "VISP")
        self.add_constant_key("WAVELNTH", 1080.0)
        self.add_constant_key("DATE-OBS", "2020-01-02T00:00:00.000")
        self.add_constant_key("DATE-END", "2020-01-03T00:00:00.000")
        self.add_constant_key("ID___013", "PROPOSAL_ID1")
        self.add_constant_key("PAC__002", "clear")
        self.add_constant_key("PAC__003", "on")
        self.add_constant_key("TELSCAN", "Raster")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)
        self.add_constant_key("BZERO", 0)
        self.add_constant_key("BSCALE", 1)

        # Because these test data are from "ViSP" we need to add these keys,
        # which would normally be added by the `*-processing-visp` science task (although they are not
        # added by the `*-processing-test` science task because Test calibrates VBI data in integration tests
        self.add_constant_key("VSPMAP", 1)
        self.add_constant_key("VSPNMAPS", 2)


@pytest.fixture()
def complete_common_header():
    """
    A header with some common by-frame keywords
    """
    # Taken from dkist-processing-common
    ds = CommonDataset()
    header_list = [
        spec122_validator.validate_and_translate_to_214_l0(d.header(), return_type=fits.HDUList)[
            0
        ].header
        for d in ds
    ]

    return header_list[0]


@pytest.fixture(scope="function", params=[1, 4])
def write_l1_task(complete_common_header, request):
    with WriteL1Data(
        recipe_run_id=randint(0, 99999),
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        num_of_stokes_params = request.param
        stokes_params = ["I", "Q", "U", "V"]

        # Make sure polarimetric header validation happens correctly
        if num_of_stokes_params == 4:
            complete_common_header["VSPPOLMD"] = "observe_polarimetric"
            complete_common_header["POL_NOIS"] = 0.1
            complete_common_header["POL_SENS"] = 0.2
        else:
            complete_common_header["VSPPOLMD"] = "observe_intensity"

        hdu = fits.PrimaryHDU(
            data=np.random.random(size=(1, 128, 128)) * 10, header=complete_common_header
        )
        logger.info(f"{num_of_stokes_params=}")
        hdul = fits.HDUList([hdu])
        for i in range(num_of_stokes_params):
            task.write(
                data=hdul,
                tags=[Tag.calibrated(), Tag.frame(), Tag.stokes(stokes_params[i])],
                encoder=fits_hdulist_encoder,
            )
        task.constants._update(
            asdict(
                FakeConstantDb(
                    AVERAGE_CADENCE=10,
                    MINIMUM_CADENCE=10,
                    MAXIMUM_CADENCE=10,
                    VARIANCE_CADENCE=0,
                    INSTRUMENT="TEST",
                )
            )
        )
        yield task, num_of_stokes_params
        task._purge()


def test_write_l1_task(write_l1_task, mocker):
    """
    :Given: a write L1 task
    :When: running the task
    :Then: no errors are raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, num_of_stokes_params = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output()]))
    logger.info(f"{files=}")
    assert len(files) == num_of_stokes_params
    for file in files:
        logger.info(f"Checking file {file}")
        assert file.exists


class BaseSpec214l0Dataset(Spec122Dataset):
    def __init__(self, num_tasks: int, instrument: str = "vbi"):
        super().__init__(
            dataset_shape=(num_tasks, 4, 4),
            array_shape=(1, 4, 4),
            time_delta=1,
            instrument=instrument,
            file_schema="level0_spec214",
        )

    @property
    def data(self):
        return np.ones(shape=self.array_shape)


@pytest.fixture()
def test_l0_quality_metrics_task_class(quality_l0_task_types):
    # Just to override `quality_task_types` to make testing more precise
    class TestingL0QualityMetrics(TestQualityL0Metrics):
        @property
        def quality_task_types(self) -> list[str]:
            return quality_l0_task_types

    return TestingL0QualityMetrics


@pytest.fixture(params=[pytest.param(1, id="no_modstates"), pytest.param(4, id="with_modstates")])
def num_modstates(request):
    return request.param


@pytest.fixture()
def quality_l0_task_types() -> list[str]:
    # The tasks types we want to build l0 metrics for
    return [TaskName.lamp_gain.value, TaskName.dark.value]


@pytest.fixture()
def dataset_task_types(quality_l0_task_types) -> list[str]:
    # The task types that exist in the dataset. I.e., a larger set than we want to build metrics for.
    return quality_l0_task_types + [TaskName.solar_gain.value, TaskName.observe.value]


@pytest.fixture()
def quality_l0_task(
    test_l0_quality_metrics_task_class,
    tmp_path,
    num_modstates,
    dataset_task_types,
    link_constants_db,
    recipe_run_id,
):
    link_constants_db(
        recipe_run_id=recipe_run_id, constants_obj={BudName.num_modstates.value: num_modstates}
    )
    with test_l0_quality_metrics_task_class(
        recipe_run_id=recipe_run_id, workflow_name="TestTasks", workflow_version="vX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        ds = BaseSpec214l0Dataset(num_tasks=len(dataset_task_types) * num_modstates)
        for modstate in range(1, num_modstates + 1):
            for frame, task_type in zip(ds, dataset_task_types):
                hdu = frame.hdu()
                hdul = fits.HDUList([hdu])
                task.write(
                    data=hdul,
                    tags=[Tag.input(), Tag.task(task_type), Tag.modstate(modstate)],
                    encoder=fits_hdulist_encoder,
                )

        yield task
        task._purge()


def test_quality_l0_metrics(quality_l0_task, quality_l0_task_types, num_modstates):
    """
    Given: A sublcassed `QualityL0Metrics` task and some data frames
    When: Running the task
    Then: The correct metrics are produced
    """
    task = quality_l0_task
    task()

    task_metric_names = ["FRAME_RMS", "FRAME_AVERAGE"]

    for modstate in range(1, num_modstates + 1):
        for metric_name in task_metric_names:
            for task_type in quality_l0_task_types:
                tags = [Tag.quality(metric_name), Tag.quality_task(task_type)]
                if num_modstates > 1:
                    tags.append(Tag.modstate(modstate))
                files = list(task.read(tags=tags))
                assert files  # there are some
                for file in files:
                    with file.open() as f:
                        data = json.load(f)
                        assert isinstance(data, dict)
                        assert data["x_values"]
                        assert data["y_values"]
                        assert all(isinstance(item, str) for item in data["x_values"])
                        assert all(isinstance(item, float) for item in data["y_values"])
                        assert len(data["x_values"]) == len(data["y_values"])

    global_metric_names = ["DATASET_AVERAGE", "DATASET_RMS"]
    for metric_name in global_metric_names:
        files = list(task.read(tags=[Tag.quality(metric_name)]))
        assert files
        for file in files:
            with file.open() as f:
                data = json.load(f)
                assert isinstance(data, dict)


def test_quality_l0_metrics_task_integration_run(recipe_run_id):
    """
    Given: A base `TestQualityL0Metrics` task with no constants or data
    When: Running the task
    Then: No error is raised
    """
    # I.e., this tests that the fixturization needed to get good testing on the quality L0 task aren't hiding
    # an inability to run in integration tests where the setup is much more minimal
    task = TestQualityL0Metrics(
        recipe_run_id=recipe_run_id, workflow_name="integration-style", workflow_version="vX.Y"
    )
    task()


@pytest.fixture()
def make_movie_frames_task(tmp_path, recipe_run_id):
    with MakeTestMovieFrames(
        recipe_run_id=recipe_run_id, workflow_name="MakeMovieFrames", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        task.testing_num_dsps_repeats = 10
        task.num_steps = 1
        task.num_exp_per_step = 1
        task.constants._update(
            asdict(FakeConstantDb(NUM_DSPS_REPEATS=task.testing_num_dsps_repeats))
        )
        ds = S122Headers(
            array_shape=(1, 10, 10),
            num_steps=task.num_steps,
            num_exp_per_step=task.num_exp_per_step,
            num_dsps_repeats=task.testing_num_dsps_repeats,
        )
        header_generator = (d.header() for d in ds)
        for d, header in enumerate(header_generator):
            data = np.ones((1, 10, 10))
            data[:, : d * 10, :] = 0.0
            hdl = generate_214_l0_fits_frame(data=data, s122_header=header)
            task.write(
                data=hdl,
                tags=[
                    Tag.calibrated(),
                    Tag.dsps_repeat(d + 1),
                ],
                encoder=fits_hdulist_encoder,
            )
        yield task
        task._purge()


def test_make_movie_frames_task(make_movie_frames_task, mocker):
    """
    :Given: a make_movie_frames_task task
    :When: running the task
    :Then: no errors are raised and a movie file is created
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = make_movie_frames_task
    task()
    movie_frames = list(task.read(tags=[Tag.movie_frame()]))
    logger.info(f"{movie_frames=}")
    assert len(movie_frames) == task.testing_num_dsps_repeats
    for frame in movie_frames:
        assert frame.exists()
        hdul = fits.open(frame)
        assert len(hdul[0].data.shape) == 2


@pytest.fixture()
def assemble_test_movie_task(tmp_path, recipe_run_id):
    with AssembleTestMovie(
        recipe_run_id=recipe_run_id, workflow_name="AssembleTestMovie", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
        task.testing_num_dsps_repeats = 10
        task.num_steps = 1
        task.num_exp_per_step = 1
        task.constants._update(
            asdict(FakeConstantDb(NUM_DSPS_REPEATS=task.testing_num_dsps_repeats))
        )
        ds = S122Headers(
            array_shape=(1, 10, 10),
            num_steps=task.num_steps,
            num_exp_per_step=task.num_exp_per_step,
            num_dsps_repeats=task.testing_num_dsps_repeats,
        )
        header_generator = (d.header() for d in ds)
        for d, header in enumerate(header_generator):
            data = np.ones((10, 10))
            data[: d * 10, :] = 0.0
            hdl = generate_214_l0_fits_frame(data=data, s122_header=header)
            task.write(
                data=hdl,
                tags=[
                    Tag.movie_frame(),
                    Tag.dsps_repeat(d + 1),
                ],
                encoder=fits_hdulist_encoder,
            )
        yield task
        task._purge()


def test_assemble_test_movie_task(assemble_test_movie_task, mocker):
    """
    :Given: an assemble_test_movie task
    :When: running the task
    :Then: no errors are raised and a movie file is created
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = assemble_test_movie_task
    task()
    movie_file = list(task.read(tags=[Tag.movie()]))
    logger.info(f"{movie_file=}")
    assert len(movie_file) == 1
    assert movie_file[0].exists()


@pytest.fixture
def trial_output_task(recipe_run_id, tmp_path, mocker):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=FakeGQLClient,
    )
    proposal_id = "test_proposal_id"
    with TransferTrialData(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.constants._update({"PROPOSAL_ID": proposal_id})

        file_count = 0
        # Write a debug frame
        debug_file_obj = uuid4().hex.encode("utf8")
        task.write(debug_file_obj, tags=[Tag.debug(), Tag.frame()])
        file_count += 1

        # Write an intermediate frame
        intermediate_file_obj = uuid4().hex.encode("utf8")
        task.write(
            intermediate_file_obj,
            tags=[Tag.intermediate(), Tag.frame(), Tag.task("DUMMY")],
        )
        file_count += 1

        # An output frame
        output_file_obj = uuid4().hex.encode("utf8")
        task.write(output_file_obj, tags=[Tag.output(), Tag.frame()])
        file_count += 1

        # Output dataset inventory
        dsi_file_obj = uuid4().hex.encode("utf8")
        task.write(dsi_file_obj, tags=[Tag.output(), Tag.dataset_inventory()])
        file_count += 1

        # Output asdf
        asdf_file_obj = uuid4().hex.encode("utf8")
        task.write(asdf_file_obj, tags=[Tag.output(), Tag.asdf()])
        file_count += 1

        # Output movie
        movie_file_obj = uuid4().hex.encode("utf8")
        task.write(movie_file_obj, tags=[Tag.output(), Tag.movie()])
        file_count += 1

        # Output quality data
        quality_data_file_obj = uuid4().hex.encode("utf8")
        task.write(quality_data_file_obj, tags=Tag.quality_data())
        file_count += 1

        # Output quality report
        quality_report_file_obj = uuid4().hex.encode("utf8")
        task.write(quality_report_file_obj, tags=[Tag.output(), Tag.quality_report()])
        file_count += 1

        # This one won't get transferred
        task.write(uuid4().hex.encode("utf8"), tags=[Tag.frame(), "FOO"])

        yield task, file_count
        task._purge()


def test_transfer_test_trial_data(trial_output_task, mocker):
    """
    Given: A TransferTrialData task with associated frames
    When: Running the task and building the transfer list
    Then: No errors occur and the transfer list has the correct number of items
    """
    task, expected_num_items = trial_output_task

    mocker.patch(
        "dkist_processing_common.tasks.mixin.globus.GlobusMixin.globus_transfer_scratch_to_object_store"
    )
    mocker.patch(
        "dkist_processing_common.tasks.trial_output_data.TransferTrialData.remove_folder_objects"
    )

    # Just make sure the thing runs with no errors
    task()

    transfer_list = task.build_transfer_list()
    assert len(transfer_list) == expected_num_items


@pytest.fixture()
def exercise_numba_task(recipe_run_id):
    with ExerciseNumba(
        recipe_run_id=recipe_run_id, workflow_name="ExerciseNumba", workflow_version="VX.Y"
    ) as task:
        yield task


def test_exercise_numba_task(exercise_numba_task):
    """
    :Given: an exercise_numba task
    :When: running the task
    :Then: the numba module can be loaded and simple method using numba is executed
    """
    original = np.linspace(0.0, 10.0, 1001)
    task = exercise_numba_task
    task()
    assert task.speedup > 1.0
    assert np.all(np.equal(original, task.sorted_array))
