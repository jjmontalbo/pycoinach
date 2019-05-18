import struct
from collections import namedtuple


ScdHeader = namedtuple(
    'ScdHeader',
    ' '.join([
        'unknown_1_count',
        'unknown_2_count',
        'entry_count',
        'unknown_1',
        'unknown_1_offset',
        'entry_table_offset',
        'unknown_2_offset',
        'unknown_2',
        'unknown_offset_1',
    ]))

ScdHeaderFormat = struct.Struct('@HHHHIIIII')
