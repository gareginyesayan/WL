# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 08:56:30 2017

@author: GYesayan
"""

import csv
#from openpyxl import load_workbook
#import os
#import xml.etree.ElementTree as ET

mode = {'L':'(Learn it!)', 'R': '(Ready?)', 'P':'(Practice it!)','U':'(Use it!)','G':'(Got it?)',}

class cci:
    
    _all_chapters = list(range(1,21));
    _all_chapters.append('P')
    
    def __init__(self, cci_file):
        self.cci_file = cci_file
        with open(self.cci_file, 'r') as f:
            reader = csv.reader(f)
            csv_data = list(reader);
        self.cci_dictionary = {}
        for i in range(30):
            self.cci_dictionary[csv_data[2][i]]=[row[i] for row in csv_data[3:]]
        self.cci_dictionary['Activity Number']=list(map(lambda x,y,z: x + y + '-' + z, 
                      self.cci_dictionary['Activity step'], 
                      self.cci_dictionary['Chapter'],
                      self.cci_dictionary['Activity number']))
#        return self.cci_dictionary;    
    
#########################################################################################################################
    def get_adf_cgi_from_chapter(self, chapter):
        adf_cgi_list = [x for x in self.cci_dictionary['CGI'] if 
                       ((self.cci_dictionary['Chapter'][self.cci_dictionary['CGI'].index(x)] == str(chapter))
                            and (self.cci_dictionary['File Type'][self.cci_dictionary['CGI'].index(x)] not in 
                            ['narrative item', 'assessment item', ''])
                            and x !='')]      
        return adf_cgi_list;
#    

    def get_adf_cgi_from_chapters(self, chapters_list = _all_chapters):
        chapters = list(map(lambda x: str(x), chapters_list))
        adf_cgi_list = [x for x in self.cci_dictionary['CGI'] if 
                       (self.cci_dictionary['Chapter'][self.cci_dictionary['CGI'].index(x)] in chapters
                            and self.cci_dictionary['File Type'][self.cci_dictionary['CGI'].index(x)] not in 
                            ['narrative item', 'assessment item', '']
                            and x !='')]      
        return adf_cgi_list;
#    
##########################################################################################################################
    def get_cars_cgi_from_chapter(self, chapter):
        cars_cgi_list = [x for x in self.cci_dictionary['CGI'] if 
                       (self.cci_dictionary['Chapter'][self.cci_dictionary['CGI'].index(x)] == str(chapter)
                            and self.cci_dictionary['File Type'][self.cci_dictionary['CGI'].index(x)] in 
                            ['narrative item', 'assessment item'])]      
        return cars_cgi_list;
    
    def get_cars_cgi_from_chapters(self, chapters_list = _all_chapters):
        chapters = list(map(lambda x: str(x), chapters_list))
        cars_cgi_list = [x for x in self.cci_dictionary['CGI'] if 
                       (self.cci_dictionary['Chapter'][self.cci_dictionary['CGI'].index(x)] in chapters
                            and self.cci_dictionary['File Type'][self.cci_dictionary['CGI'].index(x)] in 
                            ['narrative item', 'assessment item'])]      
        return cars_cgi_list;
    
    def get_HSA_cgi(self):
        hsa_cgi = []
        for cgi in self.cci_dictionary['CGI']:
            if self.cci_dictionary['Activity step'][self.cci_dictionary['CGI'].index(cgi)] == 'T':
                hsa_cgi.append(cgi)     
        return hsa_cgi;  
    
    def get_cars_cgi_all(self):
        cars_cgi_list = [x for x in self.cci_dictionary['CGI'] if 
                          (self.cci_dictionary['File Type'][self.cci_dictionary['CGI'].index(x)] in 
                           ['narrative item', 'assessment item'])]      
        return cars_cgi_list;
##################################################################################################################    

    def get_narrative_cars_cgi_from_chapter(self, chapter):
        narrative_cars_cgi_list = [x for x in self.cci_dictionary['CGI'] if 
                       (self.cci_dictionary['Chapter'][self.cci_dictionary['CGI'].index(x)] == str(chapter)
                            and self.cci_dictionary['File Type'][self.cci_dictionary['CGI'].index(x)] =='narrative item')]      
        return narrative_cars_cgi_list;

    def get_narrative_cars_cgi_from_chapters(self, chapters_list = _all_chapters):
        chapters = list(map(lambda x: str(x), chapters_list))
        cars_cgi_list = [x for x in self.cci_dictionary['CGI'] if 
                       (self.cci_dictionary['Chapter'][self.cci_dictionary['CGI'].index(x)] in chapters
                            and self.cci_dictionary['File Type'][self.cci_dictionary['CGI'].index(x)] =='narrative item')]      
        return cars_cgi_list;
###########################################################################################################################
    def get_unique_narrative_cgi_from_chapter(self, chapter):
        return list(set(self.get_narrative_cars_cgi_from_chapter(chapter)));
    
    
    def get_unique_cars_cgi_from_chapter(self, chapter):
        return list(set(self.get_cars_cgi_from_chapter(chapter)));
    
    def get_unique_cars_cgi_all(self):
        return list(set(self.get_cars_cgi_all()));
    
    
    
# ###################################################################################################################   

    def get_assessment_cars_cgi_from_chapter(self, chapter):
        assessment_cars_cgi_list = [x for x in self.cci_dictionary['CGI'] if 
                       (self.cci_dictionary['Chapter'][self.cci_dictionary['CGI'].index(x)] == str(chapter)
                            and self.cci_dictionary['File Type'][self.cci_dictionary['CGI'].index(x)] =='assessment item')]      
        return assessment_cars_cgi_list;


    def get_assessment_cars_cgi_from_chapters(self, chapters_list = _all_chapters):
        chapters = list(map(lambda x: str(x), chapters_list))
        cars_cgi_list = [x for x in self.cci_dictionary['CGI'] if 
                       (self.cci_dictionary['Chapter'][self.cci_dictionary['CGI'].index(x)] in chapters
                            and self.cci_dictionary['File Type'][self.cci_dictionary['CGI'].index(x)] =='assessment item')]      
        return cars_cgi_list;

##########################################################################################################################
    def print_cla_numbers(self, item_list, output = 0):
        for item in item_list:
            print(item, '\t', end="")
            for i in range(len(self.cci_dictionary['CGI'])):
                if self.cci_dictionary['CGI'][i] in item and self.cci_dictionary['CGI'][i] != '':
                    print(self.cci_dictionary['Activity Number'][i], '\t',end="")
            print('\n')

    def get_cla_numbers(self, item_list, output = 0):
        cla_set = set();
        for item in item_list:
            for i in range(len(self.cci_dictionary['CGI'])):
                if self.cci_dictionary['CGI'][i] in item and self.cci_dictionary['CGI'][i] != '':
                    cla_set.add(self.cci_dictionary['Activity Number'][i])
#                    print(self.cci_dictionary['Activity Number'][i], '\t',end="")
#            print('\n')
        return list(cla_set)
    
    def get_pages_count(self, cla):
        count = 0;
        for i in range(len(self.cci_dictionary['File Type'])):
            print
            if (self.cci_dictionary['File Type'][i] == 'page' 
                and self.cci_dictionary['Activity Number'][i] == cla):
                count = count + 1;
        return count;
    
    
    def get_cla_count(self, chapters_list = _all_chapters, output = 0):
        chapters = list(map(lambda x: str(x), chapters_list));
        count = 0;
        for i in range(len(self.cci_dictionary['File Type'])):
            if (self.cci_dictionary['File Type'][i] == 'multi-page sequence' 
                and self.cci_dictionary['Chapter'][i] in chapters):
                count = count + 1;
        return count;
    
    def get_cla_from_chapter(self, chapter, output = 0):
        chapter = str(chapter);
        cla=[];
        for i in range(len(self.cci_dictionary['File Type'])):
            if (self.cci_dictionary['File Type'][i] == 'multi-page sequence' 
                and self.cci_dictionary['Chapter'][i] == chapter
                and self.cci_dictionary['Activity step'][i] != 'T'):
                an = self.cci_dictionary['Activity Number'][i]
                cla.append(an);
        return list(cla);


def print_CLA_titles(csv_file, chapter):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        csv_data = list(reader);
#        print('csv_data[i][0]')
        
    for i in range(len(csv_data)):
#        print(csv_data[i][1])
        if csv_data[i][1] == str(chapter) and csv_data[i][5] == 'multi-page sequence':
            print(csv_data[i][0] + csv_data[i][1] +'-'+ csv_data[i][2],csv_data[i][6], mode[csv_data[i][0]] )
#    
#    def print_to_file(output_file, cgi_list):
#        with open(output_file,'w') as text_file:
#            for cgi in cgi_list:
#                print(cgi, file=text_file);
#
#
if __name__ == "__main__":
    title = 'Rutas'
    cci_file ='C:\\Users\\gyesayan\\CARS\\CCI\\' + title + '_CCI.csv';
    rut_cci = cci(cci_file);
    ch = [5]
    cars3_5_6 = rut_cci.get_narrative_cars_cgi_from_chapters([3,'P', 1])
    cgi = rut_cci.get_cars_cgi_all()
    cla= rut_cci.get_cla_from_chapter(2)
  
#    a = rut_cci.get_narrative_cars_cgi_from_chapters([3])
#    b = list(set(rut_cci.get_cars_cgi_from_chapter(9)))
#    c = rut_cci.get_adf_cgi_from_chapter(9)
#    c1 = rut_cci.get_cars_cgi_from_chapter(9)
#    rut_cci.print_cla_numbers(a[100:130])
    grid = rut_cci.cci_dictionary;
#    print(len(c))
#    print_CLA_titles(cci_file,6)
    cl = rut_cci.get_cla_numbers(rut_cci.get_cars_cgi_from_chapter(7)[10:20])
    rut_cci.print_cla_numbers(rut_cci.get_cars_cgi_from_chapter(7)[10:20])
    print(rut_cci.get_cla_count([9]))
