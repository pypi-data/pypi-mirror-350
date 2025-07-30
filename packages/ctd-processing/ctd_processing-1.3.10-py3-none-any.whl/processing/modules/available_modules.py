from pathlib import Path
from processing.module import Module
from processing.modules.geomar_wildedit import WildeditGEOMAR
from processing.modules.seabird_functions import AlignCTD
from processing.utils import default_seabird_exe_path

mapper = {
    "alignctd": AlignCTD,
    "wildedit_geomar": WildeditGEOMAR,
}


def map_proc_name_to_class(module: str) -> type[Module]:
    """
    Sets and maps the known processing modules to their respective
    module classes.

    Parameters
    ----------
    module: str :
        Name of the module, that is being used inside the config.

    Returns
    -------

    """
    return mapper[module.lower()]


def get_list_of_custom_exes(
    path_to_custom_exe_dir: Path | str | None = None,
) -> list[str]:
    if isinstance(path_to_custom_exe_dir, Path | str):
        return [exe.stem for exe in Path(path_to_custom_exe_dir).glob("*.exe")]
    else:
        return []


def get_list_of_installed_seabird_modules() -> list[str]:
    seabird_path = default_seabird_exe_path()
    return [str(file.stem)[:-1] for file in seabird_path.glob("*W.exe")]


def get_list_of_available_processing_modules(
    path_to_custom_exe_dir: Path | str | None = None,
) -> list[str]:
    proc_list = [
        *list(mapper.keys()),
        *get_list_of_custom_exes(path_to_custom_exe_dir),
        *get_list_of_installed_seabird_modules(),
    ]
    proc_list.sort()
    return proc_list
