from specpink.stacker import Stacker
from specpink.reducer import Reducer

class Pipeline:
    """
    A class that defines a full spectroscopic data reduction pipeline.

    Attributes:
        raw_data_path (str): Path to the raw FITS files.
        stacked_data_path (str): Path to store stacked calibration frames.
        reduced_data_path (str): Path to store reduced science/calibrated data.
        spectrum_path (str): Path to save the extracted spectrum as a text file.
    """
    def __init__(self, raw_data_path, stacked_data_path, reduced_data_path, spectrum_path):
        """
        Initialize the Pipeline.

        Parameters:
            raw_data_path (str): Path to raw FITS files.
            stacked_data_path (str): Path to output stacked calibration files.
            reduced_data_path (str): Path to output reduced light and reference frames.
            spectrum_path (str): Path to output extracted spectrum in .txt format.
        """
        self.raw_data_path = raw_data_path
        self.stacked_data_path = stacked_data_path
        self.reduced_data_path = reduced_data_path
        self.spectrum_path = spectrum_path

    def full(self):
        """
        Run the full reduction pipeline:
            1. Stack calibration frames (bias, dark, flat, lamp, light)
            2. Generate and save master calibration frames
            3. Apply calibration corrections to science data
            4. Extract and save the 1D spectrum
            5. Plot the final spectrum
        """
        cal = Stacker(self.raw_data_path)
        cal.create_stacks()
        cal.create_master_frames()
        cal.save_stacked_frames(output_dir=self.stacked_data_path)

        red = Reducer(self.stacked_data_path)
        red.bias_subtraction()
        red.dark_subtraction()
        red.lamp_dark_subtraction()
        red.flat_fielding()
        red.save_master_frames(output_dir=self.reduced_data_path)

        spec = red.extract_spectrum()
        spec.save_spectrum_to_txt(self.spectrum_path)

        spec.plot()
