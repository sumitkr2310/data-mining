# -*- coding: utf-8 -*-
"""
#Application= [Extraxcting the info.]
#Filename   = [extracting_info.py]
#Directory  = [D:\SumeetKumar-21-Nov-2018\]
#Description= [Finds the contents and required info in the webpage]
#Created    = Mon Dec 17 17:56:20 2018
#Author     = [Sumeet kumar]
#Updated    = Mon Dec 17 17:56:20 2018
#Updator    = [Sumeet Kumar]

"""

from selenium import webdriver
import re
import os,shutil
     
#expression for fetching the website
exps = re.compile(r'\d+')
webexp2 = re.compile(r'w{,3}\.[\w \.\-\_]*\.net$')     #websites which ends with .net
webexp3 = re.compile(r'w{,3}\.[\w \.\-\_]*\.in$')      #websites which ends with .in
webexp4 = re.compile(r'w{,3}\.[\w \.\-\_]*\.org$')     #websites which ends with .org
webexp5 = re.compile(r'w{,3}\.[\w \.\-\_]*\.co$')      #websites which ends with .co
webexp6 = re.compile(r'w{,3}?\.?[\w \/ \? \= \.\-\_]*\.com\/?')     #websites which ends with .com
webexp7 = re.compile(r'w{,3}?\.?[\w \/ \? \= \. \- \_]*\.\w+\.?\w*\/?$')

    
#for fetching mobile number
mobile_exp = re.compile(r'[\d\+]?[\(  \d+ \)\+-/]+[\s\d+\+-/]{,7}?')

#for fetching email id
email_exp = re.compile(r'\w*?:?([\w\.-]+@[\w \-]+\-*\.\w{2,4}\.*\w*)')

#expression for zipcode
zipcode_exp = re.compile(r'\,?\s?(\d{5,6})$')


#regexpression lists
regex_list=[webexp2,webexp3,webexp4,webexp7,webexp5,webexp6]


#for counting the total number of blocks in a folder :
blocks_folder_path = "C:/Output folder/"

webpages_xpath = "//tbody[@id='tbody']/tr"

#Accessing chrome browser and path should be given where the unzipped file is existed.
browser = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
        
browser.get(blocks_folder_path)
    
blocks_file_count = browser.find_elements_by_xpath(webpages_xpath)

browser.quit()

blocks_page_count = len(blocks_file_count)

#for getting the inputs fields from the text.
file = open("blocks_analysis_inputs.txt","r") 
obj = file.readlines()
data_info = []

for line in obj: 
    line_info = line.split('|')
    data_info.append(line_info)

###############################################################################

def extract_function(blocks_page_count):
    
    if os.path.isdir("Text output folder"):
        shutil.rmtree("Text output folder")
        #os.rmdir("Text output folder")

    #for storing all the text file in a folder.
    os.mkdir("Text output folder") 

    
    #Accessing chrome browser and path should be given where the unzipped file is existed.
    browser = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
    
    i = 0
    while i < blocks_page_count:
        link_name = "C:/Output folder/blocks"+str(i)+".html"
        
        website_add_list = []
        email_id_list = []
        phone_no_list = []
        final_name_list = []
        zipcode_list = []
        browser.get(link_name)
        
        blocks_xpath = "//div[@id='datablock']"
        
        if '/tr' in data_info[i][0]:
            blocks_xpath = blocks_xpath + data_info[i][0]
        
        
        datablocks_list = browser.find_elements_by_xpath(blocks_xpath)
        
        plain_text_list = []
        for single_text in datablocks_list:
            plain_text_list.append(single_text.text)    
        
        div_count = 1
        for each_text in plain_text_list:
            if '\n' in each_text:
                txt_split = each_text.split("\n")
            else:
                txt_split = each_text.split()
            
            website_list = []
            website_flag = 0
            zipcode_flag = 0
            for txt in txt_split:
                for expressn in regex_list:
                    if '@' not in txt:
                        match_website = re.findall(expressn,txt)
                        if match_website:
                            for each_single_site in match_website:
                                if len(each_single_site) > 7:
                                    website_list.append(match_website[0])
                                    website_flag = 1
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
                if len(list(element))>9:
                    final_contact.append(element.strip())
            
            if each_text == '':
                phone_no_list.append("N/A")
            elif match_contact:
                try:
                    phone_no_list.append(final_contact[0])
                except:
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
            
            div_count = div_count+1
        
        #writing the    
        fp = open("Text output folder/block_"+str(i)+"_info.txt","w")
            
        line_num = 0
        while line_num < len(datablocks_list):
            line = str(str(final_name_list[line_num])+"|"+str(zipcode_list[line_num])+"|"+str(website_add_list[line_num])+"|"+str(email_id_list[line_num])+"|"+str(phone_no_list[line_num])+'\n')
            line_num = line_num+1
            fp.write(line)
        fp.close()
        i = i+1
    
    browser.quit()
    
#extract_function(blocks_page_count);

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
        
        if '/tr' in data_info[i][0] or 'li' in data_info[i][0]:
            blocks_xpath = blocks_xpath + data_info[i][0]
        
        
        datablocks_list = browser.find_elements_by_xpath(blocks_xpath)

        plain_text_list = []
        for single_text in datablocks_list:
            plain_text_list.append(single_text.text)    
        
        div_count = 1
        for each_text in plain_text_list:

            if '/tr' in data_info[i][0] or 'li' in data_info[i][0]:
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
            #line = str(str(website_add_list[line_num])+" | "+str(email_id_list[line_num])+" | "+str(phone_no_list[line_num])+'\n\n')
            line = str(str(final_name_list[line_num])+" | "+'\n\n')
            line_num = line_num+1
            fp.write(line)
        fp.close()
        i = i+1
    
    browser.quit()
    



        
    