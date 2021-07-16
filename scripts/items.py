# Combine assets/img/gallery/descriptions.txt with the images in thumb/large
# with their sizes and create nanogallery items
# Relies on the wand imagemagick library

# cd assets/img/gallery
# python3 items.py descriptions.txt 
import wand
from wand.image import Image
import fileinput
import textwrap
import re
unputline = None
def getline(f):
    global unputline
    ret = None # return value
    if unputline:
        ret=unputline
    else:
        ret = f.readline()
    unputline = None
    return ret

def unget(line):
    global unputline
    unputline = line

with fileinput.input() as f:
    while (line := getline(f)):
        if re.match("^\s*$", line):
            continue
        # filename: [tags]
        i = line.find(':')
        assert i != -1, line
        filename = line[:i].strip()
        tags = line[i+1:].split()
        tags = '"' + " ".join(tags) + '"'

        tw = th = lw = lh = 0
        # accumulate multiline description until next filename
        desc = ""
        firstLine = True
        while dline := getline(f):
            if not re.match("^\s*$", dline):
                dline = dline.strip()
                if firstLine:
                    firstLine = False
                else:
                    desc += "\n"
                desc += dline
            else:
                break
        
        with Image(filename=f"thumb/{filename}") as img:
            (tw, th) = img.size
        assert tw > 0 and th > 0, f"Image doesn't exist: thumb/{filename}"
        with Image(filename=f"large/{filename}") as img:
            (lw, lh) = img.size
        assert lw > 0 and lh > 0, f"Image doesn't exist: large/{filename}"
        print(f"""
            {{  
            src: "large/{filename}", 
            srct: "thumb/{filename}", 
            title: `{desc}`, 
            height: {lw}, width: {lh}, 
            imgtWidth: {tw}, imgtHeight: {th},
            }},""")
    
