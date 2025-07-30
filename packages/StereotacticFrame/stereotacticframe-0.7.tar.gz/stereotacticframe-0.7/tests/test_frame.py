from pathlib import Path
import pytest
import SimpleITK as sitk

from stereotacticframe.frames import LeksellFrame
from stereotacticframe.frame_detector import FrameDetector
from stereotacticframe.slice_provider import AxialSliceProvider
from stereotacticframe.blob_detection import detect_blobs
from stereotacticframe.preprocessor import Preprocessor

TEST_MR_IMAGE_PATH = Path("tests/data/frame/t1_15T_test_volume.nii.gz")
TEST_MR_IMAGE_TRANSFORM = (
    1.000,
    0.0109,
    -0.0233,
    -0.0116,
    1.000,
    -0.0288,
    0.0230,
    0.0291,
    0.999,
    -103.7,
    18.7,
    88.0,
)
TEST_CT_IMAGE_PATH = Path("tests/data/frame/test_ct_volume.nii.gz")
TEST_CT_IMAGE_TRANSFORM = (
    0.999,
    0.03089,
    -0.0139,
    -0.0307,
    0.999,
    0.0139,
    0.0143,
    -0.0135,
    1.000,
    -96.7,
    64.7,
    -761.0,
)


@pytest.fixture
def correct_ct_path(tmp_path) -> Path:
    """To save memory, the ct in the data path, is downsampled and downcast to uint8"""
    sitk_image = sitk.ReadImage(TEST_CT_IMAGE_PATH)
    upcast = sitk.Cast(sitk_image, sitk.sitkFloat32)
    rescaled = sitk.RescaleIntensity(upcast, outputMinimum=-1000, outputMaximum=3000)
    rescaled.CopyInformation(sitk_image)
    correct_ct_path = tmp_path.joinpath("ct_correct_scale.nii.gz")
    sitk.WriteImage(rescaled, correct_ct_path)
    return correct_ct_path


@pytest.mark.longrun
def test_align_leksell_frame_mr() -> None:
    detector = FrameDetector(
        LeksellFrame(),
        AxialSliceProvider(TEST_MR_IMAGE_PATH, Preprocessor("MR")),
        detect_blobs,
        modality="MR",
    )

    detector.detect_frame()
    frame_transform = detector.get_transform_to_frame_space()

    assert frame_transform.GetParameters() == pytest.approx(
        TEST_MR_IMAGE_TRANSFORM, rel=1e-2
    )


@pytest.mark.longrun
def test_align_leksell_frame_ct(correct_ct_path) -> None:
    detector = FrameDetector(
        LeksellFrame(),
        AxialSliceProvider(correct_ct_path, Preprocessor("CT")),
        detect_blobs,
        modality="CT",
    )

    detector.detect_frame()
    frame_transform = detector.get_transform_to_frame_space()

    assert frame_transform.GetParameters() == pytest.approx(
        TEST_CT_IMAGE_TRANSFORM, rel=1e-2
    )
