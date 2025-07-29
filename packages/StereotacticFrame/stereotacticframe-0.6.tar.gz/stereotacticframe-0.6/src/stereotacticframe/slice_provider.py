from pathlib import Path
import SimpleITK as sitk
from typing import Protocol


def _reorient_rai(img):
    return sitk.DICOMOrient(img, "RAI")


class Processor(Protocol):
    def process(self, image: sitk.Image) -> sitk.Image: ...


class AxialSliceProvider:
    def __init__(self, image_path: Path, preprocessor: Processor):
        self._image_path: Path = image_path
        self._image: sitk.Image = sitk.ReadImage(self._image_path)
        self._rai_image: sitk.Image = _reorient_rai(self._image)
        self._rai_mask: sitk.Image = preprocessor.process(self._rai_image)
        self._counter: int = 0
        self._n_axial_slices: int = self._rai_image.GetSize()[-1]

    def next_image_mask_pair(self) -> tuple[sitk.Image, sitk.Image]:
        self._counter += 1
        return self._rai_image[..., self._counter - 1], self._rai_mask[
            ..., self._counter - 1
        ]

    def is_empty(self) -> bool:
        if self._counter >= self._n_axial_slices:
            return True
        return False

    def get_current_z_coordinate(self) -> float:
        point = self._rai_image.TransformIndexToPhysicalPoint([0, 0, self._counter - 1])
        return point[2]
