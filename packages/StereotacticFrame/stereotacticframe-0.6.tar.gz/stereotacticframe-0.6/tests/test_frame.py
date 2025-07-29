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
    0.9996676804848265,
    0.010930228058566386,
    -0.02334649242747307,
    -0.011601636801316218,
    0.9995173089262706,
    -0.02881928486880874,
    0.023020221927894116,
    0.029080565183757807,
    0.9993119583551053,
    -103.67898738835223,
    18.730087615696412,
    88.04311831261525,
)
TEST_CT_IMAGE_PATH = Path("tests/data/frame/test_ct_volume.nii.gz")
TEST_CT_IMAGE_TRANSFORM = (
    0.9994264094227612,
    0.03088102857421182,
    -0.013900151888597882,
    -0.03068924910695164,
    0.9994336346151039,
    0.013805071144110899,
    0.01431859412019365,
    -0.013370567461450374,
    0.9998080844783036,
    -96.72020193220573,
    64.67744237669116,
    -761.0367154855787,
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
        TEST_MR_IMAGE_TRANSFORM, rel=1e-3
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

    assert frame_transform.GetParameters() == pytest.approx(TEST_CT_IMAGE_TRANSFORM)
