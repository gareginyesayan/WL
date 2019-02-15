# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:03:17 2018

@author: GYesayan
"""
import os
import xml.etree.ElementTree as ET
import cars
import cl
import wl_content as ct
import ccilib as cci

def vocab_missed_labels(items):
    """
    Searches for vocabulary table with missed labels(overall number of labels < 2,
    labels with empty text ans missed label with 'type'='translation'
    
    Script gives some false positive due to not unique structure of vocabulary table:
        there are not vocabulary table items containing <list><complex-media>:
            they do not have <label> inside    
    """
  
    print('\nvocabulary table with missed labels(overall number of labels < 2,labels with empty text ans missed translation label\n')
    
    affected_items = set();
    for item in items:
        
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        list_order = 0;
        for vt in root.iter(cl.list):
            list_order = list_order + 1;
            media_order = 0;
            for complex_media in vt.iter(cars.complex_media):
                media_order = media_order + 1;
    #            print(media.attrib['type'])
                if (complex_media.attrib['type'] == 'audio-clip'):
                    translation_exists = False;
                    labels_len = len(list(complex_media.iter(cars.label)));
                    if (labels_len < 2):
                        affected_items.add(item);
                        print(item, 'labels =', labels_len, ' in list ',list_order, ' complex-media ', media_order);
                    for lbl in complex_media.iter(cars.label):
                        if 'type'  in lbl.attrib.keys():
                            if (lbl.attrib['type'] == 'translation'):
                               translation_exists = True; 
    
                        lbl_txt = ''.join(lbl.itertext()).strip();
    #                    print(lbl_txt)
                        if (lbl_txt == None or len(lbl_txt) == 0):
                            print(item, 'label text missed in list ', list_order, ' complex-media ', media_order);
                            affected_items.add(item);
                    if (translation_exists == False and 
                        len(list(complex_media.iter(cars.label)))!= 0):
                        print(item, 'translation missed in list ', list_order, ' complex-media ', media_order);
                        
    
        f.close()
      
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');    

def diagram_missed_labels(items):
    #Searching for diagrams with missed labels(term or translation) and labels with empty text
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        diag_order = 0; #not used, can be used  with commented printing below
        for diag in root.iter(cars.diagram):
            diag_order = diag_order + 1;
            media_order = 0; #not used, can be used  with commented printing below
            for complex_media in diag.iter(cars.complex_media):
                media_order = media_order + 1;
    #            print(media.attrib['type'])
                if (complex_media.attrib['type'] == 'audio-clip'):
                    if (len(list(complex_media.iter(cars.label))) < 2):
                        affected_items.add(item);
    #                    print(item, 'label missed in diagram ', diag_order, ' complex-media ', media_order);
                    for lbl in complex_media.iter(cars.label):
                        lbl_txt = ''.join(lbl.itertext()).strip();
    #                    print(lbl_txt)
                        if (lbl_txt == None or len(lbl_txt) == 0):
    #                        print(item, 'label text missed in diagram ', diag_order, ' complex-media ', media_order);
                            affected_items.add(item);
    
        f.close()
    print('\nItems with missed translation or term in diagram:')    
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');    

def cloze_dup_labels(items):
    #Searching for duplicate labels inside the same FITB Cloze
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
    
        for fitbcloze in root.iter(cars.fitb_cloze):   
            labels = set();
            for lbl in fitbcloze.iter(cars.label):
                lbl_text = ''.join(lbl.itertext());
                lbl_text = ''.join(lbl_text.split())
    #            print(lbl_text)
                if (lbl_text in labels):
                    if(lbl_text != None):
                        print(item, lbl_text);
                        affected_items.add(item)
                labels.add(lbl_text);
        f.close()
    
    print ('list of fitb cloze items with duplicated text labels')
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item[:-9]);
    else:
        print ('ALL PASS');

def matching_dup_labels(items):
    #Searching for matching pointer items (pointer and DnD) with duplicated text labels
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
    
        for mp in root.iter(cars.matching):   
            labels = set();
            for lbl in mp.iter(cars.label):
                lbl_text = ''.join(lbl.itertext());
                lbl_text = ''.join(lbl_text.split())
    #            print(lbl_text)
                if (lbl_text in labels):
                    if(lbl_text != None and lbl_text != ''):
    #                    print(lbl_text);
                        affected_items.add(item)
                labels.add(lbl_text);
                
        f.close()
    
    print ('list of matching items with duplicated text labels')
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item[:-9]);
    else:
        print ('ALL PASS');
