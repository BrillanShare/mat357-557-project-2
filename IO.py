from PIL import Image


# white pixels mark the region, black pixels are everywhere else
def getbit(pix,x,y):
    try:
        return pix[x,y][0] > 0
    except IndexError:
        return False;
        
# returns a bitstream of the border, the total length in steps, the size of the image, and the start position
def get_border(file_name):

    img = Image.open(file_name)
    pix = img.load()
    
    X, Y = img.size
    start_x, start_y = -1, -1
    
    # look for the leftmost point to start with
    for x in range(X):
        for y in range(Y):
            b = getbit(pix,x,y)
            if b:
                start_x, start_y = x, y
                break
        if start_x != -1:
            break
                
    # bitstream of border codes
    border = 0b0
    
    # current location
    path_x, path_y = start_x, start_y
    
    # next direct (in binary code)
    next_dir = -1
    
    #total length in steps
    length = 0
        
    while True:
        # if this is triggered, the loop is complete
        if path_x == start_x and path_y == start_y and next_dir == 0b11:
            return border, length, (X,Y), (start_x, start_y)
        
        # start by (trying to) move down
        if next_dir == -1:
            next_dir = 0b11
        
        next_y = path_y
        next_x = path_x
        
        # follow next_dir
        if not next_dir & 1:
            next_x -= 1 if next_dir >> 1 else -1
        else:
            next_y += 1 if next_dir >> 1 else -1
        
        # can we move this way?
        if getbit(pix, next_x, next_y):
            path_x, path_y = next_x, next_y
            
            border = (border << 2) + next_dir
            length += 1
            
            #turn right, if we can
            next_dir = (next_dir - 0b01) % 0b100
        else:
            #turn left, if we must 
            next_dir += 1
            next_dir = next_dir % 0b100
         
         
def write_border(file_name, border_bin, length, size, start_pos):
    
    img = Image.new("RGB", size)
    pix = img.load()
    
    mark_color = (255, 255, 255, 255)
    
    (x,y) = start_pos
    pix[x,y] = mark_color
    
    for i in range(2*length-2, -2, -2):
        
        step = border_bin >> i & 0b11
        
        if step == 0b00:
            x += 1
        elif step == 0b01:
            y -= 1
        elif step == 0b10:
            x -= 1
        elif step == 0b11:
            y += 1
                        
        try:
            pix[x,y] = mark_color
        except IndexError:
            pass
    
    img.save(file_name)
    
