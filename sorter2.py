#!/usr/bin/env python3

"""
Created on Sunday June 18 2017

@author: aryehzapinsky

sorter2.py
v2 of sorter.py
"""

import os, sys, shutil
from PIL import Image

def sorter (filepath):
    while(True):
        if input("Are you sure you want to do this?\n"
                 "Please check that command line argument is root of folder "
                 "that you want to rename the pictures in.\n"
                 "Type 'Y' to proceed: ") == 'Y':
            break

    count = 0;
    for root, dirs, files in os.walk(filepath):
        if root == filepath:
            continue

        for fi in files:
            if ".DS_Store" in fi:
                continue
            fi_type = fi.rpartition('.')[2]
            initials = root.rpartition('/')[2].upper()

            with Image.open(root+'/'+fi) as img:
                pic = img._getexif()
                date_time = pic[36867].replace(":","").replace(" ", "_")
                sec_time = pic[37521].replace("\x00", "")
                if not date_time or not sec_time:
                    continue
                name = 'IMG_{}_{}_{}.{}'.format(date_time, sec_time,
                                                initials, fi_type)
                os.rename(os.path.join(root, fi),
                          os.path.join(filepath, name))
                print("Renamed and moved: ", name)
                count += 1
    print("{} pictures renamed and moved to root directory.".format(count))

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("usage: {} <path_to_root_of_aggregate_pictres_folder>"
              .format(sys.argv[0]))
        sys.exit()
    sorter(sys.argv[1])
    #sorter('/Users/aryehzapinsky/Documents/Programming/Photo\ Album\ Manipulation/TEST')
