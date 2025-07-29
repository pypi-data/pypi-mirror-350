import matplotlib.pyplot as plt
import numpy as np

class Spectrum:
    def __init__(self, wavelength, flux):
        """
        Initialize the spectrum object with a given set of attributes.

        Attributes:
            wavelength (ndarray): Wavelength axis of the spectrum
            flux (ndarray): Flux axis of the spectrum
        """
        self.wavelength = wavelength
        self.flux = flux

    def plot(self, title="Spectrum"):
        """
        Plot the spectrum and give it a title.

        Parameters:
            title (str): Title for the plot.
        """
        plt.figure()
        plt.plot(self.wavelength, self.flux, label='Flux')
        plt.xlabel('Wavelength')
        plt.ylabel('Flux')
        plt.title(title)
        plt.legend()
        plt.show()

    def save_spectrum_to_txt(self, filepath="spectrum.txt"):
        """
        Save the 1D spectrum to a text file with two columns: wavelength and flux.

        The output is tab-separated and includes a header line.

        Parameters:
            filepath (str): Path to the output .txt file. Defaults to 'spectrum.txt'.
        """
        np.savetxt(filepath, np.column_stack((self.wavelength, self.flux)),
                   header="Wavelength\tFlux", fmt="%.6f", delimiter="\t")