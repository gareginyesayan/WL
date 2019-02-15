# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:03:17 2018

@author: GYesayan
"""

import os
import xml.etree.ElementTree as ET
import cars
import wl_content as ct
import ccilib as cci

def dnd_answer_order(items):
    #Checking that first (drag) group is on the first place in correct-mapping

    affected_items = set();
    media_refs = {};
    
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        for matching in root.iter(cars.matching):
            if matching.attrib['matching-type'] == "drag-and-drop":
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
    
    
                if (drag_gn < first_corrects or second_corrects != drop_gn):
                    affected_items.add(item)
    
        f.close()                
    print ('list of Drag and Drop items with with inconsistent mappings');
    print('match-objects do not exist in correct-mappings in correct order')
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print('\033[1;31;49m', affected_item, '\033[1;30;49m');
    else:
        print ('\033[1;32;49m ALL PASS \033[1;30;49m');
    
    
def ms_mc_equal_choices(items):
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
       
        for MC in root.iter(cars.multiple_choice):   
            answers = set();
            for ans in MC.iter(cars.answer):
                ans_all = ''.join(ans.itertext())
                if ans_all != None:
                    ans_txt = ''.join(ans_all.split())
                    if len(ans_txt) != 0:
    #                    print(ans_txt)
                        if ans_txt in answers:
                            print('\n')
                            affected_items.add(item);
                            print(item);
                            print(ans_txt)
                    answers.add(ans_txt);
        f.close()
    print('\nMC with equal choices (multi-select and single-select)')    
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');

def dropdown_single_choice(items):
    #Looking for dropdowns with choices < 2
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        for dd in root.iter(cars.drop_down_entry):
            answers = len(list(dd.iter(cars.answer)))
            if (answers < 2):
                affected_items.add(item)
                print('\n',item)
                print('answers = ',answers)
        f.close()
    print('\nDropdowns with choices < 2')    
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');    

def dropdown_dup_answers(items):
    #Looking for dropdowns with duplicated choices
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        
        for dd in root.iter(cars.drop_down_entry):   
            answers = set();
            for ans in dd.iter(cars.answer):
                ans_all = ''.join(ans.itertext())
                if ans_all != None:
                    ans_txt = ''.join(ans_all.split())
                    if len(ans_txt) != 0:
                        if ans_txt in answers:
                            print('\n')
                            affected_items.add(item);
                            print(item);
                            print(ans_txt)
                    answers.add(ans_txt);
        f.close()
    
    print('\nDropdowns with duplicated choices')    
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');    

def dropdown_backslash_in_answers(items):
    print('looking for backslash in dropdown predefined answers...') 
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        
        for dd in root.iter(cars.drop_down_entry):   
            for ans in dd.iter(cars.answer):
                if ans.text != None:
                    ans_txt = ''.join(ans.text.split())
        #            print(lb_txt);
        #            labels.append(lb_txt);
                    if len(ans_txt) != 0: 
                        if '/' in ans_txt  or '\\' in ans_txt:
                            affected_items.add(item); 
                            print(item, ans.text);
#                            print(co.text);
    
        f.close()
    if len(affected_items)==0:
        print("ALL PASS")  

def text_entry_backslash_in_answer(items):
    print('looking for backslash in text-entry predefined answers...') 
    affected_items = set();
    for item in items:
    #    print (item)
        f = open(item, 'r');
        content = f.read();
        co_txt = None;
        root = ET.fromstring(content);
        for te in root.iter(cars.text_entry):
            for co in te.iter(cars.answer):
        #        if lb.text == None:
        #            continue
                if co.text != None:
                    co_txt = ''.join(co.text.split())
        #            print(lb_txt);
        #            labels.append(lb_txt);
                    if len(co_txt) != 0: 
                        if '/' in co_txt  or '\\' in co_txt:
                            affected_items.add(item); 
                            print(item, co.text);
#                            print(co.text);
    
        f.close()
    if len(affected_items)==0:
        print("ALL PASS")
#    for affected_item in affected_items:
#        print(affected_item[:-9])


        
def dropdown_with_empty_ans(items):
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
    
        
        for dd in root.iter(cars.drop_down_entry):   
            answers = set();
            for ans in dd.iter(cars.answer):
                ans_txt = ''.join(ans.itertext())
                if ans_txt != None:
                    ans_txt = ''.join(ans_txt.split())
                if (len(ans_txt) == 0 or ans_txt == None):
                    affected_items.add(item);
        f.close()
    print('\nitems with missing text in dropdown answers:');
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');
        
    
def dropdowns_with_missed_correct(items):
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
    
        
        for dd in root.iter(cars.drop_down_entry):
            corrects_number = len(list(dd.iter(cars.correct_option)))
            if corrects_number == 0:
                affected_items.add(item);
        f.close()
    print('\nitems having dropdowns with missing correct option:');
    if (len(affected_items) != 0): 
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');
        
def mc_with_missed_correct(items):
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
    
        
        for mc in root.iter(cars.single_select):
            corrects_number = len(list(mc.iter(cars.correct_option)))
            if corrects_number == 0:
                affected_items.add(item);
        f.close()
    print('\nMC items having with missing correct option:');
    if (len(affected_items) != 0): 
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');
        
def ms_with_missed_correct(items):
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
    
        
        for ms in root.iter(cars.multi_select):
            corrects_number = len(list(ms.iter(cars.correct_option)))
            if corrects_number == 0:
                affected_items.add(item);
        f.close()
    print('\nMS items having with missing correct option:');
    if (len(affected_items) != 0): 
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');
#


