import SimpleITK as sitk
import logging


def _get_label_statistics(label_img: sitk.Image, img: sitk.Image):
    label_statistics = sitk.LabelIntensityStatisticsImageFilter()
    label_statistics.Execute(label_img, img)
    return label_statistics


modality_thresholds = {"MR": 65, "CT": 750}


def detect_blobs(
    img_slice: sitk.Image, mask_slice: sitk.Image, modality: str
) -> list[tuple[float, float]]:
    cc = sitk.ConnectedComponent(mask_slice > 0)
    label_statistics = _get_label_statistics(cc, img_slice)
    blobs_list = []

    for label_idx in label_statistics.GetLabels():
        if not 1 < label_statistics.GetPhysicalSize(label_idx) < 30.0:  # [mm²]
            continue

        logging.debug(
            f"Physical size of label {label_idx}: {label_statistics.GetPhysicalSize(label_idx)}"
        )
        logging.debug(
            f"Mean of label {label_idx}: {label_statistics.GetMean(label_idx)}"
        )

        if not label_statistics.GetMean(label_idx) > modality_thresholds[modality]:
            continue

        blobs_list.append(label_statistics.GetCenterOfGravity(label_idx))

    return blobs_list
