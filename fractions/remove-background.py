#!/usr/bin/env python3

# Remove backgrounds from all input files and save with same name elsewhere
# Started off trying to do this by automating GIMP, but that proved to be a
# bit difficult: GIMP uses Python 2 not 3, and its python support is primarily
# designed for running within the GIMP environment rather than running it externally.
# A bit of searching showed that it can be done using Pillow, the Python imaging
# library.  See this post:
#
# See https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent
#
# This solution is pretty limited, in that it hard-codes the background as being white.
# So, in current form, it won't work for any other background colour.
#
# More on doing it with GIMP here:
# # see https://stackoverflow.com/questions/60860673/gimp-python-fu-script-to-select-everything-with-a-given-color-and-change-it-to-a
#
# For reference commands are:
#
# theImage = pdb.gimp_file_load(in_filename, in_filename)
# --OR--
# theImage = gimp.image_list()[0] # interactive loading
# drawable = pdb.gimp_image_active_drawable(theImage)
# layer = pdb.gimp_image_merge_visible_layers(theImage, CLIP_TO_IMAGE)
# pdb.gimp_edit_bucket_fill(layer,BG_BUCKET_FILL,COLOR_ERASE_MODE,100.,0.,0,0.,0.)
# pdb.gimp_file_save(theImage, layer, out_filename, out_filename)

import os
from PIL import Image


def remove_background(source_file, target_file):
    """remove the background colour, making it transparent.
       works by getting each pixel in the image in RGBA form, where
       RGB encodes the colour (red, green, blue) and A is transparency.
       Any pixels that match white (RGB=255, 255, 255) have transparency
       set to zero.  The rest are left untouched.  The image is then saved
       to the target file
    """

    img = Image.open(source_file)
    img = img.convert('RGBA')
    data = img.getdata()

    newData = []
    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(target_file, "PNG")
    return


def convert_files(input_dir, output_dir):
    input_files = os.listdir(input_dir)
    for file in input_files:
        if file != ".DS_Store":
            source_name = input_dir + "/" + file
            target_name = output_dir + "/" + file
            remove_background(source_name, target_name)
        else:
            pass
    return len(input_files)


# main routine to run everything
if __name__ == "__main__":
    import sys

    # defaults for locations of input & output files
    source_dir = "tests/with-backgrounds"
    target_dir = "tests/without-backgrounds"

    # check if the source and target directories were provided
    # if not use defaults
    num_args = len(sys.argv) - 1
    if num_args != 2:
        print("Source and/or target dirs not supplied, using defaults")
        print("To override defaults:\n")
        print(f"\t{sys.argv[0]} source_directory target_directory\n")
    else:
        source_dir = sys.argv[1]
        target_dir = sys.argv[2]

    print(f"Reading from '{source_dir}', writing to '{target_dir}'...\n")
    num = convert_files(source_dir, target_dir)
    print(f"Finished. {num} files converted.\n")
    exit(0)
