from pathlib import Path

import pytest
from cwl_utils.parser.cwl_v1_2 import (
    CommandLineTool,
    CommandOutputArraySchema,
    CommandOutputBinding,
    CommandOutputParameter,
    DockerRequirement,
    File,
)

from CTADIRAC.Interfaces.Utilities.CWL_utils import (
    LFN_DIRAC_PREFIX,
    LFN_PREFIX,
    LOCAL_PREFIX,
    extract_and_translate_input_files,
    extract_and_translate_output_files,
    translate_cwl_workflow,
    translate_docker_hints,
    translate_sandboxes_and_lfns,
    verify_cwl_output_type,
)


CVMFS_BASE_PATH = Path("/cvmfs/ctao.dpps.test")


@pytest.mark.parametrize(
    ("file_input", "expected_result", "expected_lfn"),
    [
        (
            File(path=LFN_PREFIX + "test_lfn_file.txt"),
            "test_lfn_file.txt",
            True,
        ),
        (
            File(path=LOCAL_PREFIX + "test_local_file.txt"),
            "test_local_file.txt",
            False,
        ),
        (
            LFN_PREFIX + "test_lfn_str.txt",
            "test_lfn_str.txt",
            True,
        ),
        (
            LOCAL_PREFIX + "test_local_str.txt",
            "test_local_str.txt",
            False,
        ),
        (File(), None, False),  # This will raise an exception
    ],
)
def test_translate_sandboxes_and_lfns(file_input, expected_result, expected_lfn):
    if expected_result is None:
        with pytest.raises(KeyError, match="File path is not defined."):
            translate_sandboxes_and_lfns(file_input)
    else:
        result, is_lfn = translate_sandboxes_and_lfns(file_input)
        assert result == expected_result
        assert is_lfn == expected_lfn


@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    [
        (
            {"input1": File(path=LFN_PREFIX + "test_lfn_file.txt")},
            {
                "InputDesc": {"input1": File(path="test_lfn_file.txt")},
                "InputSandbox": [],
                "InputData": [LFN_DIRAC_PREFIX + "test_lfn_file.txt"],
            },
        ),
        (
            {"input1": File(path=LOCAL_PREFIX + "test_local_file.txt")},
            {
                "InputDesc": {"input1": File(path="test_local_file.txt")},
                "InputSandbox": ["test_local_file.txt"],
                "InputData": [],
            },
        ),
        (
            {
                "input1": [
                    File(path=LFN_PREFIX + "test_lfn_file1.txt"),
                    File(path=LOCAL_PREFIX + "test_local_file1.txt"),
                ]
            },
            {
                "InputDesc": {
                    "input1": [
                        File(path="test_lfn_file1.txt"),
                        File(path="test_local_file1.txt"),
                    ]
                },
                "InputSandbox": ["test_local_file1.txt"],
                "InputData": [LFN_DIRAC_PREFIX + "test_lfn_file1.txt"],
            },
        ),
        (
            {
                "input1": File(path=LFN_PREFIX + "test_lfn_file2.txt"),
                "input2": File(path=LOCAL_PREFIX + "test_local_file2.txt"),
                "input3": [
                    File(path=LFN_PREFIX + "test_lfn_file3.txt"),
                    File(path=LOCAL_PREFIX + "test_local_file3.txt"),
                ],
            },
            {
                "InputDesc": {
                    "input1": File(path="test_lfn_file2.txt"),
                    "input2": File(path="test_local_file2.txt"),
                    "input3": [
                        File(path="test_lfn_file3.txt"),
                        File(path="test_local_file3.txt"),
                    ],
                },
                "InputSandbox": ["test_local_file2.txt", "test_local_file3.txt"],
                "InputData": [
                    LFN_DIRAC_PREFIX + "test_lfn_file2.txt",
                    LFN_DIRAC_PREFIX + "test_lfn_file3.txt",
                ],
            },
        ),
        (
            {
                "input1": [
                    File(path="some/path/test_local_file1.txt"),
                ]
            },
            {
                "InputDesc": {
                    "input1": [
                        File(path="test_local_file1.txt"),
                    ]
                },
                "InputSandbox": ["some/path/test_local_file1.txt"],
                "InputData": [],
            },
        ),
        (
            {
                "input1": File(path="some/path/test_local_file1.txt"),
            },
            {
                "InputDesc": {
                    "input1": File(path="test_local_file1.txt"),
                },
                "InputSandbox": ["some/path/test_local_file1.txt"],
                "InputData": [],
            },
        ),
    ],
)
def test_extract_and_translate_input_files(input_data, expected_result):
    result = extract_and_translate_input_files(input_data)
    assert result == expected_result


ARRAY_FILE_OUTPUT = CommandOutputArraySchema(items="test.txt", type_="File")
ARRAY_ARRAY_OUTPUT = CommandOutputArraySchema(
    items=["test.txt", "test2.txt"], type_="array"
)


@pytest.mark.parametrize(
    ("output_type", "expected_result"),
    [
        ("File", True),
        (ARRAY_FILE_OUTPUT, True),
        (ARRAY_ARRAY_OUTPUT, True),
        (["File"], True),
        (["null", "File"], True),
        (["null", ARRAY_FILE_OUTPUT], True),
        (["null", ARRAY_ARRAY_OUTPUT], True),
        ("string", False),
        (["null", "string"], False),
    ],
)
def test_verify_cwl_output_type(output_type, expected_result):
    result = verify_cwl_output_type(output_type)
    assert result is expected_result


@pytest.mark.parametrize(
    ("outputs", "expected_result"),
    [
        (
            [
                CommandOutputParameter(
                    type_="File",
                    outputBinding=CommandOutputBinding(glob="/path/to/output1.txt"),
                )
            ],
            {
                "CWLDesc": {},
                "OutputSandbox": ["/path/to/output1.txt"],
                "OutputData": [],
            },
        ),
        (
            [
                CommandOutputParameter(
                    type_="File",
                    outputBinding=CommandOutputBinding(
                        glob=LFN_PREFIX + "/path/to/output1.txt"
                    ),
                )
            ],
            {
                "CWLDesc": {},
                "OutputSandbox": [],
                "OutputData": [LFN_DIRAC_PREFIX + "/path/to/output1.txt"],
            },
        ),
        (
            [
                CommandOutputParameter(
                    type_=CommandOutputArraySchema(type_="array", items=File),
                    outputBinding=CommandOutputBinding(
                        glob=[
                            LFN_PREFIX + "/path/to/output1.txt",
                            "/path/to/output2.txt",
                        ]
                    ),
                )
            ],
            {
                "CWLDesc": {},
                "OutputSandbox": ["/path/to/output2.txt"],
                "OutputData": [LFN_DIRAC_PREFIX + "/path/to/output1.txt"],
            },
        ),
    ],
)
def test_extract_and_translate_output_files(outputs, expected_result):
    cwl_obj = CommandLineTool(inputs=None, outputs=outputs)
    result = extract_and_translate_output_files(cwl_obj, {})

    assert result["OutputSandbox"] == expected_result["OutputSandbox"]
    assert result["OutputData"] == expected_result["OutputData"]
    assert isinstance(result["CWLDesc"], CommandLineTool)


@pytest.mark.parametrize(
    ("hints", "base_command", "expected_hints", "expected_base_command"),
    [
        (
            [DockerRequirement(dockerPull="harbor/python:tag")],
            "python",
            [],
            ["apptainer", "run", str(CVMFS_BASE_PATH / "harbor/python:tag"), "python"],
        )
    ],
)
def test_translate_docker_hints(
    hints, base_command, expected_hints, expected_base_command
):
    cwl_obj = CommandLineTool(
        inputs=None, outputs=None, hints=hints, baseCommand="python"
    )
    result = translate_docker_hints(cwl_obj, CVMFS_BASE_PATH, [])
    assert result.hints == expected_hints
    assert result.baseCommand == expected_base_command


def test_translate_cwl_workflow():
    cwl_obj = CommandLineTool(
        inputs=None,
        outputs=None,
        hints=[DockerRequirement(dockerPull="harbor/python:tag")],
        baseCommand="python",
    )

    result = translate_cwl_workflow(
        cwl_obj=cwl_obj,
        cwl_inputs={},
        cvmfs_base_path=CVMFS_BASE_PATH,
        apptainer_options=[],
    )

    assert result == {"CWLDesc": cwl_obj, "OutputSandbox": [], "OutputData": []}
