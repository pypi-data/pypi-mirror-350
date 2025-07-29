import numpy as np
from pydicom import FileDataset


def remove_position_indication_square_schick_sensor_image(image: np.ndarray, metadata: FileDataset) -> np.ndarray:
    """Removes the position indication square from schick sensors. In these sensors the position indication square is
    a small square in the upper right corner (when Field of view rotation = 0) that has inverted pixel values. This
    square is helpful for identifying the rotation when looking at the image but will impact statistical measures on the
    image in a negative way.

    Args:
        image: The Schick sensor image to remove position indication square from
        metadata: The metadata of the image

    Returns:
        The same image but with the position indication square pixel values rescaled to the same scale as the rest of
        the image

    Raises:
        NotImplementedError: If the metadata does not contain the DetectorManufacturerName tag
        NotImplementedError: If the metadata does not specify Sirona Dental, Inc. as the detector manufacturer
    """
    if "DetectorManufacturerName" not in metadata:
        raise NotImplementedError("No information on the detector manufacturer in file")

    if (manufacturer := metadata.DetectorManufacturerName.casefold()) != "Sirona Dental, Inc.".casefold():
        raise NotImplementedError(f"This function is not implemented for detector manufacturer {manufacturer}")

    square_mask = np.abs(image - np.mean(image)) > (4 * np.std(image))

    image[square_mask] = 2 ** metadata.BitsStored - image[square_mask]

    return image
