import io
import numpy as np
import soundfile as sf
from mutagen.oggvorbis import OggVorbis
from .sound import scd_file


def generate_entry(path):
    with open(path, 'rb') as f:
        scd = scd_file.ScdFile(f)
    if len(scd.entries) > 0:
        entry = scd.entries[0]
        ogg = io.BytesIO(entry.get_decoded())
        return entry, ogg
    return None, None


def export_test(path, entry, ogg):
    name, ext = path.rsplit('/', 1)[-1].rsplit('.', 1)

    ogg.seek(0)

    # Fix loop information
    ogg_metadata = OggVorbis(ogg)
    for k, v in ogg_metadata.items():
        ogg_metadata[k.upper()] = v
    ogg.seek(0)
    ogg_metadata.save(ogg)

    with open(f'./music/ex2/{name}.ogg', 'wb') as f:
        ogg.seek(0)
        f.write(ogg.read())

    return entry


def pysoundfile_test(path, entry, ogg, loops=2):
    name, ext = path.rsplit('/', 1)[-1].rsplit('.', 1)

    ogg.seek(0)
    data, samplerate = sf.read(ogg)

    ogg.seek(0)
    ogg_metadata = OggVorbis(ogg)

    try:
        loop_start = int(ogg_metadata['loopstart'][0])
        loop_end = int(ogg_metadata['loopend'][0])
    except KeyError:
        loop_start, loop_end = None, None

    if loop_start is not None:
        data_loop = data[loop_start:loop_end]
        for i in range(loops):
            data = np.concatenate((data, data_loop), axis=0)

    sf.write(f'./music/ex2/{name}.flac', data, samplerate)
