import os
import numpy as np
from scipy.ndimage import gaussian_filter
from specpink.utils import save_fits_file, group_files_by_imagetype, get_filepaths_from_directory


class Stacker:
    """
    Class to create stacked calibration frames from FITS files.
    """

    def __init__(self, filepath):
        """
        Initialize the Calibrator with a list of FITS files or directory path.

        Parameters:
            filepath (str): Paths to FITS files to be processed.
        """
        self.files = get_filepaths_from_directory(filepath)
        self.stacks = {'bias': None, 'dark': None, 'lamp_dark': None, 'flat': None, 'lamp': None, 'light': None}
        self.stack_headers = {'bias': None, 'dark': None, 'lamp_dark': None, 'flat': None, 'lamp': None, 'light': None}
        self.master_frames = {'bias': None, 'dark': None, 'lamp_dark': None, 'flat': None, 'lamp': None, 'light': None}

    def create_stacks(self):
        """
        Group FITS files by IMAGETYP and create median-stacked images.

        Returns:
            dict: Dictionary of stacked image arrays by type.
        """
        groups, headers = group_files_by_imagetype(self.files)

        for key in groups:
            if groups[key]:
                stack = np.stack(groups[key], axis=0)
                self.stacks[key] = np.median(stack, axis=0)
                stack_header = headers[key][0].copy()
                self.stack_headers[key] = stack_header
                print(f"Created {key} stack from {len(groups[key])} files")
            else:
                self.stacks[key] = None
                print(f"No {key} frames provided.")

        return self.stacks

    def normalize_flat(self):
        """
        Normalize the master flat field by removing large-scale features.

        Returns:
            ndarray or None: Normalized flat field image or None if unavailable.
        """
        if self.stacks['flat'] is not None:
            flat = self.stacks['flat']
            flat_gaussfiltered = gaussian_filter(flat, sigma=5)
            flat_normal = flat - flat_gaussfiltered
            flat_normal = flat_normal - np.min(flat_normal) + 0.001
            flat_normal = flat_normal / np.max(flat_normal)
            return flat_normal
        else:
            print('No flat field images provided to create normalized flat field.')
            return None

    def create_master_frames(self):
        """
        Create the final set of stacked calibration frames,
        including a normalized flat field.

        Returns:
            dict: Dictionary of master calibration frames.
        """
        if all(v is None for v in self.stacks.values()):
            print('No stacks created yet. Run create_stacks() first.')
            return None
        else:
            for key in self.stacks:
                if self.stacks[key] is not None:
                    self.master_frames[key] = self.stacks[key]

            flat_normal = self.normalize_flat()
            if flat_normal is not None:
                self.master_frames['flat'] = flat_normal
                print('Normalized flat field added to master frames.')
            else:
                print('No flat field image provided to add to master frames.')

            return self.master_frames

    def save_stacked_frames(self, output_dir='calibration_files'):
        """
        Save all stacked calibration frames as FITS files in the given directory.

        Parameters:
            output_dir (str): Directory where master FITS files will be saved.
        """
        for key, frame in self.master_frames.items():
            if frame is not None:
                header = self.stack_headers[key]
                filename = os.path.join(output_dir, f"stacked_{key}.fits")
                save_fits_file(filename, frame, header)
            else:
                print(f"No stacked frame to save for {key}")
