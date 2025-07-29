import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from CTADIRAC.Interfaces.API.CWLJob import CWLJob
from CTADIRAC.Interfaces.Utilities.CWL_utils import (
    LFN_DIRAC_PREFIX,
    LFN_PREFIX,
)

INPUT_DATA = ["/ctao/user/MC/prod.sim", "/ctao/user/MC/prod2.sim"]
INPUT_SANDBOX = ["/a/local/MC/simulation.py", "/path/to/MC.prod3.sim"]
CWL_INPUTS_EXAMPLE = f"""
local_script:
  - class: File
    path: {INPUT_SANDBOX[0]}
input_as_lfn:
  - class: File
    path: {LFN_PREFIX}{INPUT_DATA[0]}
input_as_lfn_2:
  - class: File
    path: {LFN_PREFIX}{INPUT_DATA[1]}
  - class: File
    path: {INPUT_SANDBOX[1]}
dataset: "dataset://path/to/data"
input_param: "a random param"
"""
OUTPUT_DATA = ["/ctao/user/MC/fit*.out", "/ctao/usr/MC/data.sim"]
OUTPUT_SANDBOX = ["/path/to/test*.out", "/path/to/data_2.sim", "*.txt"]
BASE_COMMAND = "python"
IMAGE = "harbor.cta-observatory.org/proxy_cache/library/python:3.12-slim"
CWL_WORKFLOW_EXAMPLE = f"""
cwlVersion: v1.2
class: CommandLineTool
doc: |
      Test using local input/output data treated as Dirac
      input/output sandboxes.

inputs:
  local_script:
    type: File
    inputBinding:
      position: 1
  input_as_lfn:
    type: File?
    inputBinding:
      position: 2
  input_as_lfn_2:
    type: File[]
    inputBinding:
      position: 3
  dataset:
    type: [File, string]
    inputBinding:
      position: 4
  input_param:
    type: string
    inputBinding:
      position: 5

outputs:
  output_as_sb:
    type: File[]?
    outputBinding:
      glob: ["{OUTPUT_SANDBOX[0]}"]
  output_as_lfn:
    type: File?
    label: "LFN wildcards"
    outputBinding:
      glob: "{LFN_PREFIX}{OUTPUT_DATA[0]}"
  output_as_lfn_2:
    type: File[]
    label: "LFN files list"
    outputBinding:
      glob:
        - {LFN_PREFIX}{OUTPUT_DATA[1]}
        - {OUTPUT_SANDBOX[1]}
  output_as_array:
    type:
      type: array
      items: File
    outputBinding:
      glob: "{OUTPUT_SANDBOX[2]}"

baseCommand: ["{BASE_COMMAND}"]

hints:
  DockerRequirement:
    dockerPull: {IMAGE}
"""

CWL_WORKFLOW_EXAMPLE_NO_INPUT = """
cwlVersion: v1.2
class: CommandLineTool
doc: |
      Test using local input/output data treated as Dirac
      input/output sandboxes.

inputs:
  local_script:
    type: string
    inputBinding:
      position: 1

outputs:
  output_as_sb:
    type: File[]?
    outputBinding:
      glob: ["/path/to/output_1.txt"]

baseCommand: ["base_command"]
"""
CWL_WORKFLOW_EXAMPLE_NO_INPUT_INPUTS = """
local_script: "test"
"""


@pytest.fixture
def mock_submit_job(mocker):
    return mocker.patch(
        "CTADIRAC.Interfaces.API.CWLJob.Dirac.submitJob",
        side_effect=lambda self: self._toXML(),
    )


@pytest.mark.parametrize(
    (
        "cwl_worflow",
        "cwl_inputs",
        "expected_input_data",
        "expected_input_sandbox",
        "expected_output_data",
        "expected_output_sandbox",
    ),
    [
        (
            CWL_WORKFLOW_EXAMPLE,
            CWL_INPUTS_EXAMPLE,
            [f"{LFN_DIRAC_PREFIX}{data}" for data in INPUT_DATA],
            INPUT_SANDBOX,
            [f"{LFN_DIRAC_PREFIX}{data}" for data in OUTPUT_DATA],
            OUTPUT_SANDBOX,
        ),
        (
            CWL_WORKFLOW_EXAMPLE_NO_INPUT,
            CWL_WORKFLOW_EXAMPLE_NO_INPUT_INPUTS,
            [],
            [],
            [],
            ["/path/to/output_1.txt"],
        ),
    ],
)
def test_cwl_job_submit(
    mock_submit_job,
    tmp_path,
    cwl_worflow,
    cwl_inputs,
    expected_input_data,
    expected_input_sandbox,
    expected_output_data,
    expected_output_sandbox,
):
    cwl_workflow_example = tmp_path / "cwl_workflow_example.cwl"
    cwl_workflow_example.write_text(cwl_worflow)
    cwl_inputs_example = tmp_path / "cwl_inputs_example.cwl"
    cwl_inputs_example.write_text(cwl_inputs)

    job = CWLJob(
        cwl_workflow=cwl_workflow_example,
        cwl_inputs=cwl_inputs_example,
        cvmfs_base_path=Path("/cvmfs/ctao.dpps.test/"),
        output_se="TEST_SE",
    )

    result = job.submit()
    mock_submit_job.assert_called_once_with(job)
    result_xml = ET.fromstring(result)

    def get_list(name):
        element = result_xml.find(f".//Parameter[@name='{name}']/value")
        if element is None or element.text is None:
            return []
        return element.text.split(";")

    input_data = get_list("InputData")
    assert input_data == expected_input_data

    output_sandbox = get_list("OutputSandbox")
    assert set(expected_output_sandbox).issubset(output_sandbox)

    input_sandbox = get_list("InputSandbox")
    assert set(expected_input_sandbox).issubset(input_sandbox)

    output_data = get_list("OutputData")
    assert output_data == expected_output_data

    if expected_output_data:
        output_se_parameter = result_xml.find(".//Parameter[@name='OutputSE']")
        assert output_se_parameter is not None
        output_se = output_se_parameter.find("value")
        assert output_se is not None
        assert output_se.text == "TEST_SE"

    if executable := result_xml.find(
        ".//StepInstance/Parameter[@name='executable']/value"
    ):
        executable = executable.text
        assert executable == "cwltool"


def test_datapipe_cwl_job(mock_submit_job):
    job = CWLJob(
        "tests/resources/cwl/process_dl0_dl1.cwl",
        "tests/resources/cwl/inputs_process_dl0_dl1.yaml",
        cvmfs_base_path=Path("/cvmfs/ctao.dpps.test/"),
    )

    # these are set via inputs
    assert len(job.input_data) == 1
    assert (
        job.input_data[0]
        == "LFN:/ctao/simpipe/prod6/gamma-diffuse/010xxx/gamma_cone10_run010000.simtel.zst"
    )

    result = job.submit()
    mock_submit_job.assert_called_once_with(job)
    result_xml = ET.fromstring(result)

    if input_data := result_xml.find(".//Parameter[@name='InputData']/value"):
        input_data = input_data.text.split(";")
        assert len(input_data) == 1
        assert input_data[0] == "gamma_cone10_run010000.simtel.zst"

    if input_sandbox := result_xml.find(".//Parameter[@name='InputSandbox']/value"):
        input_sandbox = input_sandbox.text.split(";")
        assert len(input_sandbox) == 1
        assert input_sandbox[0] == "process_config.yaml"

    if output_data := result_xml.find(".//Parameter[@name='OutputData']/value"):
        output_data = output_data.text.split(";")
        assert len(output_data) == 1
        assert output_data[0] == "LFN:/ctao/datapipe/test.dl1.h5"

    if output_sandbox := result_xml.find(".//Parameter[@name='OutputSandbox']/value"):
        output_sandbox = output_sandbox.text.split(";")
        assert len(job.output_sandbox) == 1
        assert job.output_sandbox[0] == "ctapipe-process_dl0_dl1.provenance.log"
