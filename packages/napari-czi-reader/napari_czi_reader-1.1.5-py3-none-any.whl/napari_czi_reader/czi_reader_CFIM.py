import json
import os

import numpy as np
from aicsimageio.readers import CziReader
from aicspylibczi import CziFile

from napari_czi_reader.czi_metadata_processor import (extract_key_metadata)
from napari_czi_reader.metadata_dump import metadata_dump

# CONFIG
DEBUG = False
CHANNEL_NAME = False


def truncate_filename(filename, max_chars, split_before_max=True):
    """
        Splits a filename into words and truncates it to max_chars.
        If split_before_max is False, it will include the first word that exceeds max_chars.
    """
    words = filename.split()
    result = []
    current_length = 0

    for word in words:
        extra = 1 if result else 0

        if current_length + extra + len(word) > max_chars:
            if not result:
                result.append(word[:max_chars])

            if not split_before_max:
                result.append(" ")
                result.append(word)
            break

        if extra:
            result.append(" ")
        result.append(word)
        current_length += extra + len(word)

    return "".join(result)

os.environ["AICS_PYLIBCZI_DISABLE_OPENMP"] = "1"
# TODO: Add to settings, Trunked filename length, split_before_max
# TODO: Change reader to use aicspylibczi
def read_czi(path):
    """
        Loads a .czi file and return the data in a proper callable format.
        Made because I could not get a direct reader to work with napari.

        Parameters:
            path: str -> Path to the .czi file.

        Returns:
            callable -> A callable that returns a list of tuples with the data, metadata and layer type.
                        Required format for napari readers.
    """
    reader = CziReader(path)
    czi = CziFile(path)
    file_name = os.path.basename(path)
    dimensions = czi.get_dims_shape()[0]
    channels = dimensions.get("C", (0,0)) ## Gets max channels

    xml_meta = czi.meta

    try:
        # metadata_list = extract_key_metadata(xml_meta, channels)
        metadata_list = metadata_dump(xml_meta, channels[1])
    except ValueError as e:
        metadata_list = [{} for _ in range(*channels)]

    file_name_trunked = truncate_filename(file_name, 20)


    layer_data_list = []
    for channel in range(*channels):
        metadata = metadata_list[channel]
        if DEBUG:
            print(f"Debug | Channel: {channel}, Dims: {czi.dims}")

        ## Expected dim order: 'STCZMYX'
        if czi.is_mosaic():
            data = czi.read_mosaic(C=channel)
        else:
            data = czi.read_image(C=channel)
            # data = reader.get_image_data("ZYX", C=channel)
        data = np.squeeze(data[0])


        if DEBUG:
            print(f"Debug | Channel: {channel}, data shape: {data.shape}")

        if channels[1] > 1:
            try:
                metadata["name"] = f'{int(float(metadata["metadata"]["EmissionWavelength"]))}λ - {file_name_trunked}'
            except KeyError:
                metadata["name"] = f"C_{channel} - {file_name_trunked}"

        if not isinstance(metadata, dict):  # Holy shit, I'm making errors
            raise ValueError(f"Metadata for channel {channel} is not a dictionary. Got {type(metadata)}")

        if dimensions.get("Z", (3,3))[1] == 2:
            layer_data_list.append((data, metadata, "label"))
        else:
            layer_data_list.append((data, metadata, "image"))

    def _reader_callable(_path=None):
        # Napari expect a tuple -> (data, metadata, layer_type)
        # For multiple layers, napari can also take list[tuple] -> [(data, metadata, layer_type)]
        return layer_data_list

    return _reader_callable
