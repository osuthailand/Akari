from typing import Any
from enum import unique, IntEnum
import struct

@unique
class Types(IntEnum):
    # Only using these currently. I will add more, if I find use of them.
    int32 = 5
    string = 29

class Writer:
    def write_uleb128(self, value: int) -> bytearray:
        if value == 0:
            return bytearray(b"\x00")

        data: bytearray = bytearray()
        length: int = 0

        while value > 0:
            data.append(value & 0x7F)
            value >>= 7
            if value != 0:
                data[length] |= 0x80

            length += 1

        return data

    def write_int32(self, value: int) -> bytearray:
        return bytearray(value.to_bytes(Types.int32, "little"))

    def write_str(self, string: str) -> bytearray:
        if not string:
            return bytearray(struct.pack("\x00"))
        
        data = bytearray(struct.pack("\x0B"))
        
        data += self.write_uleb128(len(string.encode()))
        data += string.encode()  
        return data 

    def write(self, pID: int, *args: tuple[Any, ...]) -> bytes:
        data = bytearray(struct.pack("<Hx", pID))

        for args, d_type in args:
            if d_type == Types.int32:
                data += self.write_int32(args)
            elif d_type == Types.string:
                data += self.write_str(args)
        
        data[3:3] += struct.pack("<I", len(data) - 3)
        return bytes(data)