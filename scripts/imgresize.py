#!/usr/local/bin/python3
# usage: imgfit max-width max-heght infile outfile
#   Fir=ts
# import wand
from wand.image import Image
import sys
import argparse

parser = argparse.ArgumentParser("Resize image down (using imagemagick) to fit a maxw x maxh cell")
parser.add_argument("-v", "--verbose", help="print original and  resized image dimensions", action="store_true")
parser.add_argument("maxwidth",  metavar='maxw', type=int, help="maximum width")
parser.add_argument("maxheight",  metavar='maxh', type=int, help="maximum height")
parser.add_argument("infile",  metavar='infile', type=str, help="input image file")
parser.add_argument("outfile",  metavar='outfile', type=str, help="outfile image file")

args = parser.parse_args()

if args.infile == args.outfile:
    print ("infile and outfile cannot be the same file")
    sys.exit(1)

with Image(filename=args.infile) as img:
    (w, h) = img.size
    w_by_h = w / h #aspect ratio. This needs to be preserved.

    with img.clone() as imgcopy:
        # If width exceeds max-width, and is constrained to max-width,
        # compute corresponding height. 
        if w > args.maxwidth:
            newh = int(args.maxwidth / w_by_h)
            if newh > args.maxheight:
                # If height exceeds max-height then height is the more limiting dimension.
                imgcopy.resize(int(args.maxheight * w_by_h), args.maxheight)
            else:
                imgcopy.resize(args.maxwidth, newh)
        elif h > args.maxheight:
            # constrain to max-height, calculate corresponding width
            neww = int(args.maxheight * w_by_h)
            if neww > args.maxwidth:
                # width is the more constraining factor
                imgcopy.resize(args.maxwidth, int(args.maxwidth / w_by_h))
            else:
                imgcopy.resize(neww, args.maxheight)
        else:
            pass # No resizing, but we will output it anyway
        (ow,oh) = imgcopy.size
        if args.verbose:
            print(f"Saving {args.infile} ({w}x{h}) => {args.outfile} ({ow}x{oh})")
        imgcopy.save(filename=args.outfile)

    


