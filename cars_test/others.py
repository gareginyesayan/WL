# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:03:17 2018

@author: GYesayan
"""
#import os
import xml.etree.ElementTree as ET
import cars
import cl
import re
#import wl_content as ct
#import ccilib as cci

def dup_media(items):
#    Finds duplicated media cgi-ref in items
    print('Looking for duplicated media inside the same item...\n')
    affected_items = set();
#    media_refs = {};
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        cgi_list = [];
        
        for media in root.iter(cars.media):
            cgi_ref = media.attrib['cgi-ref'];
            if cgi_ref in cgi_list:
                affected_items.add(item);
                print('media ',cgi_ref, 'in item ', item, '\n')
            else:
                cgi_list.append(cgi_ref);
                            
        f.close(); 
    print("full set of affected items\n")
    print(affected_items) 

def cloze_blanks_notequal_mappings(items):
    print("FITB Cloze: Looking for items with number of blanks not equal to the number of correct-mappings")
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        blanks = len(list(root.iter("{http://www.cengage.com/CARS/2}cloze-blank")))
        answers = len(list(root.iter("{http://www.cengage.com/CARS/2}correct-mapping")))
        if ((blanks > 0) and (blanks != answers)):
            affected_items.add(item)
            print('\n',item)
            print('blanks = ',len(list(root.iter("{http://www.cengage.com/CARS/2}cloze-blank"))))
            print('answers = ',len(list(root.iter("{http://www.cengage.com/CARS/2}correct-mapping"))))
        f.close()
    print('\nfull list of affected items:')    
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');     

def av_df_missed_cgi(items):
#searching for A/V, DF boards for incorrect or missed cgi
    items_cgi_incorrect = {'forum':set(), 'audio': set(), 'av_board': set()};
    items_cgi_missed = {'forum':set(), 'audio': set(), 'av_board': set()};
    
    print ('searching for A/V, DF boards for incorrect or missed cgi...')
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        
        for forum_entry in root.iter(cars.forum_entry):
            if 'cgi' not in forum_entry.attrib.keys():
                items_cgi_missed['forum'].add(item)
            else:
                if not re.match("^[A-Z0-9]*$",forum_entry.attrib['cgi']):
                     items_cgi_incorrect['forum'].add(item)
                     
                     
                     
        for av in root.iter(cars.audio_video_board_entry):
            if 'cgi' not in av.attrib.keys():
                items_cgi_missed['av_board'].add(item)
            else:
                if not re.match("^[A-Z0-9]*$",av.attrib['cgi']):
                     items_cgi_incorrect['av_board'].add(item)
                     
                     
        for audio in root.iter(cars.audio_entry):
            if 'cgi' not in audio.attrib.keys():
                items_cgi_missed['audio'].add(item)
            else:
                if not re.match("^[A-Z0-9]*$",audio.attrib['cgi']):
                     items_cgi_incorrect['audio'].add(item)                 
        f.close()             
    print('Missed\n',items_cgi_missed )
    print('\nincorrect\n',items_cgi_incorrect)
    

def ordinals_in_labels(items):
    #searching for ordinals in labels
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read();
        root = ET.fromstring(content);
        for lb in root.iter("{http://www.cengage.com/CARS/2}label"):
    #        print(kt.text)
    #        if '&#176'  in kt.text:
            if lb.text != None:
                if "1." in lb.text:
    #                print(lb.text)
                    affected_items.add(item)
    #                print(item)
        f.close()
        
    print("items with ordinals in labels")
    for affected_item in affected_items:
        print(affected_item)
    if len(affected_items) == 0:
        print("ALL PASS")

def key_term_test(items):
#Items with missed key terms or translations
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        for kte in root.iter(cl.key_term_entry):
            key_term = list(kte.iter(cl.key_term));
            key_term_def = list(kte.iter(cl.key_term_def));
            if ((len(key_term) != 1) or (len(key_term_def) != 1)):
                affected_items.add(item);
            else:
                ktd_text=''.join(key_term_def[0].itertext()).strip();
                kt_text=''.join(key_term[0].itertext()).strip();
                if(ktd_text == '' or kt_text == ''):
                    affected_items.add(item);
        f.close()
        
    print('\nfull list with missed key terms or translations:')    
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');    

def pointer_objects_vs_answers_old(items):
# Searching for matching pointer items with answers != objects in the biggest match-object group
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        for mp in root.iter(cars.matching):
            if mp.attrib['matching-type'] == 'pointing':
                left_gr_len = 0;     #for the case if the left match-group missed
                right_gr_len = 0;   #for the case if the right group missed
                map_gr_len = 0;     #for the case if the mapping-group missed
                try:
                    for m_group in mp.iter(cars.match_group):
                        if m_group.attrib['name'] == 'left':
                            left_gr_len = len(list(m_group.iter(cars.match_object)));
        #                    print(left_gr_len )
                        if m_group.attrib['name'] == 'right':
                            right_gr_len = len(list(m_group.iter(cars.match_object)));
        #                    print(right_gr_len);
    
                    for map_group in mp.iter(cars.mapping_group):
                        map_gr_len = len(list(map_group.iter(cars.correct_mapping)));
        #                print(map_gr_len);
    
                    if (max(left_gr_len, right_gr_len) != map_gr_len):
                        affected_items.add(item)
                    
                except:
                    print(item)
    print ('list of matching pointer items with answers not equal objects')
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item[:-9]);
    else:
        print ('ALL PASS');

def pointer_objects_vs_answers(items):
# Searching for matching pointer items with answers != objects in the biggest match-object group
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        for mp in root.iter(cars.matching):
            if mp.attrib['matching-type'] == 'pointing':
                left_gr_len = 0;     #for the case if the left match-group missed
                right_gr_len = 0;   #for the case if the right group missed
                map_gr_len = 0;     #for the case if the mapping-group missed
                first_group_names = [];
                second_group_names = [];
                group = 1;
                try:
                    for match_group in mp.iter(cars.match_group):
        
                        if group ==1:
                            for match_object in match_group.iter(cars.match_object):
                                first_group_names.append(match_object.attrib['name'])
        
                        if group ==2:
                            for match_object in match_group.iter(cars.match_object):
                                second_group_names.append(match_object.attrib['name'])
                 
                        group += 1;
                    left_gr_len = len(first_group_names)
                    right_gr_len = len(second_group_names)
    
                    for map_group in mp.iter(cars.mapping_group):
                        map_gr_len = len(list(map_group.iter(cars.correct_mapping)));
        #                print(map_gr_len);
    
                    if (max(left_gr_len, right_gr_len) != map_gr_len):
                        affected_items.add(item)
                    
                except:
                    print(item)
    print ('list of matching pointer items with answers not equal objects')
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item[:-9]);
    else:
        print ('ALL PASS');

    

def extra_mapping(items):
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        for matching in root.iter(cars.matching):
            if matching.attrib['matching-type'] in ["drag-and-drop", "pointing"]:
    #            drag_gr_len = 0;     #for the case if the drag missed
    #            drop_gr_len = 0;   #for the case if the drop group missed
    #            map_gr_len = 0;     #for the case if the mapping-group missed
                drag_group_names = [];
                drop_group_names = [];
                first_map_obj = [];
                second_map_obj = [];
                group = 1;
                for match_group in matching.iter(cars.match_group):
    
                    if group ==1:
                        for match_object in match_group.iter(cars.match_object):
                            drag_group_names.append(match_object.attrib['name'])
    
                    if group ==2:
                        for match_object in match_group.iter(cars.match_object):
                            drop_group_names.append(match_object.attrib['name'])
             
                    group += 1;
                         
                        
                # creating list of first and second objects in correct mapping
                for correct_mapping in matching.iter(cars.correct_mapping):
                    first_map_obj.append(correct_mapping[0].text);
                    second_map_obj.append(correct_mapping[1].text)
                    
                  
                first_corrects = set(first_map_obj);
                second_corrects = set(second_map_obj);
                drag_gn = set(drag_group_names);
                drop_gn = set(drop_group_names);     
    
    
                for name in first_corrects:
                    if name not in drag_gn:
                        affected_items.add(item)
                for name in second_corrects:
                    if name not in drop_gn:
                        affected_items.add(item)
    
        f.close()                
    print ('list of matching items with inconsistent mappings');
    print('extra mapping group (answer) or not correct order in mapping groups')
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print('\033[1;31;49m', affected_item, '\033[1;30;49m');
    else:
        print ('\033[1;32;49m ALL PASS \033[1;30;49m');


def diagram_missed_bg_image(items):
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        required_tag = cars.background;
        for fb in root.iter(cars.diagram):
            if (len(fb.findall(required_tag)) == 0):
                affected_items.add(item)
        f.close()
    print("\nItems having diagrams with missed background images");     
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item[:-9]);
    else:
        print ('ALL PASS');