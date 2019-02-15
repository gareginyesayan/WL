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

def textentry_feedback_in_correct(items):
    #Looking for items with feedback inside correct-option for FITB text
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        for text_entry in root.iter(cars.text_entry):
            for cor_opt in text_entry.iter(cars.correct_option):
                for child in cor_opt:
                    if (child.tag == cars.feedback):
                        affected_items.add(item)
        f.close()
        
    print ('list of items with feedback inside correct-option for FITB text')
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS');

def dropdown_feedback_in_correct(items):
# Finding items with grandchild having specific parent: 
#    <feedback> as child of <correct-option> which is child of drop-down-entry/text-entry 
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        for text_entry in root.iter(cars.drop_down_entry):
            for cor_opt in text_entry.iter(cars.correct_option):
                for child in cor_opt:
                    if (child.tag ==cars.feedback):
                        affected_items.add(item)
        f.close()
        
    print ('list of items with feedback inside correct-option for dropdowns')
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item);
    else:
        print ('ALL PASS'); 

def feedback_miss_paragraph(items):
#   Finding whether the paragraph is the child of feedback: 
#   item fails if paragraph is not a child or there is any text outside of paragraph 
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        required_tag = cars.paragraph;
        for fb in root.iter(cars.feedback):
            if (len(fb.findall(required_tag)) == 0):
                affected_items.add(item)
            fb_text = ''.join(fb.itertext())
            if fb_text !=None:
                    fb_text = ''.join(fb_text.split()) 
            par = fb.find(required_tag);
            try:
                
                par_text = ''.join(par.itertext());
                if par_text != None:
                    par_text = ''.join(par_text.split())
                if fb_text != par_text:
                    affected_items.add(item)
    #                print(item, par_text, fb_text)
            except:
    #            print('exception for', item)
                affected_items.add(item)
    
        f.close()
        
    print ('list of items having text outside of paragrpaph tg inside feedback')
    if (len(affected_items) != 0):  
        for affected_item in affected_items:
            print(affected_item[:-9]);
    else:
        print ('ALL PASS'); 


def feedback_in_fitb_cloze(items):
    print('Searching fo activity level (overall)  feedback tagged as child of fitb-cloze')
    affected_items = set();
    for item in items:
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        for cloze in root.iter(cars.fitb_cloze):
            for child in cloze:
                    if (child.tag == cars.feedback):
                        affected_items.add(item)

        f.close()
        
    for affected_item in affected_items:
        print(affected_item)
    if len(affected_items) ==0:
        print("ALL PASS")