import json
from xml.etree import ElementTree as ET

from aicsimageio.readers import CziReader
import xmltodict

from napari_czi_reader.library_workarounds.RangeDict import RangeDict

# helper for safe nested dict access
def get_in(dct: dict, keys: list, default=None):
    cur = dct
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur

debug = False


def metadata_dump(czi_read_file, channels) -> list[dict]:
    """
    Dumps the metadata of a .czi file to a json file.
    """

    raw_xml = ET.tostring(czi_read_file.metadata, encoding="utf-8")
    ome_dict = xmltodict.parse(raw_xml)

    if debug:
        print("[*] Metadata dump:")
        print(json.dumps(ome_dict, indent=2))

    # safe nested values
    image_dict = get_in(ome_dict, ["ImageDocument","Metadata","Information","Image"], {})
    aq_mode = get_in(ome_dict, ["ImageDocument","Metadata","Experiment","ExperimentBlocks","AcquisitionBlock","AcquisitionModeSetup"], {})
    track_setup = get_in(ome_dict, ["ImageDocument","Metadata","Experiment","ExperimentBlocks","AcquisitionBlock","MultiTrackSetup","TrackSetup"], [])
    # ensure list
    if isinstance(track_setup, dict):
        track_list = [track_setup]
    elif isinstance(track_setup, list):
        track_list = track_setup
    else:
        track_list = []

    # pix count
    try:
        pixcount = [int(image_dict.get("SizeY", 0)), int(image_dict.get("SizeX", 0))]
    except Exception:
        pixcount = [0, 0]
    # spacing
    try:
        yx_spacing = [float(aq_mode.get("ScalingX", 0)) * 1e6, float(aq_mode.get("ScalingY", 0)) * 1e6]
    except Exception:
        yx_spacing = [1.0, 1.0]
    metadata = {"size": pixcount, "scale": yx_spacing, "units": "micrometre"}
    # wavelengths
    wavelengths = []
    for td in track_list:
        att = td.get("Attenuators", {}).get("Attenuator", {})
        if isinstance(att, list):
            for a in att:
                w = a.get("Wavelength")
                if w is not None:
                    wavelengths.append(w)
        else:
            w = att.get("Wavelength")
            if w is not None:
                wavelengths.append(w)
    # channels
    dims = get_in(image_dict, ["Dimensions","Channels","Channel"], [])
    if isinstance(dims, dict): dims_list = [dims]
    elif isinstance(dims, list): dims_list = dims
    else: dims_list = []
    channel_metadata_list = []
    for idx in range(channels):
        em = dims_list[idx].get("EmissionWavelength") if idx < len(dims_list) else None
        try:
            wv = round(float(em)) if em else 0.0
        except Exception:
            wv = 0.0
        # fallback
        if wv == 0.0 and idx < len(wavelengths):
            try: wv = round(float(wavelengths[idx]))
            except Exception: wv = 0.0
        try:
            cmap = wavelength_to_color[wv]
        except Exception:
            cmap = "Grey"
        channel_metadata_list.append({
            "metadata": {**metadata, "wavelength": wv},
            "scale": yx_spacing,
            "units": metadata["units"],
            "colormap": cmap
        })
    return channel_metadata_list


wavelength_to_color = RangeDict(
    [
        (0, 380, "Grey"),
        (380, 450, "Violet"),
        (450, 485, "Blue"),
        (485, 500, "Cyan"),
        (500, 565, "Green"),
        (565, 590, "Yellow"),
        (590, 625, "Orange"),
        (625, 740, "Red")])
if __name__ == "__main__":
    czifile = CziReader(r"C:\Users\marku\OneDrive - Københavns Erhvervsakademi\Desktop\Nye billeder til test\C01 validation 1-Tile-4-Stain-Intellesis Trainable Segmentation-Output-01.czi")
    metadata = metadata_dump(czifile, 2)

    print(json.dumps(metadata, indent=2))
