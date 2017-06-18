# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 00:03:58 2017

@author: aryehzapinsky

sorter.py
This program goes through images in a folder and renames them if there is
date and time information.
Used to resolve numbering conflicts across multiple users with individual
filenames. Allows for master photos folder with uniform filename and
photographer's signature.
"""

from PIL import Image
import os

failed = open('failed.txt', 'w')
letter = "AK"
#direct = '/Users/aryehzapinsky/Pictures/Toronto 2016-2017/ArielK/'
direct = '/Users/aryehzapinsky/Documents/Programming/Photo\ Album\ Manipulation/TEST'
notAccepted = ['.AAE', '.MOV', '.png', '.mp4', '.DS_Store', '.gif']

for f in os.listdir(direct):
    if (f[f.rfind("."):] in notAccepted):
        failed.write("%s\t||\t%s\n" %(direct, f))
        continue
    #print (direct+f)
    fd = Image.open(direct+f)
    pic = fd._getexif()
    fd.close()
    #print(pic)
    if not(36867 in pic.keys()):
        failed.write("%s\t||\t%s\n" %(direct, f))
        continue
    dateTime = pic[36867][0]
    dateTime = dateTime.replace(":","")
    dateTime = dateTime.replace(" ", "_")
    if not(37521 in pic.keys()):
        failed.write("%s\t||\t%s\n" %(direct, f))
        continue
    secTime = pic[37521][0]

    #'''
    # Had to modify for files not preceded by IMG_
    # and for when secTime had null byte
    pos = secTime.find("\x00")
    if pos != -1:
        secTime = secTime[:pos]
    fut_name = "IMG_%s_%s_%s" %(dateTime, secTime, letter)
    cur_name = f[:f.rfind(".")]

    #'''

    #fut_name = "%s_%s_%s" %(dateTime, secTime, letter)
    #cur_name = f[f.find("_")+1:f.rfind(".")]

    os.rename(direct + f, direct + f.replace(cur_name, fut_name))

failed.close()
