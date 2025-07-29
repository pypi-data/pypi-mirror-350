import zstandard as zstd

from ..blk.FileInfo import FileType
from ..blk.Block import Block
from ..blk.Chunk import ChunkParser
from ..blk.ParamParser import BLKTypes
from ..BitStream import BitStream


class BlkParser:
    """
    a blk parser
    inputs:
    dat: the data to be parsed
    offset: how far along into the data the blk starts
    name_map: an optional parameter for blks that have a name map, see FileInfo.py for more info
    zstd_dict: an optional parameter for blks that have a zstd dict, see FileInfo.py for more info
    """

    def __init__(self, dat, offset=0, name_map: list[bytearray] = None, zstd_dict=None):
        if not isinstance(dat, BitStream):
            dat = BitStream(dat)
        dat.IgnoreBytes(offset)
        self.data = None
        self.blkType = FileType(dat.ReadBits(8, "blk_type")[0])  # gets blk type, the first byte
        if self.blkType == FileType.BBF:
            raise Exception("BLK is invalid type BBF")
        if not self.blkType.is_zstd():
            self.data = dat
        else:
            if self.blkType.needs_dict():
                if zstd_dict is None:
                    raise Exception("zstd dict is required")
            # print(dat.read(8).hex())
            # input()
            # print(dat.GetData())
            x = zstd.ZstdDecompressor(zstd_dict).stream_reader(dat) # bitstream doesnt implement RawIO, but it has the needed .read() func

            self.data = BitStream(x.read())

            x.close()
        self.names_in_name_map = self.data.ReadUleb(
            "names_in_name_map")  # gets the number of names in the name map
        self.names = None
        if self.blkType.is_slim():
            if name_map is None:
                print("BAD NAME MAP")
            self.names = []
            for name in name_map:
                try:
                    self.names.append(name.decode("utf-8"))
                except UnicodeDecodeError:
                    self.names.append("BADBADBAD" + name.decode("utf-8", errors="ignore"))
        else:
            self.name_map_size = self.data.ReadUleb("name_map_size")  # gets the size of the name map
            self.names = [x.decode("utf-8") for x in
                          self.data.ReadBits((self.name_map_size - 1) * 8, "names").split(b"\x00")]
            # print(self.names)
            self.data.IgnoreBytes(8)  # it only fetches size - 1 for speed to reduce slicing
            if len(self.names) != self.names_in_name_map:
                print("RED ALERT")
        self.num_of_blocks = self.data.ReadUleb("num_of_blocks")
        self.num_of_params = self.data.ReadUleb("num_of_params")
        self.params_data_size = self.data.ReadUleb("param_data_size")
        self.params_data = self.data.ReadBits(self.params_data_size * 8, "param_data")  # used later on, data
        '''
        here we are are skipping results creation and starting with chunks
        assume we are doing let chunks
        '''
        chunks = []
        parser = ChunkParser(self.names, BLKTypes(self.names, self.params_data))
        for i in range(self.num_of_params):
            chunks.append(parser.parse(self.data.ReadBits(8 * 8, "chunk")))

        # chunks = Chunks(self.data, self.num_of_params, self.names, B)
        blocks = []
        for i in range(self.num_of_blocks):  # this creates all the blocks
            name_id = self.data.ReadUleb("blk_name_Id")
            param_count = self.data.ReadUleb("blk_param_count")
            block_count = self.data.ReadUleb("blk_block_count")
            if block_count > 0:
                first_block_id = self.data.ReadUleb("blk_first_blk_Id")
            else:
                first_block_id = -1

            # print(name_id, param_count, block_count, first_block_id, self.data._ptr, self.block_id_to_name(name_id))
            # print(self.block_id_to_name(name_id), name_id)
            blocks.append(Block(self.block_id_to_name(name_id), param_count, block_count, first_block_id))

        # if current_t > 0:
        #     print(f"After block creation and final file read: {time.perf_counter() - current_t}")

        result_ptr = 0
        for block in blocks:  # this grabs all the values and puts them in their correct blocks
            field_count = block.param_count
            for i in range(field_count):
                block.add_field(chunks[result_ptr + i])
            result_ptr += field_count

        # if current_t > 0:
        #     print(f"After block param matching: {time.perf_counter() - current_t}")

        self.parent = blocks[0]
        self.from_blocks_with_parent(self.parent, blocks)

        # if current_t > 0:
        #     print(f"After block hierarchy creation: {time.perf_counter() - current_t}")

    def to_dict(self):
        return self.parent.to_dict()

    def block_id_to_name(self, block_id):
        if block_id == 0:
            return "root"
        else:
            return self.names[block_id - 1]

    def from_blocks_with_parent(self, parent, blocks):
        for i in range(parent.blocks_count):
            parent.children.append(blocks[i + parent.first_block_id])
            self.from_blocks_with_parent(blocks[i + parent.first_block_id], blocks)


class BlkBytes:
    """
    # A class that acts like BLkDecoder without all the parsing, simply used to get all the bytes from a BLK
    """

    def __init__(self, dat, offset=0, name_map: list[bytearray] = None, zstd_dict=None):
        self.bytes = bytearray()
        if type(dat) is not BitStream:
            dat = BitStream(dat)

        start_index = dat.GetReadOffset()
        dat.advance(offset * 8)
        self.data = None
        x = dat.ReadBits(8, "blk_type")
        self.blkType = FileType(x[0])  # gets blk type, the first byte
        self.bytes.extend(x)
        if self.blkType == FileType.BBF:
            raise Exception("BLK is invalid type BBF")
        if not self.blkType.is_zstd():
            self.data = dat
        else:
            if self.blkType.needs_dict():
                if zstd_dict is None:
                    raise Exception("zstd dict is required")
            x = zstd.ZstdDecompressor(zstd_dict).stream_reader(dat)
            self.data = BitStream(x.read())
            x.close()
        self.names_in_name_map, temp = self.data.decode_uleb128_bytes()  # gets the number of names in the name map
        self.bytes += temp
        # self.names = None
        if self.blkType.is_slim():
            if name_map is None:
                print("BAD NAME MAP")
        else:
            self.name_map_size, temp = self.data.decode_uleb128_bytes()  # gets the size of the name map
            self.bytes += temp

            # self.names = [x.decode("utf-8") for x in self.data.fetch(self.name_map_size - 1).split(b"\x00")]
            self.bytes += self.data.ReadBits(self.name_map_size * 8)
            # print(self.names)
            # self.data.advance(1)
            # if len(self.names) != self.names_in_name_map:
            #     print("RED ALERT")

        self.num_of_blocks, temp = self.data.decode_uleb128_bytes()
        self.bytes += temp
        self.num_of_params, temp = self.data.decode_uleb128_bytes()
        self.bytes += temp
        self.params_data_size, temp = self.data.decode_uleb128_bytes()
        self.bytes += temp
        # self.params_data = self.data.fetch(self.params_data_size)  # used later on, data
        self.bytes += self.data.ReadBits(self.params_data_size * 8)
        '''
        here we are are skipping results creation and starting with chunks
        assume we are doing let chunks
        '''
        # chunks = []
        # parser = ChunkParser(self.names, BLKTypes(self.names, self.params_data))
        # for i in range(self.num_of_params):
        #     chunks.append(parser.parse(self.data.fetch(8)))
        self.bytes += self.data.ReadBits(self.num_of_params * 8 * 8)
        # chunks = Chunks(self.data, self.num_of_params, self.names, B)
        # blocks = []
        for i in range(self.num_of_blocks):  # this creates all the blocks
            name_id, temp = self.data.decode_uleb128_bytes()
            self.bytes += temp
            param_count, temp = self.data.decode_uleb128_bytes()
            self.bytes += temp
            block_count, temp = self.data.decode_uleb128_bytes()
            self.bytes += temp
            if block_count > 0:
                first_block_id, temp = self.data.decode_uleb128_bytes()
                self.bytes += temp
        #     else:
        #         first_block_id = -1
        # print(self.block_id_to_name(name_id), name_id)
        #     blocks.append(Block(self.block_id_to_name(name_id), param_count, block_count, first_block_id))

        # if current_t > 0:
        #     print(f"After block creation and final file read: {time.perf_counter() - current_t}")
        '''
        result_ptr = 0
        for block in blocks:  # this grabs all the values and puts them in their correct blocks
            field_count = block.param_count
            for i in range(field_count):
                block.add_field(chunks[result_ptr + i])
            result_ptr += field_count

        # if current_t > 0:
        #     print(f"After block param matching: {time.perf_counter() - current_t}")

        self.parent = blocks[0]
        self.from_blocks_with_parent(self.parent, blocks)

        '''  # if current_t > 0:
        #     print(f"After block hierarchy creation: {time.perf_counter() - current_t}")