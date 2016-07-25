# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 10:53:19 2016

@author: yiyuezhuo
"""

'''dwSize, dwFlags, dwHeight, dwWidth, dwPitchLinear, dwDepth, dwMipMapCount, ddpfPixelFormat, ddsCaps = unpack("<IIIIIII 44x 32s 16s 4x", header[4:])
'''
from struct import unpack, pack

from PIL import Image, ImageFile

import os



class Header(object):
    def __init__(self):
        self.magic = pack('BBBB', 0x44, 0x44, 0x53, 0x20)
        
        self.dwSize = None
        self.dwFlags = None
        self.dwHeight = None
        self.dwWidth = None
        self.dwPitchLinear = None
        self.dwDepth = None
        self.dwMipMapCount = None
        self.ddpfPixelFormat = None
        self.ddsCaps = None
        
        self._dwSize = None
        self._dwFlags = None
        self.dwFourCC = None
        self.dwRGBBitCount = None
        self.dwRBitMask = None
        self.dwGBitMask = None
        self.dwBBitMask = None
        self.dwABitMask = None
    def tobytes(self):
        dwSize, dwFlags, dwHeight, dwWidth, dwPitchLinear, dwDepth, dwMipMapCount, ddpfPixelFormat, ddsCaps = self.dwSize, self.dwFlags, self.dwHeight, self.dwWidth, self.dwPitchLinear, self.dwDepth, self.dwMipMapCount, self.ddpfPixelFormat, self.ddsCaps 
        _dwSize, _dwFlags, dwFourCC, dwRGBBitCount, dwRBitMask, dwGBitMask, dwBBitMask, dwABitMask = self._dwSize, self._dwFlags, self.dwFourCC, self.dwRGBBitCount, self.dwRBitMask, self.dwGBitMask, self.dwBBitMask, self.dwABitMask
        
        ddpfPixelFormat = pack('<IIIIIIII', _dwSize, _dwFlags, dwFourCC, dwRGBBitCount, dwRBitMask, dwGBitMask, dwBBitMask, dwABitMask)
        no_magic_header = pack("<IIIIIII 44x 32s 16s 4x", dwSize, dwFlags, dwHeight, dwWidth, dwPitchLinear, dwDepth, dwMipMapCount, ddpfPixelFormat, ddsCaps)
        return self.magic + no_magic_header

    def decode(self, header):
        assert self.magic == header[:4]
        dwSize, dwFlags, dwHeight, dwWidth, dwPitchLinear, dwDepth, dwMipMapCount, ddpfPixelFormat, ddsCaps = unpack("<IIIIIII 44x 32s 16s 4x", header[4:])
        self.dwSize, self.dwFlags, self.dwHeight, self.dwWidth, self.dwPitchLinear, self.dwDepth, self.dwMipMapCount, self.ddpfPixelFormat, self.ddsCaps = dwSize, dwFlags, dwHeight, dwWidth, dwPitchLinear, dwDepth, dwMipMapCount, ddpfPixelFormat, ddsCaps
        
        _dwSize, _dwFlags, dwFourCC, dwRGBBitCount, dwRBitMask, dwGBitMask, dwBBitMask, dwABitMask = unpack('<IIIIIIII', ddpfPixelFormat)
        self._dwSize, self._dwFlags, self.dwFourCC, self.dwRGBBitCount, self.dwRBitMask, self.dwGBitMask, self.dwBBitMask, self.dwABitMask = _dwSize, _dwFlags, dwFourCC, dwRGBBitCount, dwRBitMask, dwGBitMask, dwBBitMask, dwABitMask
    def __repr__(self):
        sdic = dict(_dwSize = self._dwSize, _dwFlags = self._dwFlags, dwFourCC = self.dwFourCC, dwRGBBitCount = self.dwRGBBitCount, dwRBitMask = self.dwRBitMask, dwGBitMask = self.dwGBitMask, dwBBitMask = self.dwBBitMask, dwABitMask = self.dwABitMask)
        dic = dict(dwSize = self.dwSize, dwFlags = self.dwFlags, dwHeight = self.dwHeight, dwWidth = self.dwWidth, dwPitchLinear = self.dwPitchLinear, dwDepth = self.dwDepth, dwMipMapCount = self.dwMipMapCount, ddpfPixelFormat = self.ddpfPixelFormat, ddsCaps = self.ddsCaps)
        dic['_ddpfPixelFormat'] = sdic
        return dic.__repr__()
        
class ClassicHeader(Header):
    def __init__(self):
        super(ClassicHeader, self).__init__()
        
        #self.magic = pack('BBBB', 0x44, 0x44, 0x53, 0x20)
        
        self.dwSize = 124
        self.dwFlags = 528391
        #self.dwHeight = None
        #self.dwWidth = None
        #self.dwPitchLinear = None
        self.dwDepth = 0
        self.dwMipMapCount = 0
        #self.ddpfPixelFormat = None
        self.ddsCaps = b'\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        
        self._dwSize = 32
        #self._dwFlags = None # RGB 64 RGBA 65
        self.dwFourCC = 0
        self.dwRGBBitCount = 32
        #self.dwRBitMask = None
        #self.dwGBitMask = None
        #self.dwBBitMask = None
        #self.dwABitMask = None
        
class ModelHeader(ClassicHeader):
    def __init__(self, mode, size):
        super(ModelHeader, self).__init__()
        
        self.dwWidth = size[0]
        self.dwHeight = size[1]
        
        self.dwRBitMask = 16711680
        self.dwGBitMask = 65280
        self.dwBBitMask = 255
        
        #self.dwRBitMask = 255
        #self.dwGBitMask = 65280
        #self.dwBBitMask = 16711680    
        
        #if mode == 'RGB':
        if len(mode) == 3: # RGB, BGR,...
            self._dwFlags = 64
            self.dwPitchLinear = size[0] * size[1] * 3
            self.dwABitMask = 0
        elif len(mode) == 4: # RGBA BGRA
        #elif mode == 'RGBA':
            self._dwFlags = 65
            self.dwPitchLinear = size[0] * size[1] * 4
            self.dwABitMask = 4278190080
        else:
            raise Exception('Unkown mode')
        
        #_dwSize, _dwFlags, dwFourCC, dwRGBBitCount, dwRBitMask, dwGBitMask, dwBBitMask, dwABitMask = unpack('<IIIIIIII', ddpfPixelFormat)
        ddpfPixelFormat = pack('<IIIIIIII', self._dwSize, self._dwFlags, self.dwFourCC, self.dwRGBBitCount, self.dwRBitMask, self.dwGBitMask, self.dwBBitMask, self.dwABitMask)
        self.ddpfPixelFormat = ddpfPixelFormat
        
def basic_decoder(data,mode='RGB'):
    # data are bytes
    #if mode in ['RGB','RGBA']: # base
    #    return data 
    len_mode = len(mode)
    block_count = len(data)//len_mode
    assert len(data) % len_mode == 0
    
    block_list = [data[i*len_mode : (i+1)*len_mode] for i in range(block_count)]
    
    r_index = mode.index('R')
    g_index = mode.index('G')
    b_index = mode.index('B')
    
    if len_mode == 3: # RBG,BRG...
        new_block_list = [b''.join([pack('B',block[r_index]), pack('B',block[g_index]), pack('B',block[b_index])]) for block in block_list]
        
    elif len_mode == 4: #ARGB,GAGB...
        a_index = mode.index('A')
        new_block_list = [b''.join([pack('B',block[r_index]), pack('B',block[g_index]), pack('B',block[b_index]), pack('B',block[a_index])]) for block in block_list]
        
    return b''.join(new_block_list)

        
def read_dds(path):
    if not(isinstance(path, Image.Image)):
        im = Image.open(path)
    else:
        im = path
    mode = 'BGRA' if im.mode == 'RGBA' else 'BGR'
    model = ModelHeader(mode, im.size)
    return model.tobytes() + basic_decoder(im.tobytes(), mode)
    
def to_dds(path, output_path = None):
    _bytes = read_dds(path)
    if output_path == None:
        fn, ext = os.path.splitext(path)
        output_path = fn + '.dds'
    with open(output_path, 'wb') as f:
        f.write(_bytes)
        
def bin_int32(int32):
    s = bin(int32)[2:]
    print('0'*(32-len(s))+s)

if __name__ == '__main__':
    with open('tech_aura_minefield.dds', 'rb') as f:
        header_bytes = f.read(128)
        
    
    with open('pulsar_icon.dds', 'rb') as f:
        header_bytes2 = f.read(128)
    
    header = Header()
    header.decode(header_bytes)
    header2 = Header()
    header2.decode(header_bytes2)
    header3 = Header()