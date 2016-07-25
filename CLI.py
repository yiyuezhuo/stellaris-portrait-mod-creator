# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 22:44:00 2016

@author: yiyuezhuo
"""

from mod_creator import Mod

import argparse

parser = argparse.ArgumentParser(usage = 'python CLI.py raw_mod_project_path target_mod_path',
                                 description = "Stellaris portrait MOD basic creator")
parser.add_argument('raw', help = 'raw mod project path')
parser.add_argument('target', help= 'target mod project path (eg.Paradox Interactive/Stellaris/mod/your_mod )')

args=parser.parse_args()

mod = Mod.read_raw(args.raw)
mod.save(args.target)