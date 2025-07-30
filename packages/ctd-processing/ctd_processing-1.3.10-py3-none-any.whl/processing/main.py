from pathlib import Path
import sys
import argparse
import logging
from processing.procedure import Procedure
from processing.settings import Configuration


format = "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
loglevel = logging.INFO

# Configure the root logger with a file handler
logging.basicConfig(
    level=loglevel,
    format=format,
    datefmt=datefmt,
    handlers=[
        logging.FileHandler("processing.log"),
        logging.StreamHandler(),  # Also output to console
    ],
)

logger = logging.getLogger(__name__)


def main(
    processing_target: str = "",
    path_to_configuration: Path | str = Path("processing_config.toml"),
    procedure_fingerprint_directory: str | None = None,
    file_type_dir: str | None = None,
    verbose: bool = False,
):
    """

    Parameters
    ----------
    processing_target: str :
        The target file to process.
         (Default value = "")

    path_to_configuration: Path | str :
        The path to the configuration file.
         (Default value = Path("processing_config.toml"))

    procedure_fingerprint_directory: str | None :
        The path to a fingerprint directory. If none given, no fingerprints
        will be created.
         (Default value = None)

    file_type_dir: str | None :
        The path to a file type directory. If none given, the files will not be
        separated into file type directories.
         (Default value = None)

    verbose: bool :
        An option to allow more verbose output.
         (Default value = False)

    Returns
    -------

    """
    path_to_config = Path(path_to_configuration)
    if path_to_config.exists():
        config = Configuration(path_to_config)
    else:
        sys.exit("Could not find the configuration file.")
    config["input"] = processing_target
    Procedure(
        configuration=config,
        procedure_fingerprint_directory=procedure_fingerprint_directory,
        file_type_dir=file_type_dir,
        verbose=verbose,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--processing_target",
        default="",
        help="The processing target file. When left empty, the target file(s) need to be specified inside of the config file.",
    )
    parser.add_argument(
        "-c",
        "--config_file",
        default="processing_config.toml",
        help="The configuration file that describes the processing run.",
    )
    parser.add_argument(
        "-f",
        "--fingerprint_dir",
        default=None,
        help="The target directory to store fingerprint files. If none given, no fingerprint files will be created.",
    )
    parser.add_argument(
        "-d",
        "--file_type_dir",
        default=None,
        help="The target directory to store individual file type directories to. If none give, no file type directories will be created.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Whether to give verbose feedback.",
    )
    args = parser.parse_args()

    main(
        args.processing_target,
        args.config_file,
        args.fingerprint_dir,
        args.file_type_dir,
        args.verbose,
    )
