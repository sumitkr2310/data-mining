# -*- coding: utf-8 -*-
"""
#Application= [Extraxcting the required info like name, phone no, email ids,websites, etc.]
#Filename   = [extracting_mail_cont.py]
#Directory  = [D:\SumeetKumar-21-Nov-2018\]
#Description= [Finds the email-ids and makes a list of emails along with the contact no. from the web page]
#Created    = Mon Jan 14 17:21:19 2019
#Author     = [User]
#Updated    = Mon Jan 14 17:21:19 2019
#Updator    = [Sumeet Kumar]

"""


from selenium import webdriver
import re
import os,shutil
import time
from sys import exit

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from  more_itertools import unique_everseen  #this is used for remove duplicates from a particular list without losing order preferences


#expression for fetching the website
exps = re.compile(r'\d+')
webexp1 = re.compile(r'w{,3}\.[\w \.\-\_]*\.co\.in') 
webexp2 = re.compile(r'w{,3}\.[\w \.\-\_]*\.net')     #websites which ends with .net
webexp3 = re.compile(r'w{,3}\.[\w \.\-\_]*\.in')      #websites which ends with .in
webexp4 = re.compile(r'w{,3}\.[\w \.\-\_]*\.org')     #websites which ends with .org
webexp5 = re.compile(r'w{,3}\.[\w \.\-\_]*\.co')      #websites which ends with .co
#webexp6 = re.compile(r'w{,3}?\.?[\w \/ \? \= \.\-\_]*\.com\/?')     #websites which ends with .com
webexp6 = re.compile(r'w{,3}?\.?[\w\/\?\=\.\-\_]*\.com\/?')     #websites which ends with .com
webexp7 = re.compile(r'w{,3}?\.?[\w\/\?\=\.\-\_]*\.\w+\.?\w*\/?$')


#for fetching mobile number
#mobile_exp = re.compile(r'\(?\+?\d{2,4}?\)?\s?[\(\d \.\)\+\-\.\/]*[\s\d+\+-/]{,7}?')
#mobile_exp = re.compile(r'.?\s?([\(\d\.\)\+\-\.\/]*[\s\d+\+-/]{,7}?)')
mobile_exp = re.compile(r'\s?(\(\d{2,3}\)\s?[\d\. \+\-\/]*)')
mobile_exp2 = re.compile(r'.?([\d{2,3}\s]*\(\d{2,3}\)\s?[\d\.\+\-\/]*)')
mobile_exp3 = re.compile(r'\s?([\d\. \-\/\,]*)')        #modified - added "\,"
mobile_exp4 = re.compile(r'\s?\+?\d{2,3}?\s{1,3}?\-?\s{1,3}?\d{7,11}\s?\,?')

mobile_regex_list = [ mobile_exp3, mobile_exp2, mobile_exp]
#mobile_regex_list = [ mobile_exp4, mobile_exp3]


#for fetching email id
email_exp = re.compile(r'\w*?:?([\w\.-]+@[\w \-]+\-*\.\w{2,4}\.*\w*)')



#expression for zipcode
zipcode_exp = re.compile(r'\,?\s{,2}?([A-Z]{2,3}?\,?\s{,3}?\d{5,6}\-?\d{4}?)')
zipcode_exp2 = re.compile(r'\,?\s{,2}?([A-Z]{1,2}?\,?\s{,3}?\d{5,6})')
#zipcode_exp3 = re.compile(r'\,?\s{,2}?([a-z]{1,2}?\,?\s{,3}?\d{5,6})')
zipcode_exp4 = re.compile(r'\,?\s{,2}?([A-Z]{1,2}?[a-z]{1}?\,?\s{,3}?\d{5,6})')

'''
#this code used if zipcode contains full city name

zipcode_exp = re.compile(r'\,?\s{,2}?([A-Z a-z]+?\,?\s{,3}?\d{5,6}\-?\d{4}?)')

zipcode_exp2 = re.compile(r'\,?\s{,2}?([A-Z a-z]+?\,?\-?\s{,3}?\d{5,6})')  #modified 19th feb

#zipcode_exp3 = re.compile(r'\,?\s{,2}?([A-Z a-z]+?\,?\s{,3}?\d{5,6})')
zipcode_exp4 = re.compile(r'\,?\s{,2}?([A-Za-z]+?[a-z]{1}?\-?\,?\s{,3}?\d{5,6})')   #modified for zipcode for indian type zipcode. Added = "\-?"
'''

zipcode_regex_list = [zipcode_exp,zipcode_exp4,zipcode_exp2]

#regexpression lists
regex_list=[webexp2,webexp3,webexp4,webexp6,webexp7,webexp5]



file = open("selenium_blocks_inputs.txt","r")
obj = file.readlines()


if len(obj) == 0:
    print("The 'names_path_inputs' file is empty, please give some inputs \n")
    exit()

data_info = []
for line in obj: 
    line_info = line.split('|')
    data_info.append(line_info)
    

#for getting the inputs fields to get the available hrefs.
href_file = open("hrefs_path_input_selenium.txt","r")
href_obj = href_file.readlines()

href_data_info = []
for line in href_obj:
    href_data_info.append(line.split('|'))

#checks if all the elements of the list are identical
def allthesame(l):
    #return np.all(np.diff(l)==0)
    try:
        if len(set(l)) == 1:
            if l[0] == 'N/A':
                return True
            else:
                return False
        else:
            return False
    except:
        return False
        pass

if os.path.isdir("Text output folder(selenium)"):
    time.sleep(3)
    shutil.rmtree("Text output folder(selenium)")

time.sleep(2)
#for storing all the text file in a folder.
os.mkdir("Text output folder(selenium)") 


browser = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')

websites_numbers = len(data_info)

i = 0
i2 = 0
#accessing URL one by one
for url_info in data_info:
    
    website_add_list = []
    email_id_list = []
    phone_no_list = []
    final_name_list = []
    zipcode_list = []
    href_website_list = []
        
    #making the xpaths
    link = url_info[0]
    tag_info,attr_value = url_info[1].split('/') and url_info[1].split('==')
    tag_name,tag_attr = tag_info.split('/')
    
    second_extra_path_flag = 0
    if '$' in attr_value:
        attr_value, second_extra_path = attr_value.split('$')
        second_extra_path_flag = 1
        
    
    blocks_xpath = "//"+tag_name+"[@"+tag_attr+"='"+attr_value+"']"
    
    if second_extra_path_flag == 1:
        blocks_xpath = blocks_xpath + second_extra_path
    
    
    if '#yes' in url_info:
        href_extra_xpath = href_data_info[i2][0]
        i2 = i2+1
    
    from selenium.common.exceptions import InvalidSelectorException
    #accessing each links or URLs
    try:
        browser.get(link)
        '''
        #this line below is used to scroll down the webpage
        
        for scroll in range(0,20):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("no. ",scroll)
            time.sleep(3)
        '''
        blocks_list = browser.find_elements_by_xpath(blocks_xpath)
        print("try 1")

    except InvalidSelectorException:
        print("path in input file is wrong. please check it again..\n")
        break
    except:
        try:
            WebDriverWait(browser, 6).until(EC.alert_is_present)
            browser.switch_to.alert.accept()
            print("excp 1 - try 2")
        except:
            browser.switch_to.alert.accept()
            print("excp 2")

    while True:    
        time.sleep(3)
        blocks_list = browser.find_elements_by_xpath(blocks_xpath)
        print("waiting for the blocks..")
        #WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, blocks_xpath)))
        if blocks_list != []:
            print("got the blocks")
            break
    
    if '##yes' in url_info:
        #if the main datablocks are present inside the hrefs
        
        tag_info,attr_value = url_info[4].split('/') and url_info[4].split('=')
        tag_name,tag_attr = tag_info.split('/')
        
        blocks_xpath =  "//"+tag_name+"[@"+tag_attr+"='"+attr_value+"']"
        
        hrefs_links_list = []
        for url in blocks_list:
            hrefs_links_list.append(str(url.get_attribute('href')))
            
        if None in hrefs_links_list:
            hrefs_links_list = [var for var in hrefs_links_list if var != None ]
        
        b = 0
        hrefs_blocks_list = []
        plain_text_list = []
        for each_href_url in hrefs_links_list:
            try:
                browser.get(each_href_url)
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, blocks_xpath)))
                time.sleep(2)
                hrefs_blocks_list.append(browser.find_element_by_xpath(blocks_xpath))
                plain_text_list.append(browser.find_element_by_xpath(blocks_xpath).text)
                #print("got href plain text")
                
            except:
                plain_text_list.append("N/A")
                continue
            
            print("got the href blocks",b)
            b=b+1
            
        blocks_list = hrefs_blocks_list
        
    else:    
        plain_text_list = []
        for single_text in blocks_list[:5]:
            try:
                plain_text_list.append(single_text.text)    
            except:
                plain_text_list.append("N/A")
            
    div_count = 1
    for each_text in plain_text_list:
        
        try:
            WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'urlname')))
            urlname = browser.find_element_by_id('urlname').text
            link = urlname
        except:
            #print("pass")
            pass
        
        
        try:
            if '##yes' in url_info:
                browser.get(hrefs_links_list[div_count - 1])
        except:
            print("pass the href links")
            pass
        
        
        txt_split = each_text.split() and each_text.split("\n")
        
        #getting website and zipcode
        website_list = []
        final_zipcodes = []
        website_flag = 0
        zipcode_flag = 0
        for txt in txt_split:
            for expressn in regex_list:
                if '@' not in txt:
                    match_website = re.findall(expressn,txt)
                    if match_website:
                        for each_single_site in match_website:
                            if 'twitter.com' not in each_single_site and 'facebook.com' not in each_single_site and 'instagram.com' not in each_single_site:
                                if len(each_single_site) > 5:
                                    website_list.append(match_website[0])
                                    website_flag = 1
                            else:
                                website_flag = 0
                        break;
            for zipcode_exprsn in zipcode_regex_list:
                match_zipcode = re.findall(zipcode_exprsn,txt)
                if match_zipcode:
                    final_zipcodes.append(match_zipcode[0])
                    zipcode_flag = 1
                    break
                
        if zipcode_flag == 1:
            zipcode_list.append(final_zipcodes[0])
        else:
            zipcode_list.append("N/A")
        
                        

        #getting email
        match_email = re.findall(email_exp, each_text)
            
        email_id_flag = 0
        if match_email:
            final_email = []
            for each_email in match_email:
                if "www." not in each_email or "@" in each_email:
                    final_email.append(each_email)
                    email_id_flag = 1
            if email_id_flag == 1:
                email_id_list.append(final_email[0])
            else:
                email_id_list.append("N/A")
        else:
            email_id_list.append("N/A")    
        
        #getting phone numbers
        match_contact = []
        for mob_expr in mobile_regex_list:
            match_contact_1 = re.findall(mob_expr, each_text)
            match_contact = match_contact_1 + match_contact
                
        final_contact = []

        for element in match_contact:
            if len(list(element)) > 7:
                final_contact.append(element.strip())
            
        if each_text == '':
            phone_no_list.append("N/A")
        elif match_contact or (match_contact == []):
            try:
                if ',' not in final_contact[0] and len(final_contact[0]) > 7:
                    zip_compare_flag = 0
                    for zip_compare in zipcode_list:
                        if final_contact[0] in zip_compare:
                            zip_compare_flag = 1
                            try:
                                if final_contact[1]:
                                    print("yes, got 2nd contact")
                                    final_contact[0] = final_contact[1]
                                    zip_compare_flag = 0
                            except IndexError:
                                pass
                            break
                    if zip_compare_flag == 0:
                        phone_no_list.append(list(unique_everseen(final_contact)))
                        #phone_no_list.append(final_contact[0])
                    else:
                        phone_no_list.append("N/A")
                else:
                    try:
                        phone_no_list.append(list(unique_everseen(final_contact)))
                        #phone_no_list.append(final_contact[0])
                    except:
                        phone_no_list.append("N/A")
            except:
                if final_contact == []:
                    phone_no_list.append("N/A")
                else:
                    phone_no_list.append(final_contact)
        
        if website_flag == 0:
            website_add_list.append("N/A")
        elif website_list[0] in phone_no_list:
            website_add_list.append("N/A")
        else:
            website_add_list.append(website_list[0])
                
        
        #getting names
        if "##yes" in url_info:
            name_xpath = blocks_xpath + url_info[2]
        else:
            name_xpath = blocks_xpath +"["+ str(div_count) +"]"+ url_info[2]
        
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, name_xpath)))
            name_element = browser.find_element_by_xpath(name_xpath)
            
            if name_element.text == '':
                final_name_list.append("N/A")
            else:
                final_name_list.append(name_element.text.replace('\n',' '))
        except:
            print("in except of name")
            final_name_list.append("N/A")
        
        #getting hrefs from the datablocks
        if '#yes' in url_info:
            if '##yes' in url_info:
                href_xpath = blocks_xpath + href_extra_xpath
            else:
                href_xpath = blocks_xpath +"["+ str(div_count) +"]"+ href_extra_xpath
            try:
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, href_xpath)))
                href_element = browser.find_element_by_xpath(href_xpath).get_attribute('href')
                if href_element == '' or href_element == None:
                    href_website_list.append("N/A")
                elif '@' in href_element:
                        email_href_value = re.findall(email_exp, href_element)
                        href_website_list.append(email_href_value[0])
                else:
                    href_website_list.append(href_element)
            except:
                href_website_list.append("N/A")
        
        print("next div",div_count)
                    
        div_count = div_count+1
        
        
    #writing the data in the output text file in a foder named as  "Text output folder(selenium)".
    fp = open("Text output folder(selenium)/block_"+str(i)+"_info.txt","w")
        
    try:
        
        fp.write(link+"\n\n")
            
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
        
        if '#yes' in url_info:
            if allthesame(href_website_list) == True:
                href_website_same = "yes"
            else:
                title_line = title_line + "|OTHER INFO(website or mail-id)"
                href_website_same = "no"
        
        fp.write(title_line+"\n\n")
            
        line_num = 0
        while line_num < len(plain_text_list):  #changed(blocks list into plain text list)
            try:
                line = ''
                    
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
                if '#yes' in url_info:
                    if href_website_same != "yes":
                        line = line +"|"+ str(href_website_list[line_num])
                
                line = line +"\n"    
            except:
                print("Errroorrrrrrrr 1\n")
                
            fp.write(str(line.encode('ascii', 'ignore').decode('ascii')))
            line_num = line_num+1
        
    except:
        print("errror  2  \n\n")
        
    finally:
        fp.close()
    
    i = i+1
        

browser.quit()


#import subprocess
#time.sleep(10)
#subprocess.call(["shutdown", "/s"])


#END OF FILE



             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             