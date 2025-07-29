from astropy.io import fits
import os

def load_fits_file(filepath):
    """
    Loads the FITS file at the given path.

    Parameters:
        filepath (str): Path to the FITS file.

    Returns:
        data (ndarray): Image data.
        header (fits.Header): FITS header.

    """
    with fits.open(filepath) as hdul:
        data = hdul[0].data
        header = hdul[0].header
    return data, header

def get_imagetype(header):
    """
    Read the IMAGETYP keyword from the header of a FITS file.

    Parameters:
         header (fits.Header): FITS header.

    Returns:
        imagetype (str): Image type as a string.
    """
    imagetype = header['IMAGETYP'].strip().lower()
    return imagetype


def save_fits_file(filepath,  data, header=None, overwrite=True):
    """
    Save a FITS file with the given data and header.

    Parameters:
        filepath (str): Path to the output file.
        data (ndarray): Image data.
        header (fits.Header, optional): FITS header to include.
        overwrite (bool): Whether to overwrite existing file.
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    fits.writeto(filepath, data, header, overwrite=overwrite)
    print(f"Saved FITS file: {filepath}")

def group_files_by_imagetype(files, keywords=('bias', 'dark', 'lamp_dark', 'flat', 'lamp', 'light')):
    """
    Group FITS files by IMAGETYP keyword.

    Parameters:
        files (list): List of FITS file paths.
        keywords (tuple): Tuple of image type keywords to group (default: common types).

    Returns:
        groups (dict): Dictionary with imagetype as key and list of data arrays as value.
        headers (dict): Dictionary with imagetype as key and list of FITS headers as value.
    """
    groups = {key: [] for key in keywords}
    headers = {key: [] for key in keywords}

    for file in files:
        data, header = load_fits_file(file)
        imagetyp = get_imagetype(header).lower()
        for key in keywords:
            if key == imagetyp:
                groups[key].append(data)
                headers[key].append(header)
                break  # stop after first match to avoid double-counting

    return groups, headers


def get_filepaths_from_directory(filepath, filetype='.fits'):
    """
    Get a list of filepaths from a given directory.

    Parameters:
         filepath (str): Path to the directory.
         filetype (str): File extension to filter by (default: '.fits').

    Returns:
        filepaths (list): List of filepaths for the given filetype in directory.
    """
    filepaths = [os.path.join(filepath, f)
             for f in os.listdir(filepath)
             if f.lower().endswith(filetype)]
    return filepaths