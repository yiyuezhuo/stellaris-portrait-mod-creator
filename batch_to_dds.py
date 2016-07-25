# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 16:01:08 2016

@author: yiyuezhuo
"""

from uncompress import read_dds
from PIL import Image, ImageFile
import os

def image_shift(im, percent):
    diff = int(im.size[0] * percent)
    im2 = Image.new(im.mode, im.size)
    im2.paste(im.crop((0, 0, im.size[0] - diff, im.size[1])), (diff, 0, im.size[0], im.size[1]))
    im2.paste(im.crop((im.size[0] - diff, 0, im.size[0], im.size[1])), (0, 0, diff, im.size[1]))
    return im2

def tend_vertical(im, size):
    # protect y
    height = size[1]
    width = int(im.size[0]/(im.size[1]/size[1]))
    if width > size[0]:
        im = im.resize((width, height))
        padding = int((width - size[0]) / 2)
        return im.crop((padding, 0, padding + size[0], height))
    else:
        im2 = Image.new(im.mode, size)
        padding = int((size[0] - width) / 2)
        im2.paste(im.resize((width, height)), (padding, 0, padding + width, height))
        return im2


def png_to_dds(full_path, output_path, target_size = (425, 380), shift_percent = 0.0):
    im = Image.open(full_path)
    #im = im.resize((int(im.size[0]/(im.size[1]/380)), 380))
    im = tend_vertical(im, target_size)
    im = image_shift(im, shift_percent)
    _bytes = read_dds(im)
    
    filename = os.path.basename(full_path)
    fn, ext = os.path.splitext(filename)
    
    with open(os.path.join(output_path, fn + ".dds"), 'wb') as f:
        f.write(_bytes)

    #im.save(os.path.join(output_path ,fn + ".dds"))
        

def verify_path(path):
    if os.path.exists(path):
        return
    else:
        res, base = os.path.split(path)
        if res == '':
            os.mkdir(base)
        else:
            verify_path(res)
            os.mkdir(os.path.join(res,base))


def png_to_dds_map(root_path, root_output_path = None, verbose = True, shift_percent = 0.0):
    if root_output_path == None:
        root_output_path = root_path + '_dds'
    for rt, dirs, files in os.walk(root_path):
        for filename in files:
            fn, ext = os.path.splitext(filename)
            if ext == '.png':
                full_path = os.path.join(rt, filename)
                left,right = os.path.split(full_path)
                output_path = left.replace(root_path, root_output_path)
                verify_path(output_path)
                png_to_dds(full_path, output_path, shift_percent = shift_percent)
                if verbose:
                    print('{} -> {}'.format(full_path, os.path.join(output_path, fn + '.dds')))
