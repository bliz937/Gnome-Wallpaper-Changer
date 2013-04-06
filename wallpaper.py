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
PATH2IMAGES = "/export/home/second/shevchenko/Desktop/ME/"

#time that you'd like to wait before the background changes images (in seconds)
Time2Wait = 15

#number of images (name) to be kept in memory (before scanning folder again)
stop = 20

#whether to choose the images at random or to choose them in order
#True: choose images randomly
#False: choose images as they are read in
executeRandom = True

######################################################################## Imports

from os import system, listdir, rename, popen 	#system commands, ls, rename file, read in system command
from sys import exit				#quit script
from time import sleep 				#holds script till next image
from platform import system as osType 		#detects OS type
if(executeRandom):
	from random import randint as ran 	#generate random int

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
	version = int(popen("gnome-session --version").readline()[14])
	if(version == 2):
		return "gconftool-2 --set --type=string /desktop/gnome/background/picture_filename "
	elif (version == 3):
		return "gsettings set org.gnome.desktop.background picture-uri file:///"
	
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
			#print(">>>"+pic[0]+"<<<")
			system(command+PATH2IMAGES+renamePic(pic.pop(0)))
			sleep(Time2Wait)

def executeProcedural(command, PATH2IMAGES, TIME2WAIT):
	while(True):
		array = listdir(PATH2IMAGES)

		for i in array:
			system(command+PATH2IMAGES+renamePic(i))
		
		array = None
		

######################################################################## Execution of script code

checkOS() #Checks whether the platform is supported by script

if (PATH2IMAGES[0] != '/'):
	PATH2IMAGES = '/'+PATH2IMAGES

command = getCommand() #Changed later on in getCommand function

if(executeRandom):
	executeRandom(command, PATH2IMAGES, TIME2WAIT, stop) #changes the images at random
else:
	executeProcedural(command, PATH2IMAGES, TIME2WAIT, stop)
	


