import struct
from collections import namedtuple


ScdEntryHeader = namedtuple(
    'ScdEntryHeader',
    ' '.join([
        'data_size',
        'channel_count',
        'frequency',
        'codec',
        'loop_start_sample',
        'loop_end_sample',
        'samples_offset',
        'aux_chunk_count',
        'unknown1',
    ]))

ScdEntryHeaderFormat = struct.Struct('@IIIIIIIHH')
