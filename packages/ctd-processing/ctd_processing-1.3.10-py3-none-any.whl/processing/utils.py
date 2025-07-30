import sys
from pathlib import Path
import numpy as np
from seabirdfilehandler import CnvFile
from seabirdfilehandler.parameter import Parameter


def default_seabird_exe_path() -> Path:
    """Creates a platform-dependent default path to the Sea-Bird exes."""
    exe_path = "Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/"
    if sys.platform.startswith("win"):
        path_prefix = Path("C:")
    else:
        path_prefix = Path.home().joinpath(".wine/drive_c")
    return path_prefix.joinpath(exe_path)


def get_sample_rate(cnv: CnvFile) -> float:
    """Fetches the sample rate from a CnvFile."""
    interval_info = cnv.data_table_misc["interval"].split(":")
    if not interval_info[0] == "seconds":
        raise BinnedDataError(cnv.file_name, "get_sample_rate")

    return np.round(1 / float(interval_info[1]))


def is_directly_measured_value(parameter: Parameter) -> bool:
    """
    Returns whether a parameter has been measured via a sensor or is calculated.
    """
    value_list = [
        "Pressure",
        "Conductivity",
        "Temperature",
        "Oxygen",
        "PAR/Irradiance",
        "SPAR",
        "Fluorescence",
        "Turbidity",
    ]
    return parameter.metadata["name"] in value_list


def get_performed_processing_modules(cnv: CnvFile) -> set:
    """
    Filters the processing metadata lines for the individual steps conducted to
    retrieve the current files version.
    """
    return {module.split("_")[0] for module in cnv.processing_info}


def get_alignment_delay_and_correlation_values(cnv: CnvFile) -> list:
    """
    Finds the two numerical values in the processing output produced by the
    custom alignment tool. These are extracted separately for each sensor and
    sorted inside of list[tuple] structure.
    """
    output = []
    sensor = 1
    for line in cnv.processing_info:
        if line.startswith("alignctd_") and not line.startswith("alignctd_metadata"):
            name, value = line.split("=")
            if str(sensor - 1) in name.strip():
                # catch files that have used Sea-Bird align or were run with a
                # pre-set value, these are not interesting for this extraction
                try:
                    delay, metainfo = value.split(",")
                except ValueError:
                    continue
                sensor_tuple = (delay.strip()[:-1], metainfo.strip()[-4:])
                output.append(sensor_tuple)
                sensor += 1
            if sensor > 2:
                break

    return output


class BinnedDataError(Exception):
    """A custom error to throw when binned data has been detected."""

    def __init__(self, file_name: str, step_name: str):
        super().__init__(f"{step_name} cannot be applied to binned data in {file_name}")
