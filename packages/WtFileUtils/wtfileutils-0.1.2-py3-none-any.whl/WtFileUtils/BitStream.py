import struct

try:
    import sys
    # raise ImportError
    sys.path.append(r"D:\cpp\PersonBLK\cmake-build-debug\cPython")
    from BitStream import BitStream
except ImportError:
    import io
    import copy
    import math
    import abc


    class __WriteStream:
        def __init__(self, add_newline: bool, immediate: bool):
            self.add_newline = add_newline
            self.immediate = immediate
            self.string = ""
            self.flush_ptr = 0

        @abc.abstractmethod
        def print(self, str_: str):
            pass

        def write(self, str_: str):
            self.string += str_
            if self.add_newline:
                self.string += "\n"
            if self.immediate:
                print(str_)

        def flush(self):
            if not self.immediate:
                self.print("#pragma pattern_limit 10000000\nstruct data {")
                data = self.string[self.flush_ptr:]
                self.flush_ptr = len(self.string)
                self.print(data)
                self.print("};\ndata d @ 0;")


    class _PrintStream(__WriteStream):
        def __init__(self, add_newline: bool, immediate: bool):
            super().__init__(add_newline, immediate)

        def print(self, str_: str):
            if self.add_newline:
                print(str_, end="\n")
            else:
                print(str_, end="")


    class _FileStream(__WriteStream):
        def __init__(self, path: str, add_newline: bool, immediate: bool):
            super().__init__(add_newline, immediate)
            self.path = path
            with open(path, "w") as f:
                pass

        def print(self, str_: str):
            with open(self.path, "a") as f:
                f.write(str_)
                if self.add_newline:
                    f.write("\n")


    class _GaijinStream:
        def __init__(self, data):
            self.__data = bytearray(data)  # easier for writing
            self.__bitsAllocated = self.bytes2bits(len(data))
            self.__bitsUsed = self.__bitsAllocated  # also write offset
            self.__readOffset = 0

        def Reset(self):
            self.__bitsUsed = self.__readOffset = 0

        def GetNumberOfBitsUsed(self):
            return self.__bitsUsed

        def GetWriteOffset(self):
            return self.__bitsUsed

        def GetNumberOfBytesUsed(self):
            return self.bits2bytes(self.__bitsUsed)

        def GetReadOffset(self):
            return self.__readOffset

        def SetReadOffset(self, newReadOffset: int):
            self.__readOffset = newReadOffset

        def GetNumberOfUnreadBits(self):
            return self.__bitsUsed - self.__readOffset

        def GetData(self):
            return self.__data

        def GetDataOffset(self):
            return self.__data[self.bits2bytes(self.__readOffset)]

        def IgnoreBits(self, bits: int):
            self.__readOffset += min(bits, self.__bitsUsed - self.__readOffset)

        def IgnoreBytes(self, bytes_: int):
            self.IgnoreBits(self.bytes2bits(bytes_))

        def SetWriteOffset(self, offs: int):
            self.__bitsUsed = offs

        def AlignWriteToByteBoundary(self):
            if self.__bitsUsed:
                self.__bitsUsed += 8 - (((self.__bitsUsed - 1) & 7) + 1)

        def AlignReadToByteBoundary(self):
            if self.__readOffset:
                self.__readOffset += 8 - (((self.__readOffset - 1) & 7) + 1)

        def ResetWritePointer(self):
            self.__bitsUsed = 0

        def ResetReadPointer(self):
            self.__readOffset = 0

        def ReadBits(self, bits) -> bytes | None:
            if bits == 0:
                return b""
            if self.__readOffset + bits > self.__bitsAllocated:
                return None

            dataPtr = 0
            readMod8 = self.__readOffset & 7
            if readMod8 == 0 and (bits & 7) == 0:  # everything byte aligned
                r_off = self.bits2bytes(self.__readOffset)
                temp = self.__data[dataPtr+r_off:dataPtr+r_off + self.bits2bytes(bits)]
                self.__readOffset += bits
                return bytes(temp)

            output = bytearray(self.bits2bytes(bits))

            offs = 0
            while bits > 0:
                output[offs] |= (self.__data[dataPtr + (self.__readOffset >> 3)] << readMod8) & 0xFF
                if readMod8 > 0 and bits > (8 - readMod8):
                    output[offs] |= self.__data[dataPtr + (self.__readOffset >> 3) + 1] >> (8 - readMod8)

                if bits >= 8:
                    bits -= 8
                    self.__readOffset += 8
                    offs += 1
                else:
                    output[offs] >>= 8 - bits
                    self.__readOffset += bits
                    break

            return bytes(output)

        def WriteBits(self, input_: bytes, bits: int) -> None:
            if input_ == b"" or bits == 0:
                return

            self.reserveBits(bits)
            bitsUsedMod8 = self.__bitsUsed & 7
            bitsMod8 = bits & 7
            srcPtr = 0
            destPtr = self.__bitsUsed >> 3
            if bitsUsedMod8 == 0 and bitsMod8 == 0:
                for i in range(len(input_)):
                    self.__data[i + self.__bitsUsed] = input_[i]
                self.__bitsUsed += bits
                return

            upShift = 8 - bitsUsedMod8  # also how many remaining free bits in byte left
            destByte = self.__data[destPtr] & (0xff << upShift)  # clear low bits
            self.__bitsUsed += bits
            srcByte = 0

            while bits >= 8:
                srcByte = input_[srcPtr]
                srcPtr += 1
                self.__data[destPtr] = destByte | (srcByte >> bitsUsedMod8)
                destPtr += 1
                destByte = (srcByte << upShift) & 0xFF

                bits -= 8

            if bits == 0:
                self.__data[destPtr] = destByte | (self.__data[destPtr] & (0xff >> bitsUsedMod8))
                return

            srcByte = input_[srcPtr] & ((1 << bits) - 1)

            bitsDiff = bits - upShift
            if bitsDiff <= 0:  # enough space left in byte to fit remaining bits
                self.__data[destPtr] = destByte | (
                        (self.__data[destPtr] & (0xff >> (bits + bitsUsedMod8))) | (srcByte << -bitsDiff))
                return

            self.__data[destPtr] = destByte | (srcByte >> bitsDiff)
            destPtr += 1
            self.__data[destPtr] = (self.__data[destPtr] & (0xff >> bits)) | (
                    (srcByte & ((1 << bits) - 1)) << (8 - bits))

        def Write(self, input_: bytes, lenInBytes: int) -> None:
            self.WriteBits(input_, self.bytes2bits(lenInBytes))

        def Read(self, lenInBytes: int):
            out = self.ReadBits(self.bytes2bits(lenInBytes))
            return out

        def WriteCompressed(self, v: int):
            while True:
                byte_ = (v & 0xFF) | (1 << 7 if v >= (1 << 7) else 0)
                self.Write(bytes([byte_]), 1)
                v >>= 7
                if v <= 0:
                    break

        def ReadCompressed(self) -> int | None:
            v = 0
            count = 0
            while True:
                byte_ = self.Read(1)
                if byte_ is None:
                    return None
                byte_ = byte_[0]
                v |= (byte_ & ~(1 << 7)) << (count * 7)
                count += 1
                if (byte_ & (1 << 7)) == 0:
                    break
            return v

        def writeString(self, t: bytes):
            self.WriteCompressed(len(t))
            if len(t) > 0:
                self.Write(t, len(t))

        def readString(self):
            len_ = self.ReadCompressed()
            if len_ is None:
                return None
            chars = self.Read(len_)
            if chars is None:
                return None
            return chars

        def reserveBits(self, bits):
            if bits == 0:
                return
            bytes_needed = self.bits2bytes(self.__bitsUsed + bits) - self.bits2bytes(self.__bitsAllocated)
            self.__data.extend([0] * bytes_needed)
            self.__bitsAllocated += bits

        @staticmethod
        def bytes2bits(by):
            return by << 3

        @staticmethod
        def bits2bytes(by):
            return (by + 7) >> 3


    class BitStream:
        def __init__(self, data: bytes, save_path: str = "", immediate_print=False, do_save=False):
            self.bs: _GaijinStream = _GaijinStream(data)
            self.do_save = do_save
            if save_path != "":
                self.ws = _FileStream(save_path, True, immediate_print)
            else:
                self.ws = _PrintStream(True, immediate_print)
            self.__count = 0

        def __write_message(self, message: str, type_: str, bitcount: int, start_bits: int):
            if self.do_save:
                start_index = start_bits >> 3
                end_index = (start_bits + bitcount + 7) >> 3
                self.ws.write(
                    f"    u8 _{message}_{type_}_{self.__count}_{start_bits}[{end_index - start_index}] @ {start_index};")
                self.__count += 1

        def Flush(self):
            self.ws.flush()

        def readU8(self, message=""):
            self.__write_message(message, "u8", 8, self.bs.GetReadOffset())
            bytes_ = self.bs.Read(1)
            if bytes_ is None:
                return None
            return bytes_[0]

        def ReadU16(self, message=""):
            self.__write_message(message, "u16", 16, self.bs.GetReadOffset())
            bytes_ = self.bs.Read(2)
            if bytes_ is None:
                return None
            return struct.unpack("<H", bytes_)[0]

        def ReadU32(self, message=""):
            self.__write_message(message, "u32", 32, self.bs.GetReadOffset())
            bytes_ = self.bs.Read(4)
            if bytes_ is None:
                return None
            return struct.unpack("<I", bytes_)[0]

        def ReadU64(self, message=""):
            self.__write_message(message, "u64", 64, self.bs.GetReadOffset())
            bytes_ = self.bs.Read(8)
            if bytes_ is None:
                return None
            return struct.unpack("<Q", bytes_)[0]

        def ReadUleb(self, message=""):
            start = self.bs.GetReadOffset()
            val = self.bs.ReadCompressed()
            if val is None:
                return None
            self.__write_message(message, "u8", self.bs.GetReadOffset() - start, start)
            return val

        def ReadFloat(self, message=""):
            self.__write_message(message, "float", 32, self.bs.GetReadOffset())
            val = self.bs.Read(4)
            if val is None:
                return None
            return struct.unpack("<f", val)[0]

        def ReadBool(self, message=""):

            self.__write_message(message, "bool", 1, self.bs.GetReadOffset())
            val = self.bs.ReadBits(1)
            if val is None:
                return None
            return val[0] == 1

        def ReadCStr(self, message=""):
            start_index = self.bs.GetReadOffset()
            out = bytearray()
            char = self.bs.Read(1)
            if char is None:
                return None
            char = char[0]
            while char != 0:
                out.append(char)
                char = self.bs.Read(1)
                if char is None:
                    return None

            self.__write_message(message, "cStr", self.bs.GetReadOffset() - start_index, start_index)
            return bytes(out)

        def ReadPascalStr(self, message=""):
            start_index = self.bs.GetReadOffset()
            p_str = self.bs.readString()
            self.__write_message(message, "pascalStr", self.bs.GetReadOffset() - start_index, start_index)
            return p_str

        def ReadBytes(self, bytes_: int, message=""):
            self.__write_message(message, "bytes", bytes_ << 8, self.bs.GetReadOffset())

            return self.bs.Read(bytes_)

        def ReadBits(self, bits: int, message=""):
            self.__write_message(message, "bits", bits, self.bs.GetReadOffset())
            return self.bs.ReadBits(bits)

        def ReadBitsInt(self, bits: int, message=""):

            self.__write_message(message, "bitsInt", bits, self.bs.GetReadOffset())
            p = self.ReadBits(bits)
            if p is None:
                return None
            return int.from_bytes(p, "little")

        def ReadRemaining(self, message=""):
            readCount = self.bs.GetNumberOfUnreadBits()
            self.__write_message(message, "Remaining", readCount, self.bs.GetReadOffset())
            return self.bs.ReadBits(readCount)

        def RemainingBits(self):
            return self.bs.GetNumberOfUnreadBits()

        def GetReadOffset(self):
            return self.bs.GetReadOffset()

        def SetReadOffset(self, offset: int):
            self.bs.SetReadOffset(offset)

        def GetWriteOffset(self):
            return self.bs.GetWriteOffset()

        def SetWriteOffset(self, offset: int):
            self.bs.SetWriteOffset(offset)

        def GetData(self):
            return self.bs.GetData()

        def IgnoreBits(self, bits: int):
            return self.bs.IgnoreBits(bits)

        def IgnoreBytes(self, bytes_: int):
            return self.bs.IgnoreBytes(bytes_)

        def ReserveBits(self, bits: int):
            self.bs.reserveBits(bits)

        def read(self, size: int = -1):
            # print(size)
            if size == -1:
                return self.ReadRemaining("read_readRemaining")
            payload = self.ReadBytes(size, "read_read")
            if payload is None:
                out = self.ReadRemaining("read_read_failed")
                return out
            return payload

        def WriteBits(self, data, bits):
            self.bs.WriteBits(data, bits)

        def WriteBytes(self, data, bytes_):
            self.bs.Write(data, bytes_)

        def WriteU8(self, data: int):
            self.bs.Write(data.to_bytes(1, byteorder="little"), 1)

        def WriteU16(self, data: int):
            self.bs.Write(data.to_bytes(2, byteorder="little"), 2)

        def WriteU32(self, data: int):
            self.bs.Write(data.to_bytes(4, byteorder="little"), 4)

        def WriteU64(self, data: int):
            self.bs.Write(data.to_bytes(8, byteorder="little"), 8)

        def WriteUleb(self, data: int):
            self.bs.WriteCompressed(data)

        def WriteFloat(self, data: float):
            self.bs.Write(struct.pack("<f", data), 4)

        def WriteBool(self, data: bool):
            self.bs.Write(bytes([int(data)]), 1)

        def WriteCStr(self, data: bytes):

            self.bs.Write(data, len(data))
            if not data.endswith(b"\x00"):
                self.bs.Write(b"\x00", 1)

        def WritePStr(self, data: bytes):
            self.bs.writeString(data)

        def WriteBitsInt(self, data: int, bits: int):
            byte_size = self.bs.bits2bytes(bits)
            self.bs.WriteBits((data & ((1 << byte_size) - 1)).to_bytes(byte_size, byteorder="little"), bits)

