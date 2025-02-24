from IO import get_border, write_border
from border import encode, decode


file_name = 'demos/tree'
border_bin, total_length, size, start_pos = get_border(file_name+'.png')

for level in range(5):
    transmission = encode(border_bin, total_length, level)
    compressed_border_bin, this_length = decode(transmission)
    
    write_border(file_name+' - compression '+str(level)+'.png', \
                 compressed_border_bin, this_length, size, start_pos)