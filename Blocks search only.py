# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on 12-Dec-2018

@author: %(Shekhar joshi)s

#Application : Blocks Search
 
#Description : Searches for the blocks in the website.

#Updated    : 12-Dec-2018

#Updater    : Shekhar Joshi
"""



import re
expslashn=re.compile(r'^\n')

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen



#url contents


#browser file to be accessed
#browser = webdriver.Chrome('C:\ProgramData\Anaconda3\chromedriver_win32\chromedriver.exe')

file = open("Blocks_url.txt","r")
x=file.readlines()

link_with_tags=[]
links_only=[]
final_links=[]
final=[]
for p in x:
    p.replace('\n',"")
    links_only=p.split('|')
    final_tags=links_only[1].split("/")
    final=[final_tags[0]]+final_tags[1].split("=")
    link_with_tags.append([links_only[0]]+final)
    #link_with_tags[0][1].split('/')
    
    
#To remove any UCS character present in the string. we used the code given below.
    emoji_pattern = re.compile("["
                                 u"\U0001F600-\U0001F64F"  # emoticons
                                 u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                 u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                 u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                 u"\U00002702-\U000027B0"
                                 u"\U000024C2-\U0001F251"
                                 "]+", flags=re.UNICODE)


    
for link in link_with_tags:    
    
#    linkx="https://www.wineroad.com/wineries/?winery_name=a&region=&wine_type=&amenity="
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    req = Request(str(link[0]), headers=hdr)
    page = urlopen(req)        
    #text=linkx.text
    soup = BeautifulSoup(page)
    #soup = BeautifulSoup(linkx.content, "html.parser")
    #soup = BeautifulSoup(linkx.content, 'html.parser')
    #all_blocks=soup.find('div',{'class':'listing equalheight '})
    #all_blocks=soup.find_all(""+link[1]+"",{str(link[2]):str(link[3])}) #str(link[3])})
    
    all_blocks=soup.find_all(""+link[1]+"",{str(link[2]):re.compile(r'^'+str(link[3])+'')})
    
    #all_blocks=soup.find_all(""+link[1]+"",{'class':""+link[3]+""})
    
    ip = open("updated.txt","a")
    
    fp = open("blocks"+str(link_with_tags.index(link))+".html","w")
    updatedline=str(str(link[0])+'|'+'Completed'+'|'+str(len(all_blocks))+'\n')
    ip.write(updatedline)
    i = 0
    for line_num in all_blocks:
        try:
            if i == 0:
                line = "\n<hr/><div id='datablock'>"+str(line_num)+'</div>\n\n<hr/>\n'
                i=i+1
            else:    
                line = "<div id='datablock'>"+str(line_num)+'</div>\n\n<hr/>\n'
            #line_num = line_num+1
            fp.write(line)
        except:
            updatedline=str(link[0])+'|'+'Error'+'0'+'\n'
            line = "None"+'\n\n<hr/>\n'
            fp.write(line)
    
    detail= open("detail.txt","a")
    details=str(link[0]+"|"+link[1]+"/"+link[2]+"="+link[3]+"\n")
    
    detail.write(details)
    
    detail.close()
    fp.close()
    ip.close()
