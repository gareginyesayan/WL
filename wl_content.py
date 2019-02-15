# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 08:56:30 2017

@author: GYesayan
"""

#import csv
#from openpyxl import load_workbook
import os
import xml.etree.ElementTree as ET
import cars
from ccilib import cci
import wl_elements as el

#class dropdown:
#   
#    def __init__(self, items, fields_count, items_count):
#        self.fields_count = fields_count; 
#        self.items = items;
#        self.items_count = items_count; 
    

class geyser_content:

    _all_chapters = list(range(1,21));
    _all_chapters.append('P') 
    
   
    def __init__(self, content_folder, chapters_list = _all_chapters):
        self.content_folder = content_folder
        os.chdir(self.content_folder);
        items = os.listdir(self.content_folder)
#        removing all not xml files from item list
        self.items = list(filter(lambda x: '.xml' in x.lower(), items))
        

#        cr = set(self.cci.get_unique_cars_cgi_from_chapter(chapters[0]))
#        s  = set(self.items)
#        temp = [x for x in s if x[13:-4] not in cr]
#        print(temp)
        

################################################################################
    
    def get_assessments(self):
        a_items = set();
        required_tag = cars.assessment;
        for item in self.items:
            try:
                f = open(item, 'r', encoding='utf-8');
                ct = f.read()
                root = ET.fromstring(ct);
                for a in root.iter(required_tag):
                    a_items.add(item);
                f.close()
            except:
                print('exception:',item)
        return list(a_items)
    
    def get_narratives(self):
        n_items = set();
        required_tag = cars.narrative_item;
        for item in self.items:
            try:
                f = open(item, 'r', encoding='utf-8');
                ct = f.read()
                root = ET.fromstring(ct);
                for n in root.iter(required_tag):
                    n_items.add(item);
                f.close()
            except:
                print('exception:',item)
        return list(n_items)
    
###############################################################################        
        
    def get_MC(self):
        ss_items = set();
        required_tag = cars.single_select;
        mc = {'count': 0, 'items': []};
        for item in self.items:
            try:
                f = open(item, 'r', encoding='utf-8');
                ct = f.read()
                root = ET.fromstring(ct);
                for ss in root.iter(required_tag):
                    mc['count'] += 1;
                    ss_items.add(item);
                mc['items'] = list(ss_items)
                mc_object =el.single_select(mc['items'],mc['count'], len(mc['items']))
                f.close()
            except:
                print('exception:',item)
        return mc_object
    
    def get_MS(self):
        ms_items = set();
        required_tag = cars.multi_select;
        ms = {'count': 0, 'items': []};
        for item in self.items:
            try:
                f = open(item, 'r', encoding='utf-8');
                ct = f.read()
                root = ET.fromstring(ct);
                for m in root.iter(required_tag):
                    ms['count'] += 1;
                    ms_items.add(item);
                ms['items'] = list(ms_items)
                ms_object =el.multi_select(ms['items'],ms['count'], len(ms['items']))
                f.close()
                f.close()
            except:
                print('exception:',item)
        return ms_object

############################################################################

   
    def get_text_entries(self):
        te_items = set();
        required_tag = cars.text_entry;
        te = {'count': 0, 'items': []};
        for item in self.items:
            try:
                f = open(item, 'r', encoding='utf-8');
                ct = f.read()
                root = ET.fromstring(ct);
                for t in root.iter(required_tag):
                    te['count'] +=1;
                    te_items.add(item);
                te['items'] = list(te_items);
                te_object = el.text_entry(te['items'],te['count'], len(te['items']))
                f.close()
            except:
                print('exception:',item)
        return te_object

    def get_dropdowns(self):
        dd_items = set();
        required_tag = cars.drop_down_entry;
        dd= {'count': 0, 'items': []};
        for item in self.items:
            try:
                f = open(item, 'r', encoding='utf-8');
                ct = f.read()
                root = ET.fromstring(ct);
                for d in root.iter(required_tag):
                    dd['count'] +=1;
                    dd_items.add(item);
                dd['items'] = list(dd_items);
                d_object = el.dropdown(dd['items'],dd['count'], len(dd['items']))
                f.close()
            except:
                print('exception:',item)
        return d_object;
#

    def get_element_by_tag(self, required_tag):
        dd_items = set();
#        required_tag = cars.drop_down_entry;
        dd= {'count': 0, 'items': []};
        for item in self.items:
            try:
                f = open(item, 'r', encoding='utf-8');
                ct = f.read()
                root = ET.fromstring(ct);
                for d in root.iter(required_tag):
                    dd['count'] +=1;
                    dd_items.add(item);
                dd['items'] = list(dd_items);
#                d_object = el.dropdown(dd['items'],dd['count'], len(dd['items']))
                f.close()
            except:
                print('exception:',item)
        return dd;
#
    def keep_cars_from_chapters(self, cci_file, chapters_list = _all_chapters):
        os.chdir(self.content_folder);
        items = os.listdir(self.content_folder)
#        removing all not xml files from item list
        self.items = list(filter(lambda x: '.xml' in x.lower(), items))
        self.cci = cci(cci_file);
        chapters = list(map(lambda x: str(x), chapters_list))
#        print(chapters)
        req_cgi = self.cci.get_cars_cgi_from_chapters(chapters)
        req_cgi = list(set(req_cgi))
#        print(len(req_cgi))
        all_items = [];
        for cgi in req_cgi:
            try:
                item  = list(filter(lambda x: cgi in x.upper(), self.items))[0]
                all_items.append(item);
            except:
                print('cannot find cgi ', cgi, 'in folder' )
        self.items = all_items

    def keep_only_HSA(self, cci_file, items):
        self.cci = cci(cci_file);
        hsa_items = []
        hsa_cgi = self.cci.get_HSA_cgi()
        for item in items:
           for cgi in hsa_cgi:
               if cgi in item:
                   hsa_items.append(item)
                   
        return hsa_items
    

    def exclude_HSA(self, cci_file, items):
        self.cci = cci(cci_file);
        noHSA_items = items
        hsa_cgi = self.cci.get_HSA_cgi()
        for item in items:
           for cgi in hsa_cgi:
               if cgi in item:
                   noHSA_items.remove(item)
                 
        return noHSA_items                
            


if __name__ == "__main__":
    fol = 'C:\\Users\\gyesayan\\CARS\\Rutas';
    Juntos = geyser_content(fol);
    title = 'Rutas'
    cci_file ='C:\\Users\\gyesayan\\CARS\\CCI\\' + title + '_CCI.csv';
    Juntos.keep_cars_from_chapters(cci_file, [2])
#    it= Juntos.items;
#    mc = Juntos.get_MC()
#    ms = Juntos.get_MS()
#    a = Juntos.get_narratives();
#    te = Juntos.get_MS()
#    print(te.items_count)
#    Juntos.keep_cars_from_chapters(cci_file, ['P',3])
#    te = Juntos.get_MS()
#    print(te.items_count, te.fields_count)
#    tag = Juntos.get_element_by_tag(cars.multi_select)

    
    


