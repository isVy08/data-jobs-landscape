#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 20:24:21 2020

@author: vyvo
"""

import time
import re
import requests 
import pandas as pd 
from selenium import webdriver
from bs4 import BeautifulSoup


pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',500)

#Define functions 
def load_bottom(driver,link):
    driver.get(link)
    SCROLL_PAUSE_TIME = 1
    # Check if infinite loading or "see more" button 
    last_height = driver.execute_script("return document.body.scrollHeight") #get scrool height
    try: 
        while True: 
            button = driver.find_element_by_class_name("see-more-jobs")
            button.click()
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    except:
        while True: 
        # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page 
            time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


def basic_info(d, driver):
    soup = BeautifulSoup(driver.page_source, "lxml")
    jobs = soup.find_all('li',class_=re.compile('result-card'))
    try:
        for ad in jobs:
            d['id'].append(ad.attrs['data-id'])
            d['link'].append(ad.find('a').get('href'))
            d['title'].append(ad.find('h3').get_text())
            d['company'].append(ad.find('h4').get_text())
            d['location'].append(ad.find_all("span",class_="job-result-card__location")[0].get_text())
            d['list_time'].append(ad.find_all("time")[0].attrs['datetime'])
    except: pass 
    return d


def detail_info(link_list):
    global d
    d = {'description':[],'exp_level':[],'job_type':[],'job_func':[],'industry':[],'link':[]}
    for lk in link_list:
        result = requests.get(lk)
        src = BeautifulSoup(result.content,"lxml") 
        print(link_list.index(lk),end='---')
        d['link'].append(lk)
        try:
            d['description'].append(src.find_all("div",class_=re.compile("text description"))[0])
        except: 
            d['description'].append(0)
        
        criteria = src.find_all("li",class_="job-criteria__item")
        try:
            d['exp_level'].append(criteria[0].find('span').get_text()) #Seniority level 
        except:
            d['exp_level'].append(0)
        try:
            d['job_type'].append(criteria[1].find('span').get_text()) #Employment type
        except: 
            d['job_type'].append(0)
        try:
            d['job_func'].append([i.get_text() for i in criteria[2].contents[1:]])
        except:
             d['job_func'].append(0)
        try:
            d['industry'].append([i.get_text() for i in criteria[3].contents[1:]])
        except: 
            d['industry'].append(0)   

#------------------

#Initiate driver
driver = webdriver.Chrome()
country_list = ['Australia','Canada','Singapore','China','India','Japan','South%20Africa', 'Germany','France','Netherlands','Sweden','Spain','Switzerland','Italy','United%20States','United%20Kingdom']


#Get basic info
b = {'id':[], 'link':[],'title':[],'company':[],'location':[],'list_time':[]}
for country in country_list:
    link = 'https://www.linkedin.com/jobs/search?keywords=Data%2BScientist&location='+country+'&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
    load_bottom(driver,link)
    b = basic_info(b,driver)

basic = pd.DataFrame(b) 
basic.to_csv('dsjob_basic.csv',index=False)

#Get details 
basic = pd.read_csv('dsjob_basic.csv')
link_list = list(basic['link'])
detail_info(link_list)

#Check same length 
for k,v in d.items():
    print(k, len(v))

detail = pd.DataFrame(d)


#Add id column  
detail['id'] = detail['link'].str.extract(r'-(\d*)\?').astype('int')


# export to csv files 
detail.to_csv('dsjob_detail.csv',index=False)

#merge with basic info
final = basic.merge(detail,how='inner',on=['id','link'])

#export final dataset
final.to_csv('dsjob_final.csv',index=False)

