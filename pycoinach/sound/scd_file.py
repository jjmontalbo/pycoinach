import struct
import sys
from .scd_codec import ScdCodec
from .scd_entry_header import ScdEntryHeader, ScdEntryHeaderFormat
from .scd_header import ScdHeader, ScdHeaderFormat
from .scd_ogg_entry import ScdOggEntry


IS_LITTLE_ENDIAN = sys.byteorder == 'little'


class ScdFile:
    def __init__(self, source_file):
        if source_file:
            self.source_file = source_file
        else:
            raise ValueError('source_file is not defined.')

        self._use_little_endian = False
        self._input_buffer = None
        self.scd_header = None
        self.entries = []

        self.decode()

    def decode(self):
        self.source_file.seek(0)
        self._input_buffer = bytearray(self.source_file.read())

        self.init()

        file_header_size = self._read_int_16(0x0E)

        self.read_scd_header(file_header_size)

        entry_headers = []
        entry_chunk_offsets = []
        entry_data_offsets = []

        for i in range(self.scd_header.entry_count):
            header_offset = self._read_int_32(self.scd_header.entry_table_offset + 4 * i)

            entry_header = self.read_entry_header(header_offset)
            entry_headers.append(entry_header)

            entry_chunk_offset = header_offset + ScdEntryHeaderFormat.size
            entry_chunk_offsets.append(entry_chunk_offset)

            entry_data_offset = entry_chunk_offset
            for j in range(entry_header.aux_chunk_count):
                entry_data_offset += self._read_int_32(entry_data_offset + 4)
            entry_data_offsets.append(entry_data_offset)

        for i in range(self.scd_header.entry_count):
            self.entries.append(
                self.create_entry(
                    entry_headers[i],
                    entry_chunk_offsets[i],
                    entry_data_offsets[i],
                )
            )

        self._input_buffer = None

    def init(self):
        if self._read_int_64(0, little_endian=False) != 0x5345444253534346:
            raise ValueError('File format is not valid')

        ver_big_endian = self._read_int_32(8, little_endian=False)
        ver_little_endian = self._read_int_32(8, little_endian=True)

        if ver_big_endian == 2 or ver_big_endian == 3:
            self._use_little_endian = False
        elif ver_little_endian == 2 or ver_little_endian == 3:
            self._use_little_endian = True
        else:
            raise ValueError('Endianness')

    def read_scd_header(self, offset):
        size = ScdHeaderFormat.size
        self.scd_header = ScdHeader._make(
            ScdHeaderFormat.unpack(
                self._input_buffer[offset:offset + size],
            )
        )

    def read_entry_header(self, offset):
        size = ScdEntryHeaderFormat.size
        return ScdEntryHeader._make(
            ScdEntryHeaderFormat.unpack(
                self._input_buffer[offset:offset + size],
            )
        )

    def create_entry(self, header, chunks_offset, data_offset):
        if header.data_size == 0 or header.codec == ScdCodec.NONE:
            return None

        if (header.codec == ScdCodec.OGG):
            return ScdOggEntry(self, header, data_offset)
        else:
            raise NotImplementedError

    def _read_int_16(self, offset, little_endian=None):
        if little_endian is None:
            little_endian = self._use_little_endian
        buffer = self._input_buffer[offset:offset + 2]
        if IS_LITTLE_ENDIAN != little_endian:
            buffer = buffer[::-1]
        return struct.unpack('@H', buffer)[0]

    def _read_int_32(self, offset, little_endian=None):
        if little_endian is None:
            little_endian = self._use_little_endian
        buffer = self._input_buffer[offset:offset + 4]
        if IS_LITTLE_ENDIAN != little_endian:
            buffer = buffer[::-1]
        return struct.unpack('@I', buffer)[0]

    def _read_int_64(self, offset, little_endian=None):
        if little_endian is None:
            little_endian = self._use_little_endian
        buffer = self._input_buffer[offset:offset + 8]
        if IS_LITTLE_ENDIAN != little_endian:
            buffer = buffer[::-1]
        return struct.unpack('@Q', buffer)[0]
