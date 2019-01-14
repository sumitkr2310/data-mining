# -*- coding: utf-8 -*-
"""
#Application= [Extraxcting the info.]
#Filename   = [extracting_info.py]
#Directory  = [D:\SumeetKumar-21-Nov-2018\]
#Description= [Finds the contents and required info in the webpage]
#Created    = Mon Dec 17 17:56:20 2018
#Author     = [Sumeet kumar]
#Updated    = Mon Jan 7 20:56:20 2018
#Updator    = [Sumeet Kumar]

"""

from selenium import webdriver
import re
import os,shutil
import time

     
#expression for fetching the website
exps = re.compile(r'\d+')
webexp1 = re.compile(r'w{,3}\.[\w \.\-\_]*\.co\.in') 
webexp2 = re.compile(r'w{,3}\.[\w \.\-\_]*\.net$')     #websites which ends with .net
webexp3 = re.compile(r'w{,3}\.[\w \.\-\_]*\.in')      #websites which ends with .in
webexp4 = re.compile(r'w{,3}\.[\w \.\-\_]*\.org$')     #websites which ends with .org
webexp5 = re.compile(r'w{,3}\.[\w \.\-\_]*\.co')      #websites which ends with .co
#webexp6 = re.compile(r'w{,3}?\.?[\w \/ \? \= \.\-\_]*\.com\/?')     #websites which ends with .com
webexp6 = re.compile(r'w{,3}?\.?[\w\/\?\=\.\-\_]*\.com\/?')     #websites which ends with .com
webexp7 = re.compile(r'w{,3}?\.?[\w \/ \? \= \. \- \_]*\.\w+\.?\w*\/?$')


#for fetching mobile number
mobile_exp = re.compile(r'\(?\+?\d{2,3}?\)?[\(  \d \)\+-/]*[\s\d+\+-/]{,7}?')

#for fetching email id
email_exp = re.compile(r'\w*?:?([\w\.-]+@[\w \-]+\-*\.\w{2,4}\.*\w*)')

#expression for zipcode
zipcode_exp = re.compile(r'\,?[A-Z]{2,3}\s(\d{5,6})$')


#regexpression lists
regex_list=[webexp2,webexp3,webexp4,webexp6,webexp5]


#for counting the total number of blocks in a folder :
blocks_folder_path = "C:/Output folder/"

webpages_xpath = "//tbody[@id='tbody']/tr"

#Accessing chrome browser and path should be given where the unzipped file is existed.
browser = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
        
browser.get(blocks_folder_path)
    
blocks_file_count = browser.find_elements_by_xpath(webpages_xpath)

browser.quit()

blocks_page_count = len(blocks_file_count)

#for getting the inputs fields from the text file to get the required info.
file = open("blocks_analysis_inputs.txt","r") 
obj = file.readlines()
data_info = []

for line in obj: 
    line_info = line.split('|')
    data_info.append(line_info)
    
#for getting the inputa fields to get the available hrefs.
href_file = open("hrefs_path_input.txt","r")
href_obj = href_file.readlines()
href_data_info = []

for line in href_obj:
    href_data_info.append(line.split('|'))


#checks if all the elements of the list are identical
def allthesame(l):
    #return np.all(np.diff(l)==0)
    if len(set(l)) == 1:
        return True
    else:
        return False


#################################################################################################

def name_fucntion(blocks_page_count):
    #Accessing chrome browser and path should be given where the unzipped file is existed.
    browser = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
    
    i = 0
    while i < blocks_page_count:
        link_name = "C:/Output folder/blocks"+str(i)+".html"
        final_name_list = []

        browser.get(link_name)
        
        blocks_xpath = "//div[@id='datablock']"
        
        if '/tr' in data_info[i][0] or '/li' in data_info[i][0]:
            blocks_xpath = blocks_xpath + data_info[i][0]
        
        
        datablocks_list = browser.find_elements_by_xpath(blocks_xpath)

        plain_text_list = []
        for single_text in datablocks_list:
            plain_text_list.append(single_text.text)    
        
        div_count = 1
        for each_text in plain_text_list:

            if '/tr' in data_info[i][0] or '/li' in data_info[i][0]:
                extra_path = data_info[i][1]
                name_xpath = blocks_xpath +"["+str(div_count)+"]"+ extra_path
            else:            
                name_xpath = blocks_xpath +"["+str(div_count)+"]"+ data_info[i][0]
            
            try:
                name_element = browser.find_element_by_xpath(name_xpath)
                final_name_list.append(name_element.text)
            except:
                final_name_list.append("N/A")
            
            div_count = div_count+1

        fp = open("Text output folder/name_only_"+str(i)+"_info.txt","w")
            
        line_num = 0
        while line_num < len(datablocks_list):
            line = str(str(final_name_list[line_num])+" | "+'\n\n')
            line_num = line_num+1
            fp.write(line)
        fp.close()
        i = i+1
    
    browser.quit()
    

###################################################################################################
        


def extract_function(blocks_page_count):

    #######################################################################################################
    
    def table_function(i,datablocks_list,blocks_xpath,urlname,href_xpath='',href_base='',href_base_flag='',href_td_positions=''):
    
        td1_list = []
        td2_list = []
        td3_list = []
        td4_list = []
        td5_list = []
        href_td_list = []
        
        td_tag_position = data_info[i][2].split(',')
        
        index0_flag = 0
        index1_flag = 0
        index2_flag = 0
        index3_flag = 0
        index4_flag = 0
            

        index = 0
        while index < len(td_tag_position):
            
            href_td_xpath_flag = 0
            for href_positions in href_td_positions:
                if td_tag_position[index] == href_positions:
                    href_td_xpath_flag = 1
                    break
            
            
            div_count = 1
            for x in datablocks_list:
                td_xpath_position = td_tag_position[index]
                
                extra_path = data_info[i][1]
            
                td_element_xpath = blocks_xpath +"["+str(div_count)+"]"+ extra_path +"["+str(td_xpath_position)+"]"
                
                indexhref_flag = 0
                if href_td_xpath_flag == 1:
                    try:
                        href_td_xpath = td_element_xpath + href_xpath
                        href_td_element = browser.find_element_by_xpath(href_td_xpath)
                        href_td_list.append(href_td_element.get_attribute("href"))
                    except:
                        href_td_list.append("N/A")
                    indexhref_flag = 1
            
            
                if index == 0:
                    try:
                        td_element = browser.find_element_by_xpath(td_element_xpath)
                        td1_list.append(td_element.text)
                    except:
                        td1_list.append("N/A")
                    index0_flag = 1
                
                elif index == 1:
                    try:
                        td_element = browser.find_element_by_xpath(td_element_xpath)
                        td2_list.append(td_element.text)
                    except:
                        td2_list.append("N/A")
                    index1_flag = 1
                
                elif index == 2:
                    try:
                        td_element = browser.find_element_by_xpath(td_element_xpath)
                        td3_list.append(td_element.text)
                    except:
                        td3_list.append("N/A")
                    index2_flag = 1
                
                elif index == 3:
                    try:
                        td_element = browser.find_element_by_xpath(td_element_xpath)
                        td4_list.append(td_element.text)
                    except:
                        td4_list.append("N/A")
                    index3_flag = 1
            
                elif index == 4:
                    try:
                        td_element = browser.find_element_by_xpath(td_element_xpath)
                        td5_list.append(td_element.text)
                    except:
                        td5_list.append("N/A")
                    index4_flag = 1
                        
                print("next div",div_count)
                
                div_count = div_count+1
            
            index = index+1
        
        if href_base_flag == 1 and '/C:' in href_td_list[1]:
            full_href_list = []
            for each_href in href_td_list:
                second_half_href = each_href.split('/C:')
                total_href = str(href_base) + str(second_half_href[1])
                full_href_list.append(total_href)
            href_td_list = full_href_list
        
        fp = open("Text output folder/block_"+str(i)+"_info.txt","w")
        
        try:
            fp.write(urlname+"\n\n")
    
            #if index0_flag == 1:
            title2_line = "NAME"
            if index1_flag == 1:
                title2_line = title2_line + "|LOCATION"
            if index2_flag == 1:
                title2_line = title2_line + "|PHONE NO."
            if index3_flag == 1:
                title2_line = title2_line + "|OTHER INFO"
            if indexhref_flag == 1:
                title2_line = title2_line + "|WEBSITE ADDR."
    
            fp.write(title2_line+"\n\n")
        
            line_num = 0
            while line_num < len(datablocks_list):
                #line = str(str(website_add_list[line_num])+" | "+str(email_id_list[line_num])+" | "+str(phone_no_list[line_num])+'\n\n')
                if index0_flag == 1:
                    line = str(str(td1_list[line_num]))
                if index1_flag == 1:
                    line = str(str(td1_list[line_num])+"|"+str(td2_list[line_num]))
                if index2_flag == 1:
                    line = str(str(td1_list[line_num])+"|"+str(td2_list[line_num])+"|"+str(td3_list[line_num]))
                if index3_flag == 1:
                    line = str(str(td1_list[line_num])+"|"+str(td2_list[line_num])+"|"+str(td3_list[line_num])+"|"+str(td4_list[line_num]))
                if index4_flag == 1:
                    line = str(str(td1_list[line_num])+"|"+str(td2_list[line_num])+"|"+str(td3_list[line_num])+"|"+str(td4_list[line_num])+"|"+str(td5_list[line_num]))
        
                if indexhref_flag == 1:
                    line = line +"|"+str(href_td_list[line_num])
                
                line = line + "\n"
        
                fp.write(line)
                
                line_num = line_num+1
        
        finally:
            fp.close()
    
    ###########################################################################################################
    
    if os.path.isdir("Text output folder"):
        shutil.rmtree("Text output folder")

    #for storing all the text file in a folder.
    os.mkdir("Text output folder") 

    
    #Accessing chrome browser and path should be given where the unzipped file is existed.
    browser = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
    
    i = 0
    i2 = 0
    while i < blocks_page_count:
        link_name = "C:/Output folder/blocks"+str(i)+".html"
        
        
        website_add_list = []
        email_id_list = []
        phone_no_list = []
        final_name_list = []
        zipcode_list = []
        href_website_list = []
        
        
        browser.get(link_name)
        
        try:
            urlname = browser.find_element_by_id('urlname').text
        except:
            print("pass")
            pass
        
        blocks_xpath = "//div[@id='datablock']"
        

        href_base_flag = href_xpath = href_base = href_base_flag = href_td_positions = ''
        if '#yes' in data_info[i]:
            href_xpath = href_data_info[i2][0]
            if '/tr' in data_info[i][0]:
                href_td_positions = href_data_info[i2][1].split(',')
            if len(href_data_info[i2]) == 2 or len(href_data_info[i2]) == 3:
                if 'base:' in href_data_info[i2][1]:                    ## 
                    split_base = href_data_info[i2][1].split('base:')
                    href_base = split_base[1]
                    href_base_flag = 1
            elif 'base:' in href_data_info[i2][2]:
                split_base = href_data_info[i2][2].split('base:')
                href_base = split_base[1]
                href_base_flag = 1
            i2 = i2+1
            
            
        
        if '/tr' in data_info[i][0]:
            blocks_xpath = blocks_xpath + data_info[i][0]
        
        
        datablocks_list = browser.find_elements_by_xpath(blocks_xpath)
        
        if len(data_info[i]) > 2 and '/tr' in data_info[i][0] and ',' in data_info[i][2]:
            table_function(i,datablocks_list,blocks_xpath,urlname,href_xpath,href_base,href_base_flag,href_td_positions);
            i=i+1
            continue
        
        plain_text_list = []
        for single_text in datablocks_list:
            plain_text_list.append(single_text.text)    
        
        div_count = 1
        for each_text in plain_text_list:
            if '\n' in each_text:
                txt_split = each_text.split("\n")
            else:
                txt_split = each_text.split()
            
            
            if '#yes' in data_info[i]:
                each_href_xpath = blocks_xpath + "["+str(div_count)+"]"+ href_xpath
                try:
                    href_element = browser.find_element_by_xpath(each_href_xpath)
                    href_value = href_element.get_attribute("href")
                    if '@' in href_value:
                        email_href_value = re.findall(email_exp, href_value)
                        href_website_list.append(email_href_value[0])
                    else:
                        href_website_list.append(href_value)
                    #href_website_list.append(href_element.get_attribute("href"))
                except:
                    href_website_list.append("N/A")
                            
            website_list = []
            website_flag = 0
            zipcode_flag = 0
            for txt in txt_split:
                for expressn in regex_list:
                    if '@' not in txt:
                        match_website = re.findall(expressn,txt)
                        if match_website:
                            for each_single_site in match_website:
                                if 'twitter.com' not in each_single_site and 'facebook.com' not in each_single_site and 'instagram.com' not in each_single_site:
                                    if len(each_single_site) > 7:
                                        website_list.append(match_website[0])
                                        website_flag = 1
                                else:
                                    website_flag = 0
                            break;
                match_zipcode = re.findall(zipcode_exp,txt)
                if match_zipcode:
                    zipcode_list.append(match_zipcode[0])
                    zipcode_flag = 1
            
            if zipcode_flag == 0:
                zipcode_list.append("N/A")
                        
            if website_flag == 0:
                website_add_list.append("N/A")
            else:
                website_add_list.append(website_list[0])
                
            match_email = re.findall(email_exp, each_text)
            
            email_id_flag = 0
            if match_email:
                final_email = []
                for each_email in match_email:
                    if "www." not in each_email:
                        final_email.append(each_email)
                        email_id_flag = 1
                if email_id_flag == 1:
                    email_id_list.append(final_email[0])
            else:
                email_id_list.append("N/A")    
                
            match_contact = re.findall(mobile_exp, each_text)
                
            final_contact = []

            for element in match_contact:
                if len(list(element)) > 9:
                    final_contact.append(element.strip())
            
            if each_text == '':
                phone_no_list.append("N/A")
            elif match_contact or (match_contact == []):
                try:
                    if ',' not in final_contact[0] and len(final_contact[0]) > 8:
                        phone_no_list.append(final_contact[0])
                    else:
                        phone_no_list.append("N/A")
                except:
                    if final_contact == []:
                        phone_no_list.append("N/A")
                    else:
                        phone_no_list.append(final_contact)
                    
            if '/tr' in data_info[i][0]:
                extra_path = data_info[i][1]
                name_xpath = blocks_xpath +"["+str(div_count)+"]"+ extra_path
            else:            
                name_xpath = blocks_xpath +"["+str(div_count)+"]"+ data_info[i][0]
            
            try:
                name_element = browser.find_element_by_xpath(name_xpath)
                final_name_list.append(name_element.text)
            except:
                final_name_list.append("N/A")
            
            print("next div",div_count)
                    
            div_count = div_count+1
        
        if href_base_flag == 1 and '/C:' in href_website_list[1]:
            full_href_list = []
            for each_href in href_website_list:
                second_half_href = each_href.split('/C:')
                total_href = str(href_base) + str(second_half_href[1])
                full_href_list.append(total_href)
            href_website_list = full_href_list
        
        #writing the data in the output text file in a foder named as  Text output folder.  
        fp = open("Text output folder/block_"+str(i)+"_info.txt","w")
        
        try:
        
            fp.write(urlname+"\n\n")
            
            title_line = ''
            
            if allthesame(final_name_list) == True:
                final_name_same = "yes"
            else:
                title_line = "NAMES"
                final_name_same = "no"
            
            if allthesame(zipcode_list) == True:
                zipcode_same = "yes"
            else:
                title_line = title_line + "|ZIPCODE"
                zipcode_same = "no"
            
            if allthesame(website_add_list) == True:
                website_add_same = "yes"
            else:
                title_line = title_line + "|WEBSITE ADDRESS"
                website_add_same = "no"
            
            if allthesame(email_id_list) == True:
                email_id_same = "yes"
            else:
                title_line = title_line + "|EMAIL-IDs"
                email_id_same = "no"
        
            if allthesame(phone_no_list) == True:
                phone_no_same = "yes"
            else:
                title_line = title_line + "|PHONE NOs"
                phone_no_same = "no"
        
            if '#yes' in data_info[i]:
                if allthesame(href_website_list) == True:
                    href_website_same = "yes"
                else:
                    title_line = title_line + "|OTHER INFO(website or mail-id)"
                    href_website_same = "no"
        
            fp.write(title_line+"\n\n")
            
            line = ''
            line_num = 0
            while line_num < len(datablocks_list):
                try:
                    if final_name_same != "yes":
                        line = str(final_name_list[line_num])
                    if zipcode_same != "yes":
                        line = line +"|"+ str(zipcode_list[line_num])
                    if website_add_same != "yes":
                        line = line +"|"+ str(website_add_list[line_num])
                    if email_id_same != "yes":
                        line = line +"|"+ str(email_id_list[line_num])
                    if phone_no_same != "yes":
                        line = line +"|"+ str(phone_no_list[line_num]) 
                    if '#yes' in data_info[i]:
                        if href_website_same != "yes":
                            line = line +"|"+ str(href_website_list[line_num])
                
                    line = line +"\n"    
                except:
                    print("Errroorrrrrrrr\n")
                
                fp.write(line)
                line_num = line_num+1
        
        except:
            print("errror  2  \n\n")
        
        finally:
            fp.close()
        
        i = i+1
    
    browser.quit()


try:
    extract_function(blocks_page_count)
except:
    time.sleep(3)
    try:
        extract_function(blocks_page_count)
    except:
        time.sleep(3)
        extract_function(blocks_page_count)



#END OF FILE



#line = str(str(final_name_list[line_num])+str(zipcode_list[line_num])+str(website_add_list[line_num])+"|"+str(email_id_list[line_num])+"|"+str(phone_no_list[line_num])+"|"+str(href_website_list[line_num])+'\n')

#line = str(str(final_name_list[line_num])+"|"+str(zipcode_list[line_num])+"|"+str(website_add_list[line_num])+"|"+str(email_id_list[line_num])+"|"+str(phone_no_list[line_num])+'\n')

'''
def table_function(i,datablocks_list,blocks_xpath,urlname,href_td_positions,href_xpath):
    
    td1_list = []
    td2_list = []
    td3_list = []
    td4_list = []
    td5_list = []
    href_td_list = []
    td_tag_position = data_info[i][2].split(',')
    
    
    index = 0
    while index < len(td_tag_position):
        
        href_td_xpath_flag = 0
        for href_positions in href_td_positions:
            if td_tag_position[index] == href_positions:
                href_td_xpath_flag = 1
                break
        
        div_count = 1
        for x in datablocks_list:
            td_xpath_position = td_tag_position[index]
            
            extra_path = data_info[i][1]
            
            td_element_xpath = blocks_xpath +"["+str(div_count)+"]"+ extra_path +"["+str(td_xpath_position)+"]"
            
            if href_td_xpath_flag == 1:
                try:
                    href_td_xpath = td_element_xpath + href_xpath
                    href_td_element = browser.find_element_by_xpath(href_td_xpath)
                    href_td_list.append(href_td_element.get_attribute("href"))
                except:
                    href_td_list.append("N/A")
                indexhref_flag = 1
            
            index0_flag = 0
            index1_flag = 0
            index2_flag = 0
            index3_flag = 0
            index4_flag = 0
            
            if index == 0:
                try:
                    td_element = browser.find_element_by_xpath(td_element_xpath)
                    td1_list.append(td_element.text)
                except:
                    td1_list.append("N/A")
                index0_flag = 1
                
            elif index == 1:
                try:
                    td_element = browser.find_element_by_xpath(td_element_xpath)
                    td2_list.append(td_element.text)
                except:
                    td2_list.append("N/A")
                index1_flag = 1
                
            elif index == 2:
                try:
                    td_element = browser.find_element_by_xpath(td_element_xpath)
                    td3_list.append(td_element.text)
                except:
                    td3_list.append("N/A")
                index2_flag = 1
                
            elif index == 3:
                try:
                    td_element = browser.find_element_by_xpath(td_element_xpath)
                    td4_list.append(td_element.text)
                except:
                    td4_list.append("N/A")
                index3_flag = 1
            
            elif index == 4:
                try:
                    td_element = browser.find_element_by_xpath(td_element_xpath)
                    td5_list.append(td_element.text)
                except:
                    td5_list.append("N/A")
                index4_flag = 1
                        
            print("next div",div_count)
        
            div_count = div_count+1
            
        index = index+1
        
    fp = open("Text output folder/table_block_"+str(i)+"_info.txt","w")
    
    fp.write(urlname+"\n\n")
    
    #if index0_flag == 1:
    title2_line = "NAME"
    if index1_flag == 1:
        title2_line = title2_line + "|LOCATION"
    if index2_flag == 1:
        title2_line = title2_line + "|PHONE NO."
    if index3_flag == 1:
        title2_line = title2_line + "|OTHER INFO"
    if indexhref_flag == 1:
        title2_line = title2_line + "|WEBSITE ADDR."
    
    fp.write(title2_line+"\n\n")
        
    line_num = 0
    while line_num < len(datablocks_list):
        #line = str(str(website_add_list[line_num])+" | "+str(email_id_list[line_num])+" | "+str(phone_no_list[line_num])+'\n\n')
        if index0_flag == 1:
            line = str(str(td1_list[line_num]))
        elif index1_flag == 1:
            line = str(str(td1_list[line_num])+"|"+str(td2_list[line_num]))
        elif index2_flag == 1:
            line = str(str(td1_list[line_num])+"|"+str(td2_list[line_num])+"|"+str(td3_list[line_num]))
        elif index3_flag == 1:
            line = str(str(td1_list[line_num])+"|"+str(td2_list[line_num])+"|"+str(td3_list[line_num])+"|"+str(td4_list[line_num]))
        elif index4_flag == 1:
            line = str(str(td1_list[line_num])+"|"+str(td2_list[line_num])+"|"+str(td3_list[line_num])+"|"+str(td4_list[line_num])+"|"+str(td5_list[line_num]))
        
        if indexhref_flag == 1:
            line = line +"|"+str(href_td_list[line_num])
        
        line = line + "\n"
        
        fp.write(line)
        line_num = line_num+1
    
    fp.close()





'''