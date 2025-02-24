# Scribd-Bypass
A little python tool that allows the user to download the pages of a book from Scribd's webpage and converts them into a pdf bypassing the requirements of either subscribing to the service (even with a 30 days free trial) or to upload files to gain access to the whole library.

# How it works

## Folder Selection 
The program asks the user where to save the images of the pages to stitch, it can be either a pre-existing folder or a new folder that the program creates in the present working directory.
If the user choses the folder it need to be spcecified with the full path (i.e. /home/"user_name"/"folder" on Unix systemx and C:\Users\"user_name"\Desktop\"folder"), in case the folder doesn't exist the program will notify the user and prompt again to indicate a folder.

## Source grabbing
The useer is asked to paste the url from where to collect the pages the program then proceses it through a request function effectively pulling the whole html web page and storing it in a webpage_source.txt file.

## Text processing
The webpage_source.txt file is processed eliminating everything that is not a link to the pages doing a bit of clean up and fixing to get at the end a nice and ordered list of all the urls to the page images putting them in the link_list.txt file.

## Image Grabbing
The program at this point recursevely goes over all the links in the previous file and pulls all the images one by one in the subfolder /pages_images (\pages_images) this proces can take a hot second dempending on the quantity of pages that file has so let it run in the background if it's a very big book (for reference it takes on an average laptop around 20 seconds to grab 530 pages).

!!!
NOTE: sometimes the pages are saved on Scribd as different types from one another for some reason and that breaks the program so to speak, simply put it will say that the download for that image has failed, i'm currently trying to figure out a solution for this when i have time but if you want to add a fix branch off and i'll pull in the addition at some point.
!!!

## Stitching
All of the images are then stitched togheter into a pdf that gets saved as output.pdf in the same subfolder of all the images.

Voila' you have a freshly baked pdf now, enjoy!
