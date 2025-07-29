import logging
from pathlib import Path
from typing import Dict, Union

import pydicom
from pydicom.errors import InvalidDicomError

from ..helpers.check_path_is_valid import check_path_is_valid_path
from .ct import CtSeries
from .dicom_study import DicomStudy
from .dose_matrix import DoseMatrix

logger = logging.getLogger(__name__)


def import_dicom_from_folder(folder: Union[Path, str], recursively: bool = True) -> Dict[str, DicomStudy]:
    """Go through a folder and import all valid DICOM images found

    Args:
        folder: Path of the folder to search for DICOM files
        recursively: Specification if the folder should be search recursively. Defaults to True

    Raises:
        TypeError: If the given folder is not a Path object
        ValueError: If the given folder is not a directory
        ValueError: If no valid DICOM files were found in the search of the given folder

    Returns:
        A dictionary on the form {<study-instance-uid>: <DicomStudy object>}

    """
    folder = check_path_is_valid_path(path_to_check=folder)

    if not folder.is_dir():
        raise ValueError("The given folder is not a directory")

    files = folder.iterdir()
    if recursively:
        files = folder.rglob("*")

    dicom_study_list = dict()

    for fp in files:
        if not fp.is_file():
            continue

        if fp.name.casefold() == ".DS_Store".casefold():
            logger.debug("Skipping .DS_Store file")
            continue

        try:
            dcm = pydicom.dcmread(fp=str(fp.absolute()), stop_before_pixels=True)
        except InvalidDicomError as e:
            continue

        if dcm.StudyInstanceUID not in dicom_study_list:
            dicom_study_list[dcm.StudyInstanceUID] = DicomStudy(study_instance_uid=dcm.StudyInstanceUID)

        dicom_study_list[dcm.StudyInstanceUID].add_file(fp, dcm=dcm)

    if not len(dicom_study_list):
        raise ValueError("The given folder contains no valid DICOM files")

    return dicom_study_list


def import_dicom_file(file: Union[Path, str]) -> DicomStudy:
    """Import a DICOM file into a DicomStudy object

    Args:
        file: Path to the file to import

    Raises:
        TypeError: If the given file is not a Path object
        ValueError: If the given file path is not a valid file
        InvalidDicomError: If the given file is not a valid DICOM file

    Returns:
        DicomStudy object with the file added to it

    """
    file = check_path_is_valid_path(path_to_check=file)

    if not file.is_file():
        raise ValueError("File is not a valid file")

    try:
        dcm = pydicom.dcmread(fp=str(file.absolute()), stop_before_pixels=True)
    except InvalidDicomError:
        raise

    output = DicomStudy(study_instance_uid=dcm.StudyInstanceUID)
    output.add_file(file=file, dcm=dcm)

    if isinstance(output.Series[0], CtSeries):
        output.Series[0].import_image_volume()
    elif isinstance(output.Series[0], DoseMatrix):
        output.Series[0].import_dose_matrix()
    else:
        output.Series[0].import_image()

    return output
