# This is a mosaic generator for nanogallery. 
# Draw a table on https://www.tablesgenerator.com/text_tables, 
# Using cell->merge judiciously, then copy to a text file.
# This script coverts the text representation to a nanogallery
# mosaic description 
# table-to-mosaic.pl <text file> 

import fileinput

# split a string into an array of chars
def split(str):
    return [char for char in str]

# Create a 2D array of chars
lines = [split(line.strip()) for line in fileinput.input()]

numlines = len(lines)
linesize = len(lines[0])
for i in range(0, numlines-1):
    for j in range(0, linesize-1):
        # if the current char is a top-left corner
        if lines[i][j] == '+' and lines[i+1][j] == '|' and lines[i][j+1] == '-':
                #
                # Go south until we see a SW corner (starting with '+--"). 
                # That gives the height.
                height = 0;
                width = 0
                for ix in range(i+1, numlines): 
                    if lines[ix][j] == '+' and lines[ix][j+1] == '-':
                        height = int((ix - i)/2)
                        break;

                # Similarly go east until see a NE corner. That gives width
                for jx in range(j+1, linesize):
                    if lines[i][jx] == '+' and lines[i+1][jx] == '|':
                        width = int((jx - j)/3)
                        break
                row = int(i / 2) + 1 # from char position to 1-based row/col
                col = int(j / 3) + 1 
                assert width > 0
                assert height > 0
                print ("{", f"r: {row}, c: {col}, h: {height}, w: {width}", "},")

    