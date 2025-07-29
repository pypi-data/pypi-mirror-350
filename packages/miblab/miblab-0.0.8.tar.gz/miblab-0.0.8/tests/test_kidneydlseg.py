import dbdicom as db
import numpy as np
import miblab.kidneydlseg as kidneydlseg
from src.miblab.data import zenodo_fetch
import os
import zipfile
import tempfile


def test_kidney_pc_dixon():
    # Create a temporary directory
    tmp_path = tempfile.mkdtemp()

    testdata = 'test_data_post_contrast_dixon.zip'
    testdatadoi = '15489381'

    # Download ZIP file to temp directory
    zenodo_fetch(testdata, tmp_path, testdatadoi)

    # Unzip inside temp directory
    zip_file_path = os.path.join(tmp_path, testdata)
    extracted_folder = unzip_file(zip_file_path, extract_to=tmp_path)

    # Load DICOM database
    database = db.database(path=extracted_folder)

    series_outphase = database.series(SeriesDescription='Dixon_post_contrast_out_phase')
    series_inphase = database.series(SeriesDescription='Dixon_post_contrast_in_phase')
    series_water = database.series(SeriesDescription='Dixon_post_contrast_water')
    series_fat = database.series(SeriesDescription='Dixon_post_contrast_fat')

    array_outphase, _ = series_outphase[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_inphase, _ = series_inphase[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_water, _ = series_water[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_fat, _ = series_fat[0].array(['SliceLocation'], pixels_first=True, first_volume=True)

    array = np.stack((array_outphase, array_inphase, array_water, array_fat), axis=0)

    mask = kidneydlseg.kidney_pc_dixon(array)

    assert np.sum(mask['leftkidney']) == 62284#

def unzip_file(zip_path, extract_to=None):
    if extract_to is None:
        extract_to = os.path.splitext(zip_path)[0]
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to