#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: vyvo

Scrape data of available job postings on LinkedIn. 
Attributes: ID, Link, Title, Company, Location, List time, Description, Experience level, Job type, Job function, Industry 
"""

from dependency import *

def load_bottom(driver,link):
    """
    Load all the results
    Example link for Data Scientist: https://www.linkedin.com/jobs/search?keywords=Data%2BScientist&location=Worldwide&redirect=false&position=1&pageNum=0
    
    """
    driver.get(link)
    SCROLL_PAUSE_TIME = 1
    # The page has either Infinite loading or "See more" button 
    last_height = driver.execute_script("return document.body.scrollHeight") #get scrool height
    try: 
        while True: 
        # Navigate to see-more-jobs button and load      
            button = driver.find_element_by_class_name("see-more-jobs")
            button.click()
        # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
        # Calculate new scroll height and compare with last scroll height    
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


def basic_info(driver):
    """
    Collect basic information of job postings displayed on results page: ID, Link, Title, Company, Location, List time 

    """
    global basic
    basic = {'id':[], 'link':[],'title':[],'company':[],'location':[],'list_time':[]}
    soup = BeautifulSoup(driver.page_source, "lxml")
    jobs = soup.find_all('li',class_=re.compile('result-card'))
    try:
        for ad in jobs:
            basic['id'].append(ad.attrs['data-id'])
            basic['link'].append(ad.find('a').get('href'))
            basic['title'].append(ad.find('h3').get_text())
            basic['company'].append(ad.find('h4').get_text())
            basic['location'].append(ad.find_all("span",class_="job-result-card__location")[0].get_text())
            basic['list_time'].append(ad.find_all("time")[0].attrs['datetime'])
    except: pass 


def detail_info(link_list):
    """
    Collect details of each job: Description, Experience level, Job type, Job function, Industry  
    Input: List of job links collected from basic info  
    """
    global detail
    detail  = {'description':[],'exp_level':[],'job_type':[],'job_func':[],'industry':[],'link':[]}
    for lk in link_list:
        result = requests.get(lk)
        src = BeautifulSoup(result.content,"lxml") 
        
        # Track crawling process 
        print(link_list.index(lk),end='---')
        
        detail['link'].append(lk)
        try:
            detail['description'].append(src.find_all("div",class_=re.compile("text description"))[0])
        except: 
            # 0 values represents missing values due to crawling errors
            detail['description'].append(0)
        
        criteria = src.find_all("li",class_="job-criteria__item")
        try:
            detail['exp_level'].append(criteria[0].find('span').get_text()) #Seniority level 
        except:
            detail['exp_level'].append(0)
        try:
            detail['job_type'].append(criteria[1].find('span').get_text()) #Employment type
        except: 
            detail['job_type'].append(0)
        try:
            detail['job_func'].append([i.get_text() for i in criteria[2].contents[1:]])
        except:
             detail['job_func'].append(0)
        try:
            detail['industry'].append([i.get_text() for i in criteria[3].contents[1:]])
        except: 
            detail['industry'].append(0)   



