######################################################################## About

#Written by bliz937@gmail.com - www.bliz.co.za
#Last edit: 4 April 2013
#This script has been tested on:
## Ubuntu 12.10 (64 bit), Python 3.2
## Solaris 10 (SunOS 5), Python3
#It's purpose is to change the desktop image every x seconds by editing Gnome's setting with gsettings (Gnome ver 3) or gconftool (Gnome ver 2)

######################################################################## Config

### Config, you have to modify the below. ###

#path to where your images are located (NB)
PATH2IMAGES = "/host/Users/Bliz/Pictures/Wallpapers"

#time that you'd like to wait before the background changes images (in seconds)
time2Wait = 1

#whether to choose the images at random or to choose them in order
#True: choose images randomly
#False: choose images as they are read in
choseRandom = False

#number of images (name) to be kept in memory (before scanning folder again) (ONLY FOR RANDOM = True)
stop = 20

######################################################################## Imports

from os import system, listdir, rename, popen 	#system commands, ls, rename file, read in system command
from sys import exit				#quit script
from time import sleep 				#holds script till next image
from platform import system as osType 		#detects OS type
from random import randint as ran 		#generate random int

######################################################################## OS related functions

def checkOS():
	os = osType()
	if(os == 'Linux' or os == 'SunOS'):
		return
	print("Your OS/Platform is not supported!")
	exit()

######################################################################## Desktop background related functions

def renamePic(pic): #Replaces any spacing in image name with '-'
	if (' ' in pic):
		pic1 = pic.replace(' ', '-')
		rename(PATH2IMAGES+pic, "/"+PATH2IMAGES+pic1)
		#print("renamed "+pic+" to "+pic1)
		pic = pic1

	return (pic)

def getCommand(): #Gets command to execute depending on Gnome version
	version = popen("gnome-session --version").readline()
	version = int(version[version.rfind('session')+8])

	if(version == 2):
		#print("Gnome ver 2 detected")
		if(popen("which gconftool").readline() != ''):
			return "gconftool --set --type=string /desktop/gnome/background/picture_filename "
		elif(popen("which gconftool-2").readline() != ''):
			return "gconftool-2 --set --type=string /desktop/gnome/background/picture_filename "
		print("gconftool or gconftool-2 not found!")
		exit()

	elif (version == 3):
		#print("Gnome ver 3 detected")
		return "gsettings set org.gnome.desktop.background picture-uri file://"

	print("only tested for gnome version 2 & gnome version 3!\nYou have version "+version)
	exit()
	
def executeRandom(command, PATH2IMAGES, TIME2WAIT, stop): #Script execution: Random
	pic = []
	while(True):
		array = listdir(PATH2IMAGES)

		if(stop > len(array)):
			stop = len(array)
		
		for i in range(stop):
			pic.append(array.pop(ran(0,len(array) - 1)))

		array = None

		for i in range(stop):
			#print("Pic: >>>"+pic[0]+"<<<")
			system(command+PATH2IMAGES+renamePic(pic.pop(0)))
			sleep(TIME2WAIT)

def executeProcedural(command, PATH2IMAGES, TIME2WAIT):
	while(True):
		array = listdir(PATH2IMAGES)

		stop = len(array)
		for i in range(stop):			
			system(command+PATH2IMAGES+renamePic(array.pop(0)))
			#print("Pic: "+">>>"+i+"<<<")
			sleep(TIME2WAIT)
		
		array = None
		

######################################################################## Execution of script code

checkOS() #Checks whether the platform is supported by script
#print("OS checked")

if (PATH2IMAGES[0] != '/'):
	PATH2IMAGES = '/'+PATH2IMAGES
if(PATH2IMAGES[-1] != '/'):
	PATH2IMAGES = PATH2IMAGES + '/'

command = getCommand() #Changed later on in getCommand function
#print("Command gotten: "+command+"\nRandom: "+str(choseRandom))

if(choseRandom):
	executeRandom(command, PATH2IMAGES, time2Wait, stop) #changes the images at random
else:
	executeProcedural(command, PATH2IMAGES, time2Wait)
	


