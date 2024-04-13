import os
import pytesseract
import numpy as np
import cv2
import pandas as pd
import regex as re
import thefuzz
from thefuzz import process
import string
import re


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#Read the images, change this variable for the folder of images you want to use
filename = "img1_folder"

def read_text(filename):
    #Read the image
    img  = cv2.imread(filename)

    #Resize the img
    img = cv2.resize(img, dsize= (1500,1500), interpolation= cv2.INTER_AREA)
    ##Grayscale/ Binarization.
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Setting up adaptive thresholding
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15,10)

    #Noise Reduction. 
    kernel = np.ones((1,1), np.uint8)
    img1 = cv2.dilate(img, kernel, iterations=1)
    img1 = cv2.erode(img1, kernel, iterations=1)
    img1= cv2.morphologyEx(img1, cv2.MORPH_CLOSE, kernel)
    img1 = cv2.medianBlur(img1, 3)
    #The images are certainly better but the font gets more illegible. 
    
    #Next step is to thin font.
    img1 = cv2.bitwise_not(img1)
    kernel = np.ones( (2,2),np.uint8)
    img1 = cv2.dilate(img1, kernel, iterations=1)
    kernel = np.ones((3,3),np.uint8)
    img1 = cv2.erode(img1, kernel, iterations=1)
    img1 = cv2.bitwise_not(img1)

    #cv2.imshow("Image", img1)
    #cv2.waitKey(0)
    text = pytesseract.image_to_string(img1,config = '--psm 6')

    return text
'''
df = pd.read_csv("muse_v3.csv")
track_names = df['track']
'''

def track_finder(text):
    import string
    translator = str.maketrans('', '', string.punctuation) 
    text = text.translate(translator)
    text = text.split(" ")
    for idx, char in enumerate(text):
        ##Want to iterate through the string until I find the first number
        if char.isdigit():
            if int(char)==1:
                point = idx
                break
    #print(len(text),idx)
    #for char in text[point:]:
   # print(text[point:])
    words=[]
    names = []
    for x in text[point:]:
            x = x.strip(" ‘,.:;'")
            if x.isdigit():
                names.append(words)
                words = []
            else:
                words.append(x)
    if words:
        names.append(words)

    #Building up a dataset of real words, then going to fuzzy match each word to find the ideal match. This is a way of cleaning the misread words
    file1= open("words.txt")
    text1 = file1.read()
    words1 = text1.splitlines()
    
    #for name in names:
       # for x in range(len(name)):
          #  name[x] = process.extractOne(name[x],words1)[0].lower()
    
    ##Need to iterate through each name, joining them all together, 
    
    tracks = []
    for name in names:
        string =""
        for x in range(len(name)):
            #print(name)
            string += " " + name[x] 
        tracks.append(string)
    return tracks



numbers = re.compile(r'(\d+)')
def numericalSort(value):
    '''Helper key function so that the files are read in the correct order.'''
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def file_reader(files):
    tracks = []
    disc_number =[] 
    sortedfiles = sorted(os.listdir(files), key = numericalSort)
    for idx, filename in enumerate(sortedfiles):
        f = os.path.join(files, filename)
      # checking if it is a file
        if os.path.isfile(f):
            text = read_text(f)
            tracks.extend(track_finder(text))
            for i in range(len(track_finder(text))):
                 disc_number.append(idx+7)        
                    
    return tracks, disc_number


def closest_match(string,df):
    #Next function is a fuzzy  matching function that iterates through dataset to try and find the closest match and outputs this as a string.
    closest_match = process.extractOne(string, df['Song Names'], score_cutoff=85)
    #print(closest_match)
    if closest_match:
        disc_number = df.iloc[closest_match[2]]['Disc Number']
        return ("The closest match that could be found was: " + closest_match[0] + ". At Disc Number:" + str(disc_number))
    else:
        return "Could not find a close enough match"

'''This code here is what creates the csv file. Uncommenting the following lines will provide a new csv file.'''

#tracks, disc_number =file_reader(filename)
#df = pd.DataFrame({'Song Names': tracks, 'Disc Number':disc_number})
#df.to_csv('out.csv', index =False)