import SimpleITK as sitk

from stereotacticframe.frame_protocol import FrameProtocol


def apply_transform(
    image: sitk.Image,
    transform: sitk.AffineTransform,
    frame: FrameProtocol,
    interpolator=sitk.sitkLinear,
) -> sitk.Image:
    return sitk.Resample(
        image,
        frame.get_size_based_on(image.GetSpacing()),
        transform,
        interpolator,
        frame.offset,
        image.GetSpacing(),
        frame.direction,
    )
