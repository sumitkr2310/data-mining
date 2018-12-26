# data-mining
Extracting required information from list of URLs taking as an input.

NOTE :

==> first run "blocks_search_only.py file" then run "extract_production.py" file.<==

=====================readme for blocks search.py file=======================================================

Getting a Datablocks from the information websites.

like members of wineries with their own information.

with the below information (not neccessarily it should be in the below pattern)

{ name
  Address
  state and zipcode
  Contact
  email address
  website }


here there is an input file(.txt) which contains the url and tag with attribute and attribute value.

sample : { "http://granvillenychamber.com/category/all-businesses/|article/itemprop=blogPost|" }

the input file is divided by the '|' delimitters 

Here as you see the url is : "http://granvillenychamber.com/category/all-businesses/"
		    tag is : "article"
	  tag attribute is : "itemprop"
	 attribute value is : "blogPost"

IMPORTANT!!!!  --> the tags can be anything. 
		   div,id,tr,td,article,span,a,li,ul etc..

	       --> and their attribute also may vary
	           class,id,name,item, even you can give the font sizes.       {IMPORTANT!! here the attribute should be same for all the blocks then only it will give you all the blocks you need}


The updated file(.txt) contains the updated websites list with number of blocks found.

The details file(.txt) will contain the detail of the each url with the tags and names so that if we need to get the data from the same website again we need not to goto website and inspect and see for the id or class names and everything.

Just run a single url with input file and see the results.

==========================readme for extract_production.py file============================================

Getting a information from Datablocks.

Like members of wineries with their own information.

with the below information (not necessarily it should be in the below pattern)

{ name,
  Contact no.,
  email address,
  website }

  
IMPORTANT!!  
Before you proceed, go to the link mentioned below and download the driver according to your OS.(Windows,Linux,MacOS) 

link : https://chromedriver.storage.googleapis.com/index.html?path=2.43/

Create a folder in C drive as "chromedriver_win32"(without quotes), and paste the downloaded (.exe) file to this folder. (Recommended the "chromedriver_win32" folder should be created in C drive only.)

Run(without quotes) the below command in cmd prompt and wait till the installation procedure is done:
"pip install selenium"


Here there is an "blocks_analysis_inputs.txt" file which contains only tags with attribute and attribute value.


This "blocks_analysis_inputs.txt" is used for extracting the Names part only. so it means if there are no Names present in the URL then put "NA" in the line.

The synchronization of both the .txt files should be in their respective order.

for example:
			if there are 5 blocks there should be five lines in the blocks_analysis_inputs.txt file with their respective pattern(i.e, tag path to get the names).

for example, for the URL mentioned below, we want all the names, website, contact number, and email ids:

But we will access these info from the blocks0.html file(present inside the Output folder in C drive).

http://granvillenychamber.com/category/all-businesses/


The inputs in blocks_analysis_inputs.txt file should be like this(without quotes): "/article/header/h2|". this input is acting as a path to reach out to the names part inside the website. So give this path accordingly after analyzing the "blocks.html" (present in Output folder) file.


But if path contains table tag in it then the pattern should be like this : "/table/tbody/tr|/td[2]|". Here the path before the first pipe symbol will be same as written but the path after first pipe symbol should be given according to the requirement i.e., in which "td" tag the name exists.

for example:
if the name exists at 1st "td" tag then path should be like this => /table/tbody/tr|/td[1]|

if the name exists at 2nd "td" tag then path should be like this => /table/tbody/tr|/td[2]|

if the name exists at 3rd "td" tag then path should be like this => /table/tbody/tr|/td[3]|

NOTE : The number of lines written in the "blocks_analysis_inputs.txt" file should be equal to the number of html files present in the "Output folder".

The input file is divided by the '|' delimiters.

Here as you see for the url: "http://granvillenychamber.com/category/all-businesses/"
		    first tag 	: "article"
			second tag	: "header"
			third tag	: "h2"

IMPORTANT!!!!  --> 	the tags can be anything. 
					div,id,tr,td,article,span,a,li,ul etc..

IMPORTANT!! here the attribute should be same for all the blocks then only it will give you the names you need

After running the program, you will get the outputs in a folder named as "Text output folder". This folder contains all .txt files i.e, for each blocks.html file in "Output folder" there is blocks_info.txt file in "Text output folder".
or we can also say that number of files present in "Output folder" must be equal to the number of files present in "Text output folder".
