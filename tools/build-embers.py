"""Create a seamless animated GIF from an oven photo, using only Python stdlib.

Input: a 24-bit BMP (640px wide) exported with System.Drawing.
"""
import math
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'assets/oven-source.bmp').read_bytes()
offset = struct.unpack_from('<I', source, 10)[0]
width, height = struct.unpack_from('<ii', source, 18)
assert width > 0 and height > 0 and struct.unpack_from('<H', source, 28)[0] == 24
stride = (width * 3 + 3) & ~3
rows = [source[offset + (height - 1 - y) * stride:offset + (height - 1 - y) * stride + width * 3] for y in range(height)]

def compress(pixels):
    # Keep the dictionary below the 10-bit transition for a simple portable encoder.
    codes = [256]
    table = {}
    next_code = 258
    current = pixels[0]
    for value in pixels[1:]:
        key = (current, value)
        found = table.get(key)
        if found is not None:
            current = found
        else:
            codes.append(current)
            table[key] = next_code
            next_code += 1
            current = value
            if next_code == 511:
                codes.append(256)
                table.clear()
                next_code = 258
    codes.extend((current, 257))
    packed = bytearray()
    buffer = bits = 0
    for code in codes:
        buffer |= code << bits
        bits += 9
        while bits >= 8:
            packed.append(buffer & 255)
            buffer >>= 8
            bits -= 8
    if bits:
        packed.append(buffer & 255)
    return b''.join(bytes([len(packed[i:i+255])]) + packed[i:i+255] for i in range(0, len(packed), 255)) + b'\0'

palette = bytearray()
for i in range(256):
    palette.extend((round(((i >> 5) & 7) * 255 / 7), round(((i >> 2) & 7) * 255 / 7), (i & 3) * 85))
output = bytearray(b'GIF89a' + struct.pack('<HHBBB', width, height, 247, 0, 0) + palette)
output.extend(b'!\xff\x0bNETSCAPE2.0\x03\x01\x00\x00\x00')
frames = 48
for frame in range(frames):
    phase = 2 * math.pi * frame / frames
    pixels = bytearray()
    for y in range(height):
        # Periodic heat shimmer, anchored to the original photograph.
        shift = round(1.7 * math.sin(y * .043 + phase * 2) * (1 - y / height))
        row = rows[y]
        for x in range(width):
            sx = max(0, min(width - 1, x + shift)) * 3
            b, g, r = row[sx:sx+3]
            ember = max(0, (r - g) / 255) * (r / 255)
            pulse = math.sin(phase * 2 + x * .028 + y * .021) + .4 * math.sin(phase * 3 - x * .017)
            rr = max(0, min(255, int(r + 27 * ember * pulse)))
            gg = max(0, min(255, int(g + 19 * ember * pulse)))
            # Ordered dithering preserves charcoal texture with a small palette.
            dither = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))[y % 4][x % 4] - 7.5
            rq = max(0, min(7, round((rr + dither * 1.7) * 7 / 255)))
            gq = max(0, min(7, round((gg + dither * 1.7) * 7 / 255)))
            bq = max(0, min(3, round((b + dither * 3) * 3 / 255)))
            pixels.append((rq << 5) | (gq << 2) | bq)
    output.extend(b'!\xf9\x04\x04\x08\x00\x00\x00')
    output.extend(b',' + struct.pack('<HHHHB', 0, 0, width, height, 0))
    output.append(8)
    output.extend(compress(pixels))
output.append(59)
target = ROOT / 'assets/oven-embers.gif'
target.write_bytes(output)
print(f'{target}: {len(output):,} bytes; {frames} frames; {frames * .08:.2f}s seamless loop')
