#!/usr/bin/env python
import glob
import SimpleITK as sitk
import numpy as np

def load_nifti(nifti_path, return_image=True, return_metadata=False):
    """
    Load a NIfTI file and optionally return its image data and spatial metadata.

    Args:
        nifti_path (str): Path to the NIfTI file (.nii or .nii.gz).
        return_image (bool): Whether to return the image data as a NumPy array.
        return_metadata (bool): Whether to return spatial metadata (origin, spacing, direction).

    Returns:
        tuple or np.ndarray or tuple: Depending on flags, returns:
            - image_data (np.ndarray) if return_image is True and return_metadata is False
            - (origin, spacing, direction) if return_image is False and return_metadata is True
            - (image_data, origin, spacing, direction) if both are True
    """
    itk_image = sitk.ReadImage(nifti_path)
    origin = itk_image.GetOrigin()
    spacing = itk_image.GetSpacing()
    direction = itk_image.GetDirection()

    image_data = None
    if return_image:
        image_data = sitk.GetArrayFromImage(itk_image)

    if return_image and return_metadata:
        return image_data, origin, spacing, direction
    elif return_image:
        return image_data
    elif return_metadata:
        return origin, spacing, direction
    else:
        return None


def convert_numpy_to_nifti(numpy_data, template_nifti_path, output_nifti_path):
    """
    Converts a NumPy array or .npy file to a NIfTI image using a template NIfTI file for spatial metadata.

    Args:
        numpy_data (str or np.ndarray): A NumPy array or a path to a .npy file containing the image data.
        template_nifti_path (str): Path to the template NIfTI (.nii.gz) file used to extract spatial metadata.
        output_nifti_path (str): Path where the output NIfTI file will be saved (.nii.gz).

    Returns:
        None
    """

    assert isinstance(numpy_data, np.ndarray) or isinstance(numpy_data, str)
    assert template_nifti_path.endswith(".nii.gz")
    assert output_nifti_path.endswith(".nii.gz")

    origin, spacing, direction = load_nifti(
        template_nifti_path, return_image=False, return_metadata=True
    )

    if not isinstance(numpy_data, np.ndarray):
        numpy_data = np.load(numpy_data)

    if numpy_data.ndim == 4 or numpy_data.ndim == 5:
        numpy_data = np.squeeze(numpy_data)

    itk_image = sitk.GetImageFromArray(numpy_data, isVector=False)
    itk_image.SetOrigin(origin)
    itk_image.SetSpacing(spacing)
    itk_image.SetDirection(direction)

    sitk.WriteImage(itk_image, output_nifti_path)

    
if __name__ == '__main__':
    
    pass