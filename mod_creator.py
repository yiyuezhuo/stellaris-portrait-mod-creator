# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 19:04:12 2016

@author: yiyuezhuo
"""
import jinja2
import os
from batch_to_dds import png_to_dds_map

def load_template(fname,tabMap='  '):
    with open(fname,'r',encoding='utf8') as f:
        s=f.read()
    return jinja2.Template(s.replace('\t',tabMap))
    
common_species_classes_template = load_template('common_species_classes_template.txt')
common_species_names_template = load_template('common_species_names_template.txt')
gfx_portraits_portraits_template = load_template('gfx_portraits_portraits_template.txt')

def common_species_classes_template_render(specie):
    portraits_list = [{'name' : portraits.name} for portraits in specie.portraits_list]
    return common_species_classes_template.render(specie_name = specie.name,
                                                  portraits_list = portraits_list)
    
def common_species_names_template_render(specie):
    return common_species_names_template.render(specie_name = specie.name)
    
def gfx_portraits_portraits_template_render(specie):
    label_list = []
    group_list = []
    label_map = {}
    
    for portraits in specie.portraits_list:
        group = {'name' : portraits.name,
                 'default' : None,
                 'portrait' : []}
        for portrait in portraits.portrait_list:
            label_list.append(portrait.name)
            # TODO ugly process
            #label_map[portrait.name] = os.path.join('gfx', 'models', portrait.path)
            label_map[portrait.name] = portrait.path
            group['portrait'].append(portrait.name)
        group['default'] = group['portrait'][0]
        group_list.append(group)
            
    return gfx_portraits_portraits_template.render(label_list = label_list,
                                                   group_list = group_list,
                                                   label_map  = label_map)


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
            
class Portrait(object):
    def __init__(self, name, path):
        '''
        name : portrait id in game
        path : portrait image file path in game
        '''
        self.name = name
        self.path = path
            
class Portraits(object):
    def __init__(self, name, portrait_list, path):
        '''
        name : portraits name
        portrait_list : portrait list
        path : raw project path
        '''
        self.name = name
        self.portrait_list = portrait_list
        self.path = path
            
class Specie(object):
    def __init__(self, name, portraits_list):
        '''
        name : specie name
        portraits_list : portraits list
        '''
        self.name = name
        self.portraits_list = portraits_list

class Mod(object):
    def __init__(self, name, specie_list):
        '''
        name : MOD name
        specie_list : specie list
        '''
        self.name = name
        self.specie_list = specie_list
    
    @staticmethod
    def read_raw(root, name = None):
        '''
        `raw` is not like to `real` mode
        `real` mode can run in game
        but `raw` is not but friendly to MODER
        '''
        if name == None:
            _, name = os.path.split(root)
        specie_list = []
        for specie_name in os.listdir(root):
            specie_path = os.path.join(root, specie_name)
            #specie_path = specie_name
            portraits_list = []
            for portraits_name in os.listdir(specie_path):
                portraits_path = os.path.join(specie_path, portraits_name)
                portrait_list = []
                for portrait_fname in os.listdir(portraits_path):
                    #portrait_path = os.path.join(portraits_path, portrait_name)
                    portrait_name, affix = os.path.splitext(portrait_fname)
                    portrait_path = os.path.join('gfx', 'models', specie_name, portraits_name, portrait_name + '.dds').replace('\\', '/')
                    portrait = Portrait(portrait_name, portrait_path)
                    portrait_list.append(portrait)
                portraits = Portraits(portraits_name, portrait_list, portraits_path)
                portraits_list.append(portraits)
            specie = Specie(specie_name, portraits_list)
            specie_list.append(specie)
        return Mod(name, specie_list)
    
    def save(self, root, png_trans = True):
        # setup
        common_species_classes_path = os.path.join(root, 'common', 'species_classes')
        common_species_names_path = os.path.join(root, 'common', 'species_names')
        gfx_portraits_portraits_path = os.path.join(root, 'gfx', 'portraits', 'portraits')
        models_path = os.path.join(root, 'gfx', 'models')
        for path in [common_species_classes_path, common_species_names_path, gfx_portraits_portraits_path, models_path]:
            verify_path(path)
        
        for i, specie in enumerate(self.specie_list):
            
            # txt generate
            common_species_classes_doc = common_species_classes_template_render(specie)
            common_species_names_doc = common_species_names_template_render(specie)
            gfx_portraits_portraits_doc = gfx_portraits_portraits_template_render(specie)
            
            _id = str(i) if i >= 10 else ('0' + str(i)) 
            
            common_species_classes_name = '_'.join([_id, self.name, specie.name, 'class.txt'])
            common_species_names_name = '_'.join([_id, self.name, specie.name, 'names.txt'])
            gfx_portraits_portraits_name = '_'.join([_id, self.name , specie.name, 'portraits.txt'])
            
            with open(os.path.join(common_species_classes_path, common_species_classes_name), 'w', encoding = 'utf8') as f:
                f.write(common_species_classes_doc)
            with open(os.path.join(common_species_names_path, common_species_names_name), 'w', encoding = 'utf8') as f:
                f.write(common_species_names_doc)
            with open(os.path.join(gfx_portraits_portraits_path, gfx_portraits_portraits_name), 'w', encoding = 'utf8') as f:
                f.write(gfx_portraits_portraits_doc)
                
            # png to dds
            if png_trans:
                for portraits in specie.portraits_list:
                    target_path = os.path.join(models_path, specie.name, portraits.name)
                    verify_path(target_path)
                    print(portraits.path)
                    png_to_dds_map(portraits.path, target_path, shift_percent = 0.1)
                
        
                    