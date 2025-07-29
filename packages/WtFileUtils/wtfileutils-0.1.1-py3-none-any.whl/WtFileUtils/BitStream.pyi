class BitStream:
    def __init__(self, data: bytes, save_path: str = "", immediate_print: bool = False, do_save: bool = False):
        self.ws = None


    def Flush(self) -> None:
        pass

    def ReadU8(self, message: str = "") -> int:
        pass

    def ReadU16(self, message: str = "") -> int:
        pass

    def ReadU32(self, message: str = "") -> int:
        pass

    def ReadU64(self, message: str = "") -> int:
        pass

    def ReadUleb(self, message: str = "") -> int:
        pass

    def ReadFloat(self, message: str = "") -> float:
        pass

    def ReadBool(self, message: str = "") -> bool:
        pass

    def ReadCStr(self, message: str = "") -> str:
        pass

    def ReadPascalStr(self, message: str = "") -> str:
        pass

    def ReadBytes(self, bytes: int, message: str = "") -> bytes:
        pass

    def ReadBits(self, bits: int, message: str = "") -> bytes:
        pass

    def ReadBitsInt(self, bits: int, message: str = "") -> int:
        pass

    def ReadRemaining(self, message: str = "") -> bytes:
        pass

    def RemainingBits(self) -> int:
        pass

    def GetReadOffset(self) -> int:
        pass

    def SetReadOffset(self, offset: int) -> None:
        pass

    def GetWriteOffset(self) -> int:
        pass

    def SetWriteOffset(self, offset: int) -> None:
        pass

    def GetData(self) -> bytes:
        pass

    def IgnoreBits(self, bits: int) -> None:
        pass

    def IgnoreBytes(self, bytes: int) -> None:
        pass

    def ReserveBits(self, bits: int) -> None:
        pass

    def read(self, size: int = -1):
        pass

    def WriteBits(self, data: bytes, bits: int) -> None:
        pass

    def WriteBytes(self, data: bytes, bytes: int) -> None:
        pass

    def WriteU8(self, data: int) -> None:
        pass

    def WriteU16(self, data: int) -> None:
        pass

    def WriteU32(self, data: int) -> None:
        pass

    def WriteU64(self, data: int) -> None:
        pass

    def WriteUleb(self, data: int) -> None:
        pass

    def WriteFloat(self, data: float) -> None:
        pass

    def WriteBool(self, data: bool) -> None:
        pass

    def WriteCStr(self, data: bytes) -> None:
        pass

    def WritePStr(self, data: bytes) -> None:
        pass

    def WriteBitsInt(self, data: int, bits: int) -> None:
        pass
