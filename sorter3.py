#!/Users/aryehzapinsky/Documents/Programming/Photo_Album_Manipulation/env/bin/python3

"""
Created on Sunday June 18 2017

@author: aryehzapinsky

sorter2.py
v2 of sorter.py
"""

import os, sys, shutil
from PIL import Image
import json

def sorter (filepath, json_number):
    while(True):
        if input("Are you sure you want to do this?\n"
                 "Please check that command line argument is root of folder "
                 "that you want to rename the pictures in.\n"
                 "Type 'Y' to proceed: ") == 'Y':
            break

    #count = 0;
    names_dict = {}
    for root, dirs, files in os.walk(filepath):
        if root == filepath:
            continue

        bogus_sec = 0
        for fi in files:
            if ".jpg" not in fi.lower() or fi[0] == ".":
                print ("{} does not have .jpg in name".format(fi))
                continue
            fi_type = fi.rpartition('.')[2]
            initials = root.rpartition('/')[2].upper()

            with Image.open(root+'/'+fi) as img:
                pic = img._getexif()
                date_time = (pic[36867].replace(":","")
                                       .replace(" ", "_")
                                       .replace("/", ""))
                sec_time = ""
                if 37521 in pic:
                    sec_time = pic[37521].replace("\x00", "")
                else:
                    sec_time = str(bogus_sec).zfill(3)
                    bogus_sec += 1
                if not date_time or not sec_time:
                    print("{} has no time information | {} | {}".format(fi, date_time, sec_time))
                    continue
                name = 'IMG_{}_{}_{}.{}'.format(date_time, sec_time,
                                                initials, fi_type)
                os.rename(os.path.join(root, fi),
                          os.path.join(filepath, name))
                names_dict.update({name:initials+"/"+fi})
                print("Renamed and moved: {}: {}".format(name, names_dict[name]))

                #count += 1
    print("{} pictures renamed and moved to root directory.".format(
        #count
        len(names_dict)
    ))

    json_file = os.path.join(filepath, "names_dict"+str(json_number)+".json")
    with open(json_file, 'w') as outfile:
        json.dump(names_dict, outfile)

        print("JSON file: {} successfully created.".format(json_file))

if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print("usage: {} <path_to_root_of_aggregate_pictres_folder> <number_json_creating>"
              .format(sys.argv[0]))
        sys.exit()
    sorter(sys.argv[1], sys.argv[2])
    #sorter('/Users/aryehzapinsky/Documents/Programming/Photo_Album_Manipulation/TEST')
