import xml.etree.cElementTree as ET
import urllib2
import sys
import imp
import os
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def str2bool(v):
	return v.lower() in ("true", "True", "y", "Y")
def unescapeurl(v):
	return v.replace(" ", "%20")
def textlayout(text, color):
	return color + text + bcolors.ENDC;
def mainisfrozen():
   return (hasattr(sys, "frozen") or
           hasattr(sys, "importers")
           or imp.is_frozen("__main__"))
def getmaindir():
   if mainisfrozen():
       return os.path.dirname(sys.executable)
   return os.path.dirname(sys.argv[0])

filepath = getmaindir()+"/config.txt";
if not os.path.exists(filepath):
	print textlayout("Sorry, there is no config.txt to get your API key, try creating one in https://developers.google.com/places/web-service/ and placing it in config.txt next to *.py file", bcolors.FAIL + bcolors.BOLD)
	quit()

file = open(filepath, "r") 
apikey = file.readline()

typeOfEstablishment = raw_input( textlayout("What kind of establishment are you searching for?\n", bcolors.BOLD) )
while (typeOfEstablishment == ""):
	typeOfEstablishment = raw_input( textlayout("Sorry, that's not a valid input. What do you want to search for?\n", bcolors.BOLD) )

locationToSearch = raw_input( textlayout("Ok, cool. Where do you want to find " + typeOfEstablishment + "?\n", bcolors.BOLD))
while (locationToSearch == ""):
	locationToSearch = raw_input( textlayout("Sorry, that's not a valid input. Where do you want to find " + typeOfEstablishment + "?\n", bcolors.BOLD))

print textlayout("Awesome, I will find " + typeOfEstablishment + " in " + locationToSearch + "!", bcolors.BOLD)

url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?query=" + unescapeurl(typeOfEstablishment) + "+in+" + unescapeurl(locationToSearch) + "&key=" + apikey

tree = ET.ElementTree(file=urllib2.urlopen(url))
root = tree.getroot()

if(root[0].text == "REQUEST_DENIED"):
	print textlayout("Sorry, there is something wrong with your API key, try creating one in https://developers.google.com/places/web-service/ and placing it in config.txt", bcolors.FAIL + bcolors.BOLD)
	quit()
if(root[0].text == "OVER_QUERY_LIMIT"):
	print textlayout("Sorry, you requested too many times, try creating another API key and change in config.txt", bcolors.FAIL + bcolors.BOLD)
	quit()

results = []
index = 0;

for child in root.iter("result"):
	print textlayout(str(index), bcolors.UNDERLINE) + textlayout(": " + child.find('name').text, bcolors.UNDERLINE)
	index += 1;

if(index == 0):
	print textlayout("Sorry, I could not find anything for " + typeOfEstablishment + " in " + locationToSearch, bcolors.BOLD)
	quit()

showmoreinfo = True;
while (showmoreinfo):
	establishmentIndex = raw_input( textlayout("Type the index (0 to " + str((index-1)) + ") of the establishment you want to know more about\n", bcolors.BOLD))

	while not establishmentIndex.isdigit() or (int(establishmentIndex) >= index) or (int(establishmentIndex) < 0):
		establishmentIndex = raw_input( textlayout("Sorry, that's not a valid input. Type the index (0 to " + str((index-1)) + ") of the establishment you want to know more about\n", bcolors.BOLD))

	print textlayout("Showing more information about " + bcolors.UNDERLINE + root[int(establishmentIndex) + 1].find('name').text, bcolors.BOLD)
	if root[int(establishmentIndex) + 1].find('formatted_address') is not None: print textlayout("	Address: " + root[int(establishmentIndex) + 1].find('formatted_address').text, bcolors.BOLD)
	if root[int(establishmentIndex) + 1].find('rating') is not None: print textlayout("	Rating in stars (1 to 5): " + root[int(establishmentIndex) + 1].find('rating').text, bcolors.BOLD)
	if root[int(establishmentIndex) + 1].find('opening_hours') is not None: print textlayout("	It is open now!", bcolors.FAIL + bcolors.BOLD) if str2bool(root[int(establishmentIndex) + 1].find('opening_hours').text) else textlayout("	It is closed now!", bcolors.FAIL + bcolors.BOLD)

	userinput = raw_input( textlayout("Do you want to get information from others establishments? (y/n)\n", bcolors.BOLD) );
	while not userinput == "n" and not userinput == "y":
		userinput = raw_input( textlayout("Invalid input. Do you want to get information from others establishments? (y/n)\n", bcolors.BOLD) );
	showmoreinfo = str2bool(userinput);

quit()



