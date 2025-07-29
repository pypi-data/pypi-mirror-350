"""Utilities to handle CWL."""

from pathlib import Path
from typing import Any
from copy import deepcopy

from cwl_utils.parser import OutputArraySchema, File
from cwl_utils.expression import do_eval

LFN_PREFIX = "lfn://"
LFN_DIRAC_PREFIX = "LFN:"
LOCAL_PREFIX = "file://"


def fill_defaults(cwl, inputs):
    """Fill in defaults into inputs.

    This is needed for evaluating expressions later on.

    Parameters
    ----------
    cwl: dict
        The CWL definition
    inputs: dict
        user provided inputs.

    Returns
    -------
    inputs: dict
        inputs with additional values filled from CWL defaults
    """
    inputs_new = deepcopy(inputs)

    if cwl.inputs is None:
        return inputs_new

    for inp in cwl.inputs:
        key = inp.id.rpartition("#")[2]
        if key not in inputs and inp.default is not None:
            inputs_new[key] = inp.default
    return inputs_new


def translate_cwl_workflow(
    cwl_obj,
    cwl_inputs,
    cvmfs_base_path: Path,
    apptainer_options: list[Any],
) -> dict[str, Any]:
    """Translate the CWL workflow description into Dirac compliant execution."""
    output_dict = {"CWLDesc": cwl_obj, "OutputSandbox": [], "OutputData": []}

    if cwl_obj.class_ != "CommandLineTool":
        return output_dict

    if cwl_obj.hints:
        cwl_obj = translate_docker_hints(cwl_obj, cvmfs_base_path, apptainer_options)

    return extract_and_translate_output_files(cwl_obj, cwl_inputs)


def translate_docker_hints(
    cwl_obj, cvmfs_base_path: Path, apptainer_options: list[Any]
):
    """Translate CWL DockerRequirement into Dirac compliant execution."""
    for index, hints in enumerate(cwl_obj.hints):
        if hints.class_ == "DockerRequirement":
            image = hints.dockerPull
            cmd = [
                "apptainer",
                "run",
                *apptainer_options,
                str(cvmfs_base_path / f"{image}"),
            ]
            if isinstance(cwl_obj.baseCommand, str):
                cmd += [cwl_obj.baseCommand]
            else:
                cmd += cwl_obj.baseCommand
            cwl_obj.baseCommand = cmd
            del cwl_obj.hints[index]
    return cwl_obj


def collect_outputs(cwl, inputs) -> list[str]:
    """Collect evaluated output filenames.

    Parameters
    ----------
    cwl: dict
        The CWL definition
    inputs: dict
        user provided inputs.

    Returns
    -------
    outputs: list[str]
        The output filenames of this workflow given
        the provided inputs and defaults.
    """
    outputs = []

    if cwl.outputs is None:
        return outputs

    for output in cwl.outputs:
        if glob := output.outputBinding.glob:
            result = do_eval(
                glob,
                inputs,
                outdir=None,
                requirements=[],
                tmpdir=None,
                resources={},
            )
            outputs.append(result)

    return outputs


def extract_and_translate_output_files(cwl_obj, inputs) -> dict[str, Any]:
    """Translate output files into a DIRAC compliant usage.

    Extract local outputs and lfns.
    Remove outputs path prefix.
    """
    output_lfns = []
    output_sandboxes = []

    inputs = fill_defaults(cwl_obj, inputs)

    for outputs in cwl_obj.outputs or []:
        if not verify_cwl_output_type(outputs.type_):
            continue

        glob = outputs.outputBinding.glob

        if isinstance(glob, str):
            glob = do_eval(
                glob,
                inputs,
                outdir=None,
                requirements=[],
                tmpdir=None,
                resources={},
            )
            if glob.startswith(LFN_PREFIX):
                output_lfns.append(glob.replace(LFN_PREFIX, LFN_DIRAC_PREFIX))
            else:
                output_sandboxes.append(glob)

        if isinstance(glob, list):
            for glob_item in glob:
                glob_item = do_eval(
                    glob_item,
                    inputs,
                    outdir=None,
                    requirements=[],
                    tmpdir=None,
                    resources={},
                )
                if glob_item.startswith(LFN_PREFIX):
                    output_lfns.append(glob_item.replace(LFN_PREFIX, LFN_DIRAC_PREFIX))
                else:
                    output_sandboxes.append(glob_item)

    return {
        "CWLDesc": cwl_obj,
        "OutputSandbox": output_sandboxes,
        "OutputData": output_lfns,
    }


def verify_cwl_output_type(output_type) -> bool:
    """Verify the cwl output type.

    True if the type is File or OutputArraySchema
    or a list of 'null' and File/OutputArraySchema
    else False.
    """
    if isinstance(output_type, list):
        for type_ in output_type:
            if type_ == "File" or isinstance(type_, OutputArraySchema):
                return True
    if output_type == "File" or isinstance(output_type, OutputArraySchema):
        return True
    return False


# TODO: how to deal with default values not present in the input file but in the cwl?
def extract_and_translate_input_files(cwl_inputs) -> dict[str, Any]:
    """Extract input files from CWL inputs, rewrite file prefix.

    If the file is a Sandbox, ensure there is no absolute path,
    and store it in the input sandbox list.
    If the file is a LFN, remove the lfn prefix and store it in the lfns list.
    """
    input_sandboxes = []
    input_lfns = []
    cwl_inputs = deepcopy(cwl_inputs)

    def handle_file(input_value):
        original = input_value.path
        input_value.path, lfn = translate_sandboxes_and_lfns(original)
        if lfn:
            input_lfns.append(original.replace(LFN_PREFIX, LFN_DIRAC_PREFIX))
        else:
            input_sandboxes.append(original.removeprefix("file://"))

    for key, input_value in cwl_inputs.items():
        if isinstance(input_value, list):
            for input_file in input_value:
                handle_file(input_file)

        elif isinstance(input_value, File):
            handle_file(input_value)

        # assume that an LFN in the inputs as string is an output filename
        elif isinstance(input_value, str) and input_value.startswith(LFN_PREFIX):
            cwl_inputs[key], _ = translate_sandboxes_and_lfns(input_value)

    return {
        "InputDesc": cwl_inputs,
        "InputSandbox": input_sandboxes,
        "InputData": input_lfns,
    }


def translate_sandboxes_and_lfns(file: File | str) -> tuple[str, bool]:
    """Extract local files as sandboxes and lfns as input data."""
    if isinstance(file, File):
        if not file.path:
            raise KeyError("File path is not defined.")
        path = file.path
    elif isinstance(file, str):
        path = file

    lfn = False
    if path.startswith(LFN_PREFIX):
        path = path.removeprefix(LFN_PREFIX)
        lfn = True

    path = path.removeprefix(LOCAL_PREFIX)
    return Path(path).name, lfn
