import requests
import json
import os
import sys
import matplotlib.pyplot as plt
import easyocr
import cv2
import numpy as np
import time



IMAGE_PATH=r"C:\JAVASCRIPT\my-website\uploads\web_reciept.jpg"
reader = easyocr.Reader(["en"],gpu=False)

#ocr function
def ocr_funct(in_file_name):
    result=reader.readtext(in_file_name)#runs the ocr on image
    food_names=[]
    for item in result:
        is_number=False
        for i in range(len(item[1])):
            if i<3:
                if item[1][i]>":":
                    break
            if (i+1==len(item[1])):
                is_number=True
        if not is_number:#we only want the names of the foods
            food_names.append(item[1])
    return food_names
    

#categorizer function
def categorizer_function(food_names_list):
    item_category="unknown"
    vegetables=["CARROTS","PICKLES","SQUASH","LETTUCE","SPINACH","ONION","GREEN BELL","CUCUMBER","CELERY","BROCCOLI","CAULIFLOWER","CABBAGE","KALE","COLLARD","TURNIP","RADISH","BEET","ARTICHOKE","ASPARAGUS","GARLIC","GINGER","POTATO","SWEET POTATO","YAM","TARO","JICAMA","PARSNIP","RUTABAGA","WATER CHESTNUT","WATERCRESS","ZUCCHINI","CHAYOTE","OKRA","SWEET PEPPER","CHILI PEPPER","JALAPENO","HABANERO","CHERRY PEPPER","BELL PEPPER","TOMATO","AVOCADO","OLIVE","EGGPLANT","PUMPKIN","CORN","SWEET CORN","PEAS","SNOW PEAS","SUGAR SNAP PEAS","GREEN BEANS","GREEN BEAN"]
    fruits=["TOMATO","APPLE","BANANA","BERRY","STRAWBERRY","BLUEBERRY","RASPBERRY","BLACKBERRY","CHERRY","GRAPE","GRAPEFRUIT","LEMON","LIME","ORANGE","CLEMENTINE","TANGERINE","PEACH","NECTARINE","PLUM","APRICOT","PINEAPPLE","MANGO","PAPAYA","GUAVA","KIWI","FIG","DATE","WATERMELON","CANTALOUPE","HONEYDEW","HONEYDEW MELON","CRANBERRY","POMEGRANATE"]
    grain=["OAT","WHEAT","GRAIN","PITA"]
    nuts=["PEANUT","ALMOND","CASHEW"]
    dairy=["MILK","YOGURT","EGG","CREAM","BUTTER","CHEESE"]
    meat=["CHICKEN","BEEF","PORK","Salmon","TURKEY","FISH","TILAPIA","TUNA","SHRIMP","LOBSTER","CRAB","CLAM","MUSSEL","OYSTER"]
    dessert=["COOKIE","PIE","ICE","BAR"]


    category_list=[vegetables,fruits,grain,nuts,meat,dairy,dessert]

    days_remaining=[13,20,60,80,4,25,75]
    #create list of zeros
    category_sums=[0,0,0,0,0,0,0]
    category_names=["vegetables","fruits","grain","nuts","meat","dairy","dessert"]
    

   
    exp_temp=0
    for food_name in food_names_list:
        i=0
        for category in category_list:
            for food in category:
                #check if food is in category upper or lowecase
                if food.upper() in food_name:
                    item_category=category_names[i]
                    category_sums[i]+=1
                    exp_temp=days_remaining[i]
                if item_category=="unknown":
                    item_category=="MISC"
                    exp_temp=90
            i+=1
    print(category_sums)
    category_used_names=[]
    #if category has zero sum then make the name blank
    for i in range(len(category_sums)):
        if category_sums[i]==0:
            category_used_names.append("")
        else:
            category_used_names.append(category_names[i])
    print(category_used_names)
    plt.pie(category_sums,labels=category_used_names)

    plt.savefig(r"C:\JAVASCRIPT\my-website\graph-dir\graph.png")
    plt.clf()


#new file checker function
def new_file_checker(directory):
    global old_files
    new_files=[]
    current_files=os.listdir(directory)
    for item in current_files:
        if item not in old_files:
            new_files.append(item)
    old_files=current_files
    return new_files



#main function
def main():
    current_files=[]
    file_que=[]
    directory=r"C:\JAVASCRIPT\my-website\uploads"
    global old_files
    old_files=os.listdir(directory)
    while(True):
        file_que+=new_file_checker(directory)
        if len(file_que)>0:
            print(file_que[0])
            food_names=ocr_funct(directory+"\\"+str(file_que[0]))
            categorizer_function(food_names)
            file_que.pop(0)
        time.sleep(0.1)

old_files=[]
main()

