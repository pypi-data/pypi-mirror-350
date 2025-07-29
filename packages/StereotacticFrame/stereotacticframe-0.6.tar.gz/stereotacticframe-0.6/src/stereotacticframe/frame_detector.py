from __future__ import annotations

from typing import Protocol, Callable
import SimpleITK as sitk
import numpy as np
import pyvista as pv
from vtk import vtkIterativeClosestPointTransform, vtkMatrix4x4
import logging

from stereotacticframe.frame_protocol import FrameProtocol

logger = logging.getLogger(__name__)


class SliceProviderProtocol(Protocol):
    def next_image_mask_pair(self) -> tuple[sitk.Image, sitk.Image]: ...

    def is_empty(self) -> bool: ...

    def get_current_z_coordinate(self) -> float: ...


class PreprocessorProtocol(Protocol):
    def process(self, image: sitk.Image) -> sitk.Image: ...


featureImage = sitk.Image
maskImage = sitk.Image
modality = str

BlobDetectorType = Callable[
    [featureImage, maskImage, modality], list[tuple[float, float]]
]


def _create_lines(
    edges: list[tuple[int, int]], nodes: list[tuple[float, float, float]]
) -> pv.PolyData:
    line_mesh = pv.PolyData()
    for edge in edges:
        point0 = nodes[edge[0]]
        point1 = nodes[edge[1]]
        line_mesh += pv.Line(point0, point1)  # type: ignore
    return line_mesh  # type: ignore


def _iterative_closest_point(
    source: pv.PolyData,
    target: pv.PolyData,
    iterations: int,
    number_of_landmarks: int = 2_000,
    start_by_mathing_centroids: bool = True,
) -> vtkIterativeClosestPointTransform:
    icp = vtkIterativeClosestPointTransform()
    icp.SetSource(source)
    icp.SetTarget(target)
    icp.SetMaximumNumberOfIterations(iterations)
    icp.SetMaximumNumberOfLandmarks(number_of_landmarks)
    icp.StartByMatchingCentroidsOff()
    if start_by_mathing_centroids:
        icp.StartByMatchingCentroidsOn()
    icp.GetLandmarkTransform().SetModeToRigidBody()
    icp.Update()
    return icp


def _transform4x4_to_sitk_affine(vtk_matrix: vtkMatrix4x4) -> sitk.Transform:
    dimension = 3  # dimension is always 3 in a 4x4 transform
    affine = sitk.AffineTransform(dimension)
    parameters = list(affine.GetParameters())
    for i in range(dimension):
        for j in range(dimension):
            parameters[i * dimension + j] = vtk_matrix.GetElement(i, j)
    for i in range(3):
        parameters[i + dimension * dimension] = vtk_matrix.GetElement(i, dimension)
    affine.SetParameters(parameters)
    return affine


def calculate_frame_extent_3d(
    frame_dimensions: tuple[float, float, float],
    voxel_spacing: tuple[float, float, float],
    offset: tuple[float, float, float],
) -> tuple[int, ...]:
    extent = tuple()
    for dim in range(len(frame_dimensions)):
        frame_dim = frame_dimensions[dim]
        current_voxel_spacing = voxel_spacing[dim]
        offs = offset[dim]
        extent += (round((frame_dim + 2 * abs(offs)) / current_voxel_spacing),)

    return extent


class FrameDetector:
    def __init__(
        self,
        frame: FrameProtocol,
        slice_provider: SliceProviderProtocol,
        blob_detector: BlobDetectorType,
        modality: str,
    ):
        self._frame = frame
        self._slice_provider = slice_provider
        self._blob_detector = blob_detector
        self._point_cloud: pv.PolyData | None = None
        self._sitk_transform: sitk.Transform | None = None
        self._frame_object: pv.PolyData = _create_lines(
            frame.get_edges(modality), frame.nodes
        )
        self._modality = modality

    # Quite a bit of cohesion here, not sure if it's a problem, since it has to come together somewhere
    def detect_frame(self) -> None:
        blobs_list = []
        while not self._slice_provider.is_empty():
            next_img_slice, next_mask_slice = (
                self._slice_provider.next_image_mask_pair()
            )
            blobs_list += [
                two_d_point + (self._slice_provider.get_current_z_coordinate(),)
                for two_d_point in self._blob_detector(
                    next_img_slice, next_mask_slice, self._modality
                )
            ]
        self._point_cloud = pv.PolyData(np.asarray(blobs_list))

    def get_transform_to_frame_space(self) -> sitk.Transform:
        if self._point_cloud is None:
            raise ValueError(
                "Detect frame was not run or there is a problem with detect frame."
            )

        point_cloud = self._point_cloud.copy()
        # Run 1 iteration to do centroid allignment
        centroid_transform = _iterative_closest_point(
            point_cloud, self._frame_object, iterations=1
        )

        centroid_matrix = centroid_transform.GetMatrix()
        centroid_inverse_matrix = centroid_matrix.NewInstance()
        centroid_inverse_matrix.DeepCopy(centroid_matrix)
        centroid_inverse_matrix.Invert()

        point_cloud.transform(centroid_matrix)

        # Very liberally clean some points
        new_points = point_cloud.points

        right_points = new_points[new_points[..., 0] < 40]  # Keep only right points
        left_points = new_points[new_points[..., 0] > 150]  # Keep only left points

        new_cloud = pv.PolyData(right_points) + pv.PolyData(left_points)

        new_cloud.transform(centroid_inverse_matrix)

        initial_transform = _iterative_closest_point(
            new_cloud, self._frame_object, 1_000
        )
        point_cloud = self._point_cloud.copy()

        initial_matrix = initial_transform.GetMatrix()
        initial_inverse_matrix = initial_matrix.NewInstance()
        initial_inverse_matrix.DeepCopy(initial_matrix)
        initial_inverse_matrix.Invert()
        new_cloud.transform(initial_inverse_matrix)

        point_cloud.transform(initial_matrix)

        # Remove upper 20mm and lower 20mm
        new_points = point_cloud.points
        new_points = new_points[new_points[..., 2] > -110]  # Remove top 10 mm
        new_points = new_points[new_points[..., 2] < -10]  # Remove bottom 10 mm

        right_points = new_points[new_points[..., 0] < 10]  # Keep only right points
        left_points = new_points[new_points[..., 0] > 180]  # Keep only left points
        new_cloud = pv.PolyData(right_points) + pv.PolyData(left_points)

        new_cloud.transform(initial_inverse_matrix)

        refined_transform = _iterative_closest_point(
            new_cloud, self._frame_object, iterations=1_000
        )
        refined_matrix = refined_transform.GetMatrix()
        refined_inverse_matrix = refined_matrix.NewInstance()
        refined_inverse_matrix.DeepCopy(refined_matrix)
        refined_inverse_matrix.Invert()

        point_cloud = self._point_cloud.copy()
        point_cloud.transform(refined_matrix)

        new_cloud.transform(refined_matrix)

        closest_points = self._calculate_closest_points_in_frame_to(
            point_cloud.points.copy()
        )

        exact_distance = np.linalg.norm(point_cloud.points - closest_points, axis=1)

        new_points = point_cloud.points
        new_points = new_points[np.nonzero(exact_distance < 3.0)]
        new_points = new_points[new_points[..., 2] > -110]  # Remove top 10 mm
        new_points = new_points[new_points[..., 2] < -10]  # Remove bottom 10 mm
        right_points = new_points[new_points[..., 0] < 10]  # Keep only right points
        left_points = new_points[new_points[..., 0] > 180]  # Keep only left points
        new_cloud = pv.PolyData(right_points) + pv.PolyData(left_points)

        new_cloud.transform(refined_inverse_matrix)

        final_transform = _iterative_closest_point(
            new_cloud, self._frame_object, iterations=2_000
        )

        final_matrix = final_transform.GetMatrix()
        final_inverse_matrix = final_matrix.NewInstance()
        final_inverse_matrix.DeepCopy(final_matrix)
        final_inverse_matrix.Invert()
        new_cloud.transform(final_matrix)

        point_cloud = self._point_cloud.copy()
        point_cloud.transform(final_matrix)

        closest_points_in_frame = self._calculate_closest_points_in_frame_to(
            new_cloud.points
        )
        self._set_mean_max(closest_points_in_frame, new_cloud.points)

        logger.info(f"Mean detection error: {self._mean_error}")
        logger.info(f"Max detection error: {self._max_error}")

        final_itk_transform = _transform4x4_to_sitk_affine(final_matrix)
        return final_itk_transform.GetInverse()

    def _calculate_closest_points_in_frame_to(
        self, points: pv.NumpyArray
    ) -> pv.NumpyArray:
        _, closest_points = self._frame_object.find_closest_cell(
            points, return_closest_point=True
        )
        return closest_points

    def _set_mean_max(self, points: pv.NumpyArray, poly_points: pv.NumpyArray) -> None:
        distances = np.linalg.norm(points - poly_points, axis=1)
        self._mean_error = distances.mean()
        self._max_error = distances.max()
