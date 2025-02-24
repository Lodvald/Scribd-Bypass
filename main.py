import os
import subprocess
import sys

import requests
from PIL import Image

#Asks for the user permission before installing the required dependencies or quitting depending on the decision
def check_and_install():
    required = ["requests", "pillow"]
    missing = [pkg for pkg in required if not is_installed(pkg)]

    if missing:
        print(f"The following required python libraries are missing: {', '.join(missing)}")
        choice = input("Would you like to install them? (y/n): ").strip().lower()

        if choice == "y":
            for package in missing:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("All dependencies installed successfully!")
    else:
        print("Dependencies are required to run the program. Exiting.")
        sys.exit(1) #This should exit without errors statuses



#Cheks that the required libraries are installed for the program to work
def is_installed(package):
    try:
        __import__(package)
        return True
    except ImportError:
        return False



#Allows the user to either use a pre-existing folder to save images
#and build the pdf or lets the program create one in the pwd :)
def folder_selection():
    intro_menu = """Before we make your new pdf choose one of the following options:
     1. Choose an already existing folder
     2. Create a new folder"""

    print(intro_menu)

    while True:
        try:
            choice = int(input(">"))
            if choice not in [1, 2]:
                raise ValueError
            break
        except ValueError:
            print("You need to enter a number (1 or 2)!")

    if choice == 1:
        folder_path = input("Input the path of the folder where to create the pdf: ")
        if not os.path.isdir(folder_path):
            print("The path to the folder is not right, check and retry")
            return folder_selection()
    elif choice == 2:
        pwd = os.getcwd()
        folder_path = os.path.join(pwd, "/Pdf_build")
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")

    os.chdir(folder_path)



#I need to add a method that requires the url of the page and gets the actual html file
#off of it to then strip it of everything that is not the links to the images of the pages
def page_collector(url):
    source = requests.get(url)
    if source.status_code == 200:
        with open("webpage_source.txt", "w", encoding="utf-8") as file:
            file.write(source.text)
            print("Webpage source saved successfully!")



#This method deletes everything that is not a link to the images in the source code
#then edits the urls so that they actually point to the images of the pages themselves
# contentUrl: "https://html.scribdassets.com/978dg79g7/pages/1-9s7jviulhl3j5.jsonp"
def link_chain_builder():
    keyword = "contentUrl: \""
    with open("webpage_source.txt", "r", encoding="utf-8") as inputfile, open("link_list.txt", "w", encoding="utf-8") as outputfile:
        for line in inputfile:
            if line.strip().startswith(keyword):
                outputfile.write(line)

    with open("link_list.txt", "r", encoding="utf-8") as target:
        lines = target.readlines()

    with open("link_list.txt", "w", encoding="utf-8") as final:
        for line in lines:
            line = line.replace("contentUrl: \"", "")
            line = line.replace("pages", "images")
            line = line.replace("jsonp", "jpg")
            line = line.replace("\"", "")
            final.write(line)


#Downloads all the images using the list of links that has been processed before
def image_downloader():
    os.makedirs("pages_images", exist_ok=True)
    with open("link_list.txt", "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file if line.strip()]

    image_paths = []
    for i, url in enumerate(urls):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                img_path = os.path.join("pages_images", f'image_{i + 1}.jpg')
                with open(img_path, 'wb') as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                image_paths.append(img_path)
                print(f'Downloaded: {img_path}')
            else:
                print(f'Failed to download {url}')
        except Exception as e:
            print(f'Error downloading {url}: {e}')
    return image_paths


#Converts the images to a pdf, to be honest i'm not 100% sure of how this works but i'll figure it out
def images_to_pdf():
    path = image_downloader()
    if  not path:
        print("No images to convert!")
        return

    images = [Image.open(img).convert("RGB") for img in path]
    pdf_path = os.path.join(os.path.dirname(path[0]), "output.pdf")
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f'PDF saved as: {pdf_path}')



if __name__ == "__main__":
    check_and_install()
    folder_selection()
    page_collector(input("Paste the link to the Scribd page: "))
    link_chain_builder()
    images_to_pdf()