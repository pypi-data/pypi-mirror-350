import logging
from pathlib import Path
from typing import List, Optional, Union

import numpy as np
import pydicom
from plotly import graph_objects as go
from pydicom import FileDataset
from scipy import ndimage
from scipy.ndimage import center_of_mass
from skimage import morphology

from ..helpers.check_path_is_valid import check_path_is_valid_path
from ..helpers.normalize_dicom_exposure_parameters import get_xray_tube_current_in_ma
from ..helpers.patient_centering import PatientGeometricalOffset, PatientMassCenter
from ..helpers.pixel_data import get_pixel_array
from ..helpers.voxel_data import VoxelData
from ..helpers.window import get_default_window_settings
from ..plotting.plotly import (
    create_stack_plot,
    get_image_and_roi_traces_and_layout,
    show_image,
)
from ..roi.roi import Roi
from .dicom_series import DicomSeries

log = logging.getLogger(__name__)


class CtSeries(DicomSeries):
    """A class to manage DICOM files from CT connected by a Series Instance UID

    Args:
        series_instance_uid: Series instance UID of the object to be created

    Attributes:
        kV: Tube voltage used for each image in kV
        mA: Tube current used per image in mA
        SlicePosition: List of slice locations (in mm)
        Manufacturer: The name of the manufacturer of the CT machine
        ManufacturersModelName: The model name specified by the manufacturer as given in the DICOM file
        Mask: A mask covering the patient, created in the get_patient_mask method
        MaskSuccess: A boolean saying if the patient mask creationg was successful or not
        PatientClipped: A boolean specifying if the masked patient contour touches the any of the edges of the image
                        volume
        PatientMassCenterImage: A list of the masked patient mass center for each image
        PatientMassCenterVolume: The masked patient volume mass center
        PatientGeometricalOffset: The patient volume geometrical offset from the scanner isocenter
        MeanHuPatientImage: Mean HU value of the masked patient for each image
        MedianHuPatientImage: Median HU value of the masked patient for each image
        MeanHuPatientVolume: Mean HU value of the masked patient volume
        MedianHuPatientVolume: Median HU value of the masked patient volume

    """

    def __init__(self, series_instance_uid: str):
        super().__init__(series_instance_uid=series_instance_uid)
        self.kV: Optional[List[float]] = None
        self.mA: Optional[List[Optional[float]]] = None
        self.SlicePosition: Optional[List[float]] = []
        self.Manufacturer: Optional[str] = None
        self.ManufacturersModelName: Optional[str] = None

        # Image volume data
        self.Mask: Optional[np.ndarray] = None
        self.MaskSuccess: Optional[bool] = None
        self.PatientClipped: Optional[bool] = None

        # Calculated image information
        self.PatientMassCenterImage: Optional[List[PatientMassCenter]] = None
        self.PatientMassCenterVolume: Optional[PatientMassCenter] = None
        self.PatientGeometricalOffset: Optional[PatientGeometricalOffset] = None
        self.MeanHuPatientImage: Optional[List[float]] = None
        self.MedianHuPatientImage: Optional[List[float]] = None
        self.MeanHuPatientVolume: Optional[float] = None
        self.MedianHuPatientVolume: Optional[float] = None

    def add_file(self, file: Union[Path, str], dcm: Optional[FileDataset] = None) -> None:
        """Add a file to the objects list of files.

        First performs a check that the file is a valid DICOM file and that it is a CT file.
        List properties are emptied to prevent mismatch between them, the FilePaths and SlicePosition

        Raises:
            ValueError: If supplied file is not a CT image

        """
        file = check_path_is_valid_path(path_to_check=file)

        if dcm is None:
            dcm = pydicom.dcmread(fp=str(file.absolute()), stop_before_pixels=True)

        if dcm.Modality.upper() != "CT":
            raise ValueError(f"The supplied file is not a CT image. (supplied modality: {dcm.Modality}")

        self.ImageVolume = None
        self.kV = []
        self.mA = []
        self.PatientMassCenterImage = []
        self.PatientMassCenterVolume = None
        self.PatientGeometricalOffset = None
        self.MeanHuPatientVolume = None
        self.MeanHuPatientImage = []
        self.MedianHuPatientVolume = None
        self.MedianHuPatientImage = []
        self.Mask = None
        self.MaskSuccess = None
        self.PatientClipped = None

        super().add_file(file=file, dcm=dcm)
        self.Manufacturer = dcm.Manufacturer
        self.ManufacturersModelName = dcm.ManufacturerModelName if "ManufacturerModelName" in dcm else None
        self.SlicePosition.append(self._get_slice_position(dcm))

        # Reorder lists according to slice positions
        file_order = [ind for ind in list(np.argsort(np.array(self.SlicePosition)))]
        self.FilePaths = [self.FilePaths[ind] for ind in file_order]
        self.SlicePosition = [self.SlicePosition[ind] for ind in file_order]

    def import_image_volume(self) -> None:
        """Import the files in the CtVolume and insert them into the ImageVolumeProperty. Also add metadata for each
        image into the respective property.
        """
        # Remove any previously imported image volume
        self.ImageVolume = None
        self.kV = []
        self.mA = []
        self.SlicePosition = []
        self.PatientMassCenterImage = []
        self.VoxelData = []
        self.CompleteMetadata = []

        for ind, fp in enumerate(self.FilePaths):
            dcm = pydicom.dcmread(fp=str(fp.absolute()))
            px = get_pixel_array(dcm=dcm)

            if self.ImageVolume is None:
                self.ImageVolume = np.empty((px.shape[0], px.shape[1], len(self.FilePaths)))

            self.ImageVolume[:, :, ind] = px
            self.kV.append(float(dcm.KVP) if dcm.KVP else None)
            self.mA.append(get_xray_tube_current_in_ma(dcm))

            self.SlicePosition.append(self._get_slice_position(dcm))

            self.VoxelData.append(
                VoxelData(x=float(dcm.PixelSpacing[1]), y=float(dcm.PixelSpacing[0]), z=float(dcm.SliceThickness))
            )

            # Remove pixel data part of dcm to decrease memory used for the object
            try:
                del dcm[0x7FE00010]
            except Exception as e:
                log.debug(f"Could not remove pixel data from dataset ({fp.absolute()})")
                pass

            self.CompleteMetadata.append(dcm)

    @staticmethod
    def _get_slice_position(dcm: FileDataset) -> float:
        if "SliceLocation" in dcm and dcm.SliceLocation is not None:
            return float(dcm.SliceLocation)

        if "ImagePositionPatient" in dcm:
            return float(dcm.ImagePositionPatient[2])

        return float(dcm.InstanceNumber)

    def get_patient_mask(self, threshold: Optional[int] = -500, remove_table: Optional[bool] = False):
        """Segment the ImageVolume to find the patient/phantom in the images.

        Args:
            threshold: HU value to use as threshold. Defaults to -500
            remove_table: Specify if the CT table should be removed from the image. Defaults to False

        Raises:
            TypeError: If threshold is not an integer
            ValueError: If there is not image volume to segment

        """
        if not isinstance(threshold, int):
            raise TypeError("The threshold must be given as an integer")

        if self.ImageVolume is None:
            self.import_image_volume()
            if self.ImageVolume is None:
                raise ValueError("Found no image volume to segment")

        self.Mask = np.zeros(self.ImageVolume.shape)
        self.Mask[self.ImageVolume >= threshold] = 1

        if remove_table:
            # Remove the table by eroding and dilating the image volume
            if self.Mask.shape[2] > 2:
                self.Mask = morphology.binary_erosion(image=self.Mask, footprint=morphology.cube(width=3))
            else:
                for i in range(self.Mask.shape[2]):
                    self.Mask[:, :, i] = morphology.binary_erosion(
                        image=self.Mask[:, :, i], footprint=morphology.disk(radius=3)
                    )

            self.Mask, nb_labels = ndimage.label(self.Mask)

            central_position = [
                int(np.floor(np.divide(float(self.Mask.shape[0]), 2.0))),
                int(np.floor(np.divide(float(self.Mask.shape[1]), 2.0))),
                int(np.floor(np.divide(float(self.Mask.shape[2]), 2.0))),
            ]

            central_blob = np.max(
                self.Mask[
                    (central_position[0] - 2) : (central_position[0] + 3),
                    (central_position[1] - 2) : (central_position[1] + 3),
                    central_position[2],
                ]
            )

            self.Mask[self.Mask != central_blob] = 0
            self.Mask[self.Mask == central_blob] = 1

            if self.Mask.shape[2] > 2:
                self.Mask = morphology.binary_dilation(image=self.Mask, footprint=morphology.cube(width=3))
            else:
                for i in range(self.Mask.shape[2]):
                    self.Mask[:, :, i] = morphology.binary_dilation(
                        image=self.Mask[:, :, i], footprint=morphology.disk(radius=3)
                    )

        for i in range(self.Mask.shape[2]):
            self.Mask[:, :, i] = ndimage.binary_fill_holes(self.Mask[:, :, i]).astype(int)

        if np.sum(self.Mask) > 0:
            log.info("Axial images segmented successfully")
            self.MaskSuccess = True

        self.Mask = self.Mask.astype(bool)
        tmp_mass_center = [center_of_mass(input=self.Mask[:, :, ind]) for ind in range(self.Mask.shape[2])]
        self.PatientMassCenterImage = [PatientMassCenter(x=obj[1], y=obj[0]) for obj in tmp_mass_center]

        if self.Mask.shape[2] > 1:
            tmp_mass_center = center_of_mass(input=self.Mask)
            self.PatientMassCenterVolume = PatientMassCenter(
                x=tmp_mass_center[1], y=tmp_mass_center[0], z=tmp_mass_center[2]
            )
        else:
            self.PatientMassCenterVolume = self.PatientMassCenterImage[0]

        # Try to get the patient geometrical offset
        try:
            self._get_patient_geometrical_offset()
        except Exception as e:
            log.warning("Could not calculate patient geometrical offset", e)

        # Check if patient is clipped
        self.PatientClipped = any(
            [
                np.sum(self.Mask[0, :, :]) > 0,
                np.sum(self.Mask[-1, :, :]) > 0,
                np.sum(self.Mask[:, 0, :]) > 0,
                np.sum(self.Mask[:, -1, :]) > 0,
            ]
        )

        # Calculate mean and median values
        tmp_masked_image = np.ma.array(self.ImageVolume, mask=np.logical_not(self.Mask))

        self.MeanHuPatientImage = list(tmp_masked_image.mean(axis=(0, 1)))
        self.MedianHuPatientImage = list(np.ma.median(tmp_masked_image, axis=(0, 1)))
        self.MeanHuPatientVolume = tmp_masked_image.mean(axis=None)
        self.MedianHuPatientVolume = np.ma.median(tmp_masked_image, axis=None)

    def _get_patient_geometrical_offset(self):
        """Calculate the patient/phantom geometrical offset from isocenter

        Raises:
            ValueError: If the DICOM header does not contain all tags required for the calculation

        """
        log.info("Calculating phantom geometrical offset")

        for ind, mass_center in enumerate(self.PatientMassCenterImage):
            if "ImagePositionPatient" in self.CompleteMetadata[ind]:
                geometrical_center = (round(mass_center.y, 1), round(mass_center.x, 1))
                image_position = (
                    float(self.CompleteMetadata[ind].ImagePositionPatient[0]),
                    float(self.CompleteMetadata[ind].ImagePositionPatient[1]),
                )

                if self.Manufacturer.upper() in ["SIEMENS", "PHILIPS"]:
                    # Recalculate image position due to incorrect specifications
                    image_position[1] += float(self.CompleteMetadata[ind].TableHeight)

                if self.PatientGeometricalOffset is None:
                    self.PatientGeometricalOffset = []

                self.PatientGeometricalOffset.append(
                    PatientGeometricalOffset(
                        x=float(image_position[0]) + geometrical_center[1] + self.VoxelData[ind].x,
                        y=float(image_position[1]) + geometrical_center[0] + self.VoxelData[ind].y,
                    )
                )
                continue

            if (
                "DataCollectionCenterPatient" in self.CompleteMetadata[ind]
                and "ReconstructionTargetCenterPatient" in self.CompleteMetadata[ind]
            ):
                log.debug(
                    (
                        "Calculating diff from table based on DataCollectionCenterPatient and "
                        "ReconstructionTargetCenterPatient"
                    )
                )
                diff_table_x_mm = float(self.CompleteMetadata[ind].ReconstructionTargetCenterPatient[0]) - float(
                    self.CompleteMetadata[ind].DataCollectionCenterPatient[0]
                )
                diff_table_y_mm = float(self.CompleteMetadata[ind].ReconstructionTargetCenterPatient[1]) - float(
                    self.CompleteMetadata[ind].DataCollectionCenterPatient[1]
                )

            elif self.Manufacturer.upper() in ["GE MEDICAL SYSTEMS"] and self.CompleteMetadata[ind][0x431031]:
                log.debug(f"Calculating diff from table for machine from {self.Manufacturer}")
                diff_table_x_mm = float(self.CompleteMetadata[ind][0x431031].value[0])
                diff_table_y_mm = float(self.CompleteMetadata[ind][0x431031].value[1])

            elif self.Manufacturer.upper() in ["TOSHIBA"] and self.CompleteMetadata[ind][0x70051007]:
                log.debug(f"Calculating diff from table for machine from {self.Manufacturer}")
                tmp = [float(i) for i in self.CompleteMetadata[ind][0x70051007].value.decode("utf-8").split("\\")]
                diff_table_x_mm = (tmp[0] - self.CompleteMetadata[ind].Columns / 2.0) * self.VoxelData[ind].x
                diff_table_y_mm = (tmp[1] - self.CompleteMetadata[ind].Rows / 2.0) * self.VoxelData[ind].y

            else:
                raise ValueError("The DICOM header does not contain all required tags")

            # Calculate patient offset
            image_center_x = self.CompleteMetadata[ind].Columns / 2.0
            image_center_y = self.CompleteMetadata[ind].Rows / 2.0

            log.debug(f"Image center: x={image_center_x}, y={image_center_y}")

            geometrical_center = (round(mass_center[0], 1), round(mass_center[1], 1))

            diff_geom_x_center_mm = (geometrical_center[1] - image_center_x) * self.VoxelData[ind].x
            diff_geom_y_center_mm = (geometrical_center[0] - image_center_y) * self.VoxelData[ind].y

            self.PatientGeometricalOffset.append(
                PatientGeometricalOffset(
                    x=diff_table_x_mm - diff_geom_x_center_mm, y=diff_table_y_mm - diff_geom_y_center_mm
                )
            )

    def show_image(
        self,
        index: int = 0,
        rois: Optional[Roi] = None,
        colour_map: str = "bone",
        window: Optional[tuple[float, float]] = None,
        roi_only_borders: Optional[bool] = True,
        roi_colour: str = "#33a652",
        roi_border_width: int = 2,
    ) -> go.Figure:
        super().show_image(index=index, rois=rois, colour_map=colour_map, window=window)

        if self.ImageVolume is None:
            self.import_image_volume()

        if window is None:
            window = (-500, 500)

        return show_image(
            image=self.ImageVolume[:, :, index],
            x_scale=self.VoxelData[index].x,
            y_scale=self.VoxelData[index].y,
            window=window,
            rois=rois,
            roi_colour=roi_colour,
            roi_only_border=roi_only_borders,
            roi_border_width=roi_border_width,
            colour_map=colour_map,
        )

    def show_image_slices(
        self,
        rois: Optional[list[list[Roi]]] = None,
        colour_map: str = "bone",
        window: Optional[tuple[float, float]] = None,
        roi_only_borders: Optional[bool] = True,
        roi_colour: str = "#33a652",
        roi_border_width: int = 2,
        colour_bar: Optional[bool] = True,
    ):
        super().show_image(index=0, rois=None, colour_map=colour_map, window=window)

        if rois is None:
            rois = [None] * len(self.FilePaths)

        if not isinstance(rois, list) or not all(
            [
                roi is None or (isinstance(roi, list) and all([isinstance(roi_instance, Roi) for roi_instance in roi]))
                for roi in rois
            ]
        ):
            raise TypeError("ROIs, if specified, must be given as a list of lists of SquareRoi instances")

        if self.ImageVolume is None:
            self.import_image_volume()

        if window is None:
            window = self._get_default_window_settings(index=0)

        return create_stack_plot(
            image=self.ImageVolume,
            x_scale=[voxel_data.x for voxel_data in self.VoxelData],
            y_scale=[voxel_data.y for voxel_data in self.VoxelData],
            window=window,
        )

    def _get_default_window_settings(self, index: int) -> tuple[float, float]:
        return get_default_window_settings(
            metadata=self.CompleteMetadata[index], image_slice=self.ImageVolume[:, :, index], modality="ct"
        )

    def save_image_volume_to_dicom_files(self, output_directory: Path, create_directory_if_not_exist: bool = True):
        if not isinstance(output_directory, (str, Path)):
            raise TypeError("The output directory must be a path")

        output_directory: Path = Path(output_directory) if isinstance(output_directory, str) else output_directory

        if create_directory_if_not_exist:
            output_directory.mkdir(exist_ok=True, parents=True)

        if not output_directory.exists() or not output_directory.is_dir():
            raise ValueError("The specified output directory does not exist")

        _ = [
            self.save_image(image_index=ind, output_path=output_directory / f"{ind + 1}.dcm")
            for ind in range(self.ImageVolume.shape[2])
        ]
