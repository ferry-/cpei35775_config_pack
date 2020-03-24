#! python3

import sys
import zlib

END = "little"
MAGIC = b"LMMC\x00\x03\x00\x00"
LZ = b"\x78\x9c"
ADLER=0x1b2c3ec6

def pack(dec, f):
    comp = zlib.compress(dec)
    chk_sum = zlib.adler32(comp, 0x1b2c3ec6)
    raw_len = len(dec)
    comp_len = len(comp)

    assert comp[:2] == LZ

    f.write(MAGIC)
    f.write(int.to_bytes(comp_len, length=4, byteorder=END))
    f.write(int.to_bytes(chk_sum, length=4, byteorder=END))
    f.write(int.to_bytes(raw_len, length=4, byteorder=END))
    f.write(comp)

def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python3 %s <config_in.xml> [config_out.bin]" % sys.argv[0])
        sys.exit()
    else:
        fin = open(sys.argv[1], "rb")
        dec = fin.read()
        fin.close()

        if len(sys.argv) == 3:
            fout = open(sys.argv[2], "wb")
        else:
            fout = sys.stdout.buffer

        pack(dec, fout)

main()
