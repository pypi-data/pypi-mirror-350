import json
import os

import numpy as np
from aicsimageio.readers import CziReader

from napari_czi_reader.czi_reader_plugin.czi_metadata_processor import extract_key_metadata
from napari_czi_reader.czi_reader_plugin.metadata_dump import metadata_dump


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
    file_name = os.path.basename(path)
    channels = reader.dims.C
    try:
        mosaics = reader.dims.M
    except AttributeError:
        mosaics = 0

    try:
        # metadata_list = extract_key_metadata(reader, channels)
        metadata_list = metadata_dump(reader, channels)
    except ValueError as e:
        metadata_list = [{} for _ in range(channels)]

    file_name_trunked = truncate_filename(file_name, 20)


    layer_data_list = []
    for channel in range(channels):
        metadata = metadata_list[channel]
        print(f"Dev | Channel: {channel}, Dims: {reader.dims}")

        # if mosaics > 0:
        #     for m in range(reader.dims.M):
        #         tile = reader.get_image_data("YX")
        #         print(f"tile {m} shape:", tile.shape)
        # else:
        #     data = reader.get_image_data("ZYX", C=channel)
        data = reader.get_image_data()
        data = np.squeeze(data)




        if channels > 0:
            try:
                metadata["name"] = f'{int(float(metadata["metadata"]["EmissionWavelength"]))}λ - {file_name_trunked}'
            except KeyError:
                metadata["name"] = f"Channel {channel} | {file_name_trunked}"

        if not isinstance(metadata, dict):  # Holy shit, I'm making errors
            raise ValueError(f"Metadata for channel {channel} is not a dictionary. Got {type(metadata)}")

        print(f"[*] Metadata dump for channel: {channel}, size: {data.shape}")
        print(json.dumps(metadata_list, indent=2))

        if reader.dims.Z == 2:
            layer_data_list.append((data, metadata, "label"))
        else:
            layer_data_list.append((data, metadata, "image"))

    def _reader_callable(_path=None):
        # Napari expect a tuple -> (data, metadata, layer_type)
        # For multiple layers, napari can also take list[tuple] -> [(data, metadata, layer_type)]
        return layer_data_list

    return _reader_callable