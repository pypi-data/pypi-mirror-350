import typer

import SimpleITK as sitk
from pathlib import Path
from typing import Optional
import logging

from stereotacticframe.frames import LeksellFrame
from stereotacticframe.frame_detector import FrameDetector
from stereotacticframe.slice_provider import AxialSliceProvider
from stereotacticframe.blob_detection import detect_blobs
from stereotacticframe.preprocessor import Preprocessor
from stereotacticframe.transforms import apply_transform

app = typer.Typer()


@app.command()
def calculate(
    input_image_path: Path,
    modality: str,
    output_transform_path: Optional[Path],
    log_dir: Optional[Path],
    logging_on: bool = False,
) -> None:
    if log_dir:
        fh = logging.FileHandler(log_dir)
        if logging_on:
            fh.setLevel(logging.DEBUG)
        logging.root.addHandler(fh)
    if logging_on:
        logging.root.setLevel(logging.DEBUG)

    # This could be generalized to any frame with a frame option
    frame = LeksellFrame()

    preprocessor = Preprocessor(modality)

    provider = AxialSliceProvider(input_image_path, preprocessor)

    # bit anoying that I have to give modality as input for preprocessor and for framedetector
    detector = FrameDetector(frame, provider, detect_blobs, modality)

    detector.detect_frame()

    transform = detector.get_transform_to_frame_space()

    if not output_transform_path:
        output_transform_path = Path("./output.txt")

    sitk.WriteTransform(transform, output_transform_path)


@app.command()
def apply(image_path: Path, transform_path: Path, output_image_path: Path):
    frame = LeksellFrame()

    image = sitk.ReadImage(image_path)
    transform = sitk.ReadTransform(transform_path)

    sitk.WriteImage(apply_transform(image, transform, frame), output_image_path)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app()
