###########################################################################
#   scr2ppm.py                                                            #
#                                                                         #
#   Converts .scr graphic files (standard ZX Spectrum computer screen)    #
#   to simple .ppm format that does not provide any sort of compression.  #
#                                                                         #
#   Programmed by that1357 at 09-15-2024.                                 #                                                                       #
###########################################################################

def to_rgb(a):
    if a == 0 or a == 64:   # Black color
        return '0 0 0'
    elif a == 1:            # Blue color
        return '0 34 199'
    elif a == 65:           # Bright blue color
        return '0 43 251'
    elif a == 2:            # Red color
        return '214 40 22'
    elif a == 66:           # Bright red color
        return '255 51 28'
    elif a == 3:            # Magenta color
        return '212 51 199'
    elif a == 67:           # Bright magenta color
        return '255 64 252'
    elif a == 4:            # Green color
        return '0 197 37'
    elif a == 68:           # Bright green color
        return '0 249 47'
    elif a == 5:            # Cyan color
        return '0 199 201'
    elif a == 69:           # Bright cyan color
        return '0 251 254'
    elif a == 6:            # Yellow color
        return '204 200 42'
    elif a == 70:           # Bright yellow color
        return '255 252 54'
    elif a == 7:            # White color
        return '202 202 202'
    elif a == 71:           # Bright white color
        return '255 255 255'
    else:
        return 'ERROR!'

import sys

# Open .scr file
in_filename = sys.argv[1]

try:
    with open(in_filename, 'rb') as scr_file:
        content = scr_file.read()
except OSError:
    print('Could not open file:', in_filename)
    sys.exit()

# Stores strings, which are binary representations of each byte of data
data = []
base = 0
# For each screen segment (1/3 part of screen)
for i in range(3):
    index = base
    # Repeat 8 times
    for j in range(8):
        # For each of the 8 lines in segment
        for k in range(8):
            for byte_index in range(index, index + 32):
                hex_val = hex(content[byte_index])
                bin_str = bin(int(hex_val, base = 16))[2:].zfill(8)
                data.append(bin_str)
            index = index + 256
        index = index - 64 * 32 + 32
    base = base + 2048

# Attrs array contains two-element tuples (ink, paper) for each attr byte
attrs = []
for i in range(6144, 6912):
    attr_val = content[i]
    ink = to_rgb(attr_val & 0b01000111)
    paper = to_rgb(((attr_val & 0b00111000) >> 3) | 0b01000000)
    attrs.append((ink, paper))

if in_filename.endswith('.scr'):
    out_filename = in_filename[:-3] + 'ppm'
else:
    out_filename = in_filename + '.ppm'

with open(out_filename, 'w') as out_file:
    # Write PPM header to file
    out_file.write('P3\n')
    out_file.write('256 192\n')
    out_file.write('255\n')
    
    # Write RGB data to file
    data_index = 0
    attr_index = 0
    
    # For each line in attrs
    for i in range(24):
        # 8 repeats per line in attrs
        for j in range(8):
            # For each character place
            for k in range(32):
                for bit in data[data_index]:
                    if bit == '0':
                        out_file.write(attrs[attr_index][1] + '\n')
                    else:
                        out_file.write(attrs[attr_index][0] + '\n')
                data_index += 1
                attr_index += 1
            attr_index -= 32
        attr_index += 32
