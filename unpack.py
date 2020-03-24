#! python3

import sys
import zlib

END = "little"
MAGIC = b"LMMC\x00\x03\x00\x00"
LZ = b"\x78\x9c"
ADLER = 0x1b2c3ec6

def checksum(data, WS=4):
    acc = 0
    MA = (1 << (WS*8))-1
    for i in range(0, len(data), WS):
        w = int.from_bytes(data[i:i+WS], byteorder=END)
        acc = (acc + w) & MA
    acc = ((acc ^ MA) + 1) & MA
    return acc

def unpack(cont, fout, quiet=False):
    assert cont[:len(MAGIC)] == MAGIC
    comp_len = int.from_bytes(cont[8:12], byteorder=END)
    head_chk = int.from_bytes(cont[12:16], byteorder=END)
    raw_len = int.from_bytes(cont[16:20], byteorder=END)
    comp = cont[20:]
    
    chk = zlib.adler32(comp, ADLER)

    if not quiet:
        print("magic good, header claims size compressed=%d, size raw=%d, checksum: 0x%0x" % (comp_len, raw_len, head_chk), file=sys.stderr)
        print("actual adler33 checksum: 0x%0x" % chk, file=sys.stderr)

    assert len(comp) == comp_len, "compressed length doesn't match"
    assert head_chk == chk, "compressed checksum doesn't match"
    assert comp[:2] == LZ, "payload doesn't start with LZ header"

    dec = zlib.decompress(comp)
    assert len(dec) == raw_len, "decompressed length wrong"

    bytes_out = fout.write(dec)
    if not quiet:
        print("success; wrote %d bytes" % bytes_out, file=sys.stderr)

def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python3 %s <config_in.bin> [config_out.xml]" % sys.argv[0])
        sys.exit()
    else:
        fin = open(sys.argv[1], "rb")
        cont = fin.read()
        fin.close()

        if len(sys.argv) == 3:
            fout = open(sys.argv[2], "wb")
        else:
            fout = sys.stdout.buffer

        unpack(cont, fout)

main()
