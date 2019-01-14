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