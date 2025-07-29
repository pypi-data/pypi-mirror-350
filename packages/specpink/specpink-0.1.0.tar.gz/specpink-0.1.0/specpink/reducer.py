import numpy as np
import matplotlib.pyplot as plt
import os
from specpink.spectrum import Spectrum
from specpink.utils import group_files_by_imagetype, get_filepaths_from_directory, save_fits_file


class Reducer:
    """
    A class to perform spectroscopic data reduction using calibration files.

    Attributes:
        calibration_files_path : str
            Path to the directory containing calibration FITS files.
        calibration_data : dict
            Dictionary of calibration image data grouped by IMAGETYP.
        calibration_headers : dict
            Dictionary of headers for each calibration frame type.
    """
    def __init__(self, calibration_files_path):
        """
        Initialize the Reducer with the path to calibration files.

        Parameters:
            calibration_files_path (str): Path to directory containing calibration FITS files.
        """
        self.calibration_files_path = calibration_files_path
        self.calibration_data = self._load_calibration()[0]
        self.calibration_headers = self._load_calibration()[1]

    def _load_calibration(self):
        """
        Load calibration frames from the given path.

        Returns:
            cal_data (dict): Dictionary with calibration frame data arrays.
            headers (dict): Dictionary with calibration header data arrays.
        """
        calibration_files = get_filepaths_from_directory(self.calibration_files_path)
        cal_data, headers = group_files_by_imagetype(calibration_files)
        return cal_data, headers

    def bias_subtraction(self):
        """
        Subtract the bias frame from the other calibration frames.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after bias subtraction.
        """
        bias = self.calibration_data['bias'][0]
        if bias is not []:
            self.calibration_data['dark'] = self.calibration_data['dark'][0]-bias
            self.calibration_data['lamp_dark'] = self.calibration_data['lamp_dark'][0]-bias
            self.calibration_data['lamp'] = self.calibration_data['lamp'][0]-bias
            self.calibration_data['light'] = self.calibration_data['light'][0]-bias
            print('Bias frame subtracted from frames.')
            return self.calibration_data
        else:
            print('No bias frames provided. Returning uncorrected calibration frames.')
            return self.calibration_data

    def dark_subtraction(self):
        """
        Subtracts the dark frames from the science frame.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) dark subtraction.
        """
        dark = self.calibration_data['dark']
        if dark is not []:
            self.calibration_data['light'] = self.calibration_data['light'] - dark
            print('Dark frame subtracted from science frame.')
            return self.calibration_data
        else:
            print('No dark frame provided. Returning uncorrected science frame.')
            return self.calibration_data

    def lamp_dark_subtraction(self):
        """
        Subtracts the lamp dark frame from the flat and lamp frames.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) lamp dark subtraction.
        """
        lamp_dark = self.calibration_data['lamp_dark']
        if lamp_dark is not []:
            self.calibration_data['lamp'] = self.calibration_data['lamp'] - lamp_dark
            print('Lamp Dark frame subtracted from flat and lamp frames.')
            return self.calibration_data
        else:
            print('No lamp dark frames provided. Returning uncorrected calibration frames.')
            return self.calibration_data

    def flat_fielding(self):
        """
        Apply flat-field correction to the science and reference frames.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) flat correction.
        """
        flat = self.calibration_data['flat'][0]
        if flat is not []:
            self.calibration_data['light'] = self.calibration_data['light']/flat
            self.calibration_data['lamp'] = self.calibration_data['lamp']/flat
            print('Flat field applied to science frame and reference frames.')
            return self.calibration_data
        else:
            print('No flat field provided. Returning uncorrected science frame.')
            return self.calibration_data

    def _select_trace_points(self):
        """
        Display the 2D light frame and allow the user to interactively select two points.

        These two points should lie along the center of the spectrum and are used to define
        the trace line for extraction.

        Returns:
            points (lst): A list containing two (x, y) coordinate tuples selected by the user.
        """
        science = self.calibration_data['light']
        plt.imshow(science, norm='log', origin='lower', cmap='gray', aspect='auto')
        plt.title("Click 2 points along the center of the spectrum")
        points = plt.ginput(2)
        plt.close()
        return points

    def _compute_trace(self, p1, p2):
        """
        Compute a straight-line trace between two user-selected points.

        This trace is used to define the aperture path through which the spectrum is extracted.

        Parameters:
            p1 (tuple): First (x, y) coordinate selected by the user.
            p2 (tuple): Second (x, y) coordinate selected by the user.

        Returns:
            x, y (tuple): Arrays (x, y) representing the traced pixel coordinates along the line.
        """
        x1, y1 = p1
        x2, y2 = p2
        x = np.arange(int(x1), int(x2) + 1)
        y = y1 + (y2 - y1) / (x2 - x1) * (x - x1)
        x = x.astype(int)
        y = y.astype(int)
        return x, y

    def _extract_aperture(self, x_trace, y_trace, aperture_radius=10):
        """
        Extract flux along a trace line by summing over a vertical aperture at each x position.

        The flux is averaged within a window of ±aperture_radius pixels centered on the trace,
        and normalized to its maximum value.

        Parameters:
            x_trace (np.ndarray): X-coordinates of the trace.
            y_trace (np.ndarray): Y-coordinates of the trace.
            aperture_radius (int): Half-width of the aperture in the spatial (y) direction.

        Returns:
            flux (np.ndarray): Normalized 1D flux array extracted from the 2D image.
        """
        science = self.calibration_data['light']
        flux = []
        for x, y_center in zip(x_trace, y_trace):
            y_min = int(y_center - aperture_radius)
            y_max = int(y_center + aperture_radius + 1)
            flux_val = np.mean(science[y_min:y_max, x])
            flux.append(flux_val)
        flux = np.array(flux)/np.max(flux)
        return flux

    def extract_spectrum(self):
        """
        Extract a 1D spectrum from the calibrated 2D science or reference frame.

        Returns:
            self.calibration_data (dict): Dictionary with calibration frame data arrays after (attempted) generation of a compressed spectrum.
        """
        p1, p2 = self._select_trace_points()

        x_trace, y_trace = self._compute_trace(p1, p2)

        flux = self._extract_aperture(x_trace, y_trace)
        wavelength = x_trace.astype(float)

        return Spectrum(wavelength, flux)

    def save_master_frames(self, output_dir='master_files'):
        """
        Save all stacked calibration frames as FITS files in the given directory.

        Parameters:
            output_dir (str): Directory where master FITS files will be saved.
        """
        for key, frame in self.calibration_data.items():
            if frame is not []:
                header = self.calibration_headers[key][0]
                filename = os.path.join(output_dir, f"master_{key}.fits")
                save_fits_file(filename, frame, header)
            else:
                print(f"No master frame to save for {key}")