from typing import Tuple

from stereotacticframe.blob_detection import detect_blobs
import pytest
import numpy as np
import SimpleITK as sitk
import logging

logger = logging.getLogger(__name__)


def _create_numpy_blob(
    size: Tuple[int, int],
    center: Tuple[int, int],
    radius: float,
    spacing: float,
    intensity: float,
) -> np.ndarray:
    """Currently not used, but was used to create the blobs of the fixtures"""
    xx, yy = np.mgrid[: size[0], : size[1]]
    circle = np.sqrt(
        (yy - center[0]) ** 2 + (xx - center[1]) ** 2
    )  # Be mindful of the index inversion between itk and numpy
    blob = (circle <= (radius / spacing)).astype(np.float64) * intensity
    return blob


@pytest.fixture(scope="module")
def one_blob():
    numpy_blob = _create_numpy_blob(
        size=(100, 100), center=(25, 50), radius=1.0, spacing=0.5, intensity=255
    )
    sitk_image = sitk.GetImageFromArray(numpy_blob)
    sitk_image.SetSpacing((0.5, 0.5))

    return sitk_image


@pytest.fixture(scope="module")
def two_blobs():
    blob1 = _create_numpy_blob(
        size=(100, 100), radius=1.5, spacing=1.1, center=(25, 50), intensity=255
    )
    blob2 = _create_numpy_blob(
        size=(100, 100), radius=1.5, spacing=1.1, center=(50, 75), intensity=155
    )
    sitk_image = sitk.GetImageFromArray(blob1 + blob2)
    sitk_image.SetSpacing((1.1, 1.1))

    return sitk_image


@pytest.fixture(scope="module")
def six_small_blobs_one_big_blob():
    big_blob = _create_numpy_blob(
        size=(200, 200), spacing=1.1, radius=6, center=(100, 100), intensity=255
    )
    small_blob_locations = [
        (25, 50),
        (25, 100),
        (25, 150),
        (175, 50),
        (175, 100),
        (175, 150),
    ]
    small_blob_radii = [1.1, 1.5, 2.0, 2.5, 1.4, 2.2]

    for loc, radius in zip(small_blob_locations, small_blob_radii):
        big_blob += _create_numpy_blob(
            size=(200, 200), spacing=1.1, intensity=125, center=loc, radius=radius
        )

    sitk_image = sitk.GetImageFromArray(big_blob)
    sitk_image.SetSpacing((1.1, 1.1))
    return sitk_image


def test_finds_one_blob(one_blob) -> None:
    blobs = detect_blobs(one_blob, one_blob > 60, "MR")
    assert len(blobs) == 1


def test_finds_correct_center(one_blob) -> None:
    blob_list = detect_blobs(one_blob, one_blob > 60, "MR")
    assert (blob_list[0][0], blob_list[0][1]) == pytest.approx((25 * 0.5, 50 * 0.5))


def test_finds_two_centers(two_blobs) -> None:
    blob_list = detect_blobs(two_blobs, two_blobs > 60, "MR")

    assert (blob_list[0][0], blob_list[0][1]) == pytest.approx((25 * 1.1, 50 * 1.1))
    assert (blob_list[1][0], blob_list[1][1]) == pytest.approx((50 * 1.1, 75 * 1.1))


def test_finds_small_blobs_ignores_big_blob(six_small_blobs_one_big_blob) -> None:
    blob_list = detect_blobs(
        six_small_blobs_one_big_blob, six_small_blobs_one_big_blob > 60, "MR"
    )

    logger.debug(f"Blob list found is: {blob_list}")

    assert len(blob_list) == 6
    assert (blob_list[0][0], blob_list[0][1]) == pytest.approx((175 * 1.1, 50 * 1.1))
    assert (blob_list[5][0], blob_list[5][1]) == pytest.approx((25 * 1.1, 150 * 1.1))
