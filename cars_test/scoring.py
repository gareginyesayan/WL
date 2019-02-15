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



def essay_shanswer_scoring(items, cci_file):
    items_points_incorrect = {'short_answer':set(), 'essay': set()};
    items_points_missed = {'short_answer':set(), 'essay': set()};

    cci_obj = cci.cci(cci_file);
    cci_dic = cci_obj.cci_dictionary;
    print ('searching for essays with incorrect or missed points-possible...')
    for item in items:
        try:
            if cci_obj.cci_dictionary['Activity step'][cci_obj.cci_dictionary['CGI'].index(item[:-9])] =='T':
                continue
        except:
            continue
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        cgi = item[:-9] #this is specific to Geyser item name
        essay_number = len(list(root.iter(cars.essay)));
          
        if (essay_number > 0):
            try:
                i = cci_dic['CGI'].index(cgi)
    
                while cci_dic['File Type'][i] != 'assessment item':
                    i=i-1;
    #            print(i, cci_dic['CGI'][i],'\n')
#                if 'essay' in cci_dic['Assessment Type'][i].lower():
#                    if 'short answer' in cci_dic['metadata_item_type'][i].lower():
                if 'essay' in cci_dic['metadata_item_type'][i].lower():
#                    print(item)
                    if 'short answer' in cci_dic['Assessment Type'][i].lower():
                        
                        try: 
                            for assessment in root.iter(cars.assessment):
                                points = assessment.attrib['points-possible']; 
                                if  points != '20':
                                    items_points_incorrect['short_answer'].add(item);
                        except:
                            items_points_missed['short answer'].add(item)
    #                        print('points-possible is missed')
                    else:
                        try: 
                            for assessment in root.iter(cars.assessment):
                                points = assessment.attrib['points-possible']; 
                                if  points != '30':
#                                    print(points, item)
                                    items_points_incorrect['essay'].add(item);
                        except:
                            items_points_missed['essay'].add(item)
            except:
                pass
    for key in items_points_incorrect:              
        print('\n',key, '\nincorrect points-possible');
        if (len(items_points_incorrect[key]) != 0):
            for item in items_points_incorrect[key]:
                print(item);
        else:
            print ('ALL PASS');
        
        print('\nmissed points-possible');
        if (len(items_points_missed[key]) != 0):
            for item in items_points_missed[key]:
                print(item);
        else:
            print ('ALL PASS');
       
    


def matching_cloze_scoring(items, cci_file):
    items_points_incorrect = {'matching':set(), 'cloze': set()};
    items_points_missed = {'matching':set(), 'cloze': set()};
    matching_points_incorrect_LR = set()
    cci_obj = cci.cci(cci_file)
    print ('searching for matchings and fitb-cloze with incorrect or missed points-possible...')
    for item in items:
        try:
            if cci_obj.cci_dictionary['Activity step'][cci_obj.cci_dictionary['CGI'].index(item[:-9])] =='T':
                continue
        except:
            continue
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        
        matching_number = len(list(root.iter(cars.matching)));
        cloze_number = len(list(root.iter(cars.fitb_cloze)));
       
        if (matching_number > 0):
            try:
                for assessment in root.iter(cars.assessment):
                    points = assessment.attrib['points-possible'];
                    if  points != '3':
                        if cci_obj.cci_dictionary['Activity step'][cci_obj.cci_dictionary['CGI'].index(item[:-9])] in ['P', 'U', 'G']:
                            items_points_incorrect['matching'].add(item);
                    if  points != '1':
                        if cci_obj.cci_dictionary['Activity step'][cci_obj.cci_dictionary['CGI'].index(item[:-9])] in ['L', 'R']:
                            matching_points_incorrect_LR.add(item);
            except:
                try:
                    if cci_obj.cci_dictionary['Activity step'][cci_obj.cci_dictionary['CGI'].index(item[:-9])] in ['P', 'U', 'G']:
                        items_points_missed['matching'].add(item)
                except:print(' item ', item, ' does not exist correctly in CCI')
                    
        
        if (cloze_number > 0):
            try:
                for assessment in root.iter(cars.assessment):
                    points = assessment.attrib['points-possible'];
                    if  points != '3':
                        if cci_obj.cci_dictionary['Activity step'][cci_obj.cci_dictionary['CGI'].index(item[:-9])] in ['P', 'U', 'G']:
                            items_points_incorrect['cloze'].add(item);
            except:
                if cci_obj.cci_dictionary['Activity step'][cci_obj.cci_dictionary['CGI'].index(item[:-9])] in ['P', 'U', 'G']:
                    items_points_missed['cloze'].add(item)
              
    for key in items_points_incorrect:              
        print('\n',key, '\nincorrect points-possible');
        if (len(items_points_incorrect[key]) != 0):
            for item in items_points_incorrect[key]:
                print(item);
        else:
            print ('ALL PASS');
            
             
    print('\n','matching_points_incorrect_LR');
    if (len(matching_points_incorrect_LR) != 0):
        for item in matching_points_incorrect_LR:
            print(item);
    else:
        print ('ALL PASS');  
            
        print('\nmissed points-possible');
        if (len(items_points_missed[key]) != 0):
            for item in items_points_missed[key]:
                print(item);
        else:
            print ('ALL PASS');
       


def df_essay_av_scoring(items, cci_file):
    items_points_incorrect = {'forum':set(), 'essay': set(), 'av_board': set(), 'aud_entry':set() };
    items_points_missed = {'forum':set(), 'essay': set(), 'av_board': set(), 'aud_entry':set() };
#    media_refs = {};
    cci_obj = cci.cci(cci_file)
    print ('searching for A/V, DF boards and essays with incorrect or missed points-possible...')
    for item in items:
        try:
            if cci_obj.cci_dictionary['Activity step'][cci_obj.cci_dictionary['CGI'].index(item[:-9])] =='T':
                continue
        except:
            continue
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        
        essay_number = len(list(root.iter(cars.essay)));
        audio_entry_number = len(list(root.iter(cars.audio_entry)));
        forum_entry_number = len(list(root.iter(cars.forum_entry)));
        audio_video_board_entry_number = len(list(root.iter(cars.audio_video_board_entry)));
        
        
        if (forum_entry_number > 0):
            try:
                for assessment in root.iter(cars.assessment):
                    points = assessment.attrib['points-possible'];
                    if  points != '30':
                        items_points_incorrect['forum'].add(item);
            except:
                items_points_missed['forum'].add(item)

        if (essay_number > 0):
            try:
                for assessment in root.iter(cars.assessment):
                    points = assessment.attrib['points-possible'];
                    if  points != '20' and points != '30':
                        items_points_incorrect['essay'].add(item);
            except:
                items_points_missed['essay'].add(item)

        if (audio_entry_number > 0):
            try:
                for assessment in root.iter(cars.assessment):
                    points = assessment.attrib['points-possible'];
                    if  points != '16':
                        items_points_incorrect['aud_entry'].add(item);
            except:
                items_points_missed['aud_entry'].add(item)

                
        if (audio_video_board_entry_number > 0):
            try:
                for assessment in root.iter(cars.assessment):
                    points = assessment.attrib['points-possible'];
                    if  points != '30':
                        items_points_incorrect['av_board'].add(item);
            except:
                items_points_missed['av_board'].add(item)

    for key in items_points_incorrect:              
        print('\n',key, '\nincorrect points-possible');
        if (len(items_points_incorrect[key]) != 0):
            for item in items_points_incorrect[key]:
                print(item);
        else:
            print ('ALL PASS');
        
        print('\nmissed points-possible');
        if (len(items_points_missed[key]) != 0):
            for item in items_points_missed[key]:
                print(item);
        else:
            print ('ALL PASS');
   

def text_dropdown_entry_scoring(items, cci_file):
    items_points_incorrect = set();
    items_points_missed = set();
    cci_obj = cci.cci(cci_file)
    print ('searching for FITB text-entry and dropdown items with incorrect or missed points-possible...')
    for item in items:
        try:
            if cci_obj.cci_dictionary['Activity step'][cci_obj.cci_dictionary['CGI'].index(item[:-9])] =='T':
                continue
        except:
            continue
        f = open(item, 'r');
        content = f.read()
        root = ET.fromstring(content);
        txt_entry_number = len(list(root.iter(cars.text_entry)));
        drop_down_number = len(list(root.iter(cars.drop_down_entry)));
        
        fields_number = txt_entry_number + drop_down_number;
        if (fields_number > 0):
            try:
                for assessment in root.iter(cars.assessment):
                    points = assessment.attrib['points-possible'];
                    if fields_number in range(1, 6) and points != '4':
                        items_points_incorrect.add(item)
                    if (fields_number in range(6, 11) and points != '10'):
                        items_points_incorrect.add(item)
                    if fields_number >10 and points != '16':
                        items_points_incorrect.add(item);
            except:
                items_points_missed.add(item)
             
    print('\nincorrect points-possible');
    if (len(items_points_incorrect) != 0):
        for item in items_points_incorrect:
            print(item[:-9]);
    else:
        print ('ALL PASS');
        
    print('\nmissed points-possible');
    if (len(items_points_missed) != 0):
        
        for item in items_points_missed:
            print(item);
    else:
        print ('ALL PASS');
        
 