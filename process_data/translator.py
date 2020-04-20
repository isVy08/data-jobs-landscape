#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: vyvo

Translate data from a dataframe stored in Excel file using Google Translate translate.google.com 

"""


from dependency import * 


def translate(language_code,path,store=True): 
    """
    Returns translated dataframe in a local Excel file to a certain language
    
    Parameters: 
    language_code: Language to be translated into. Follow Google language ISO codes at https://cloud.google.com/translate/docs/languages
    path         : Path to local file 
    store        : Store data into dataframe, default = True. If want to proceed with Copy & Paste into a local file, set Store = False 
    
    """
    data = pd.read_excel(path)
    
    # Number of rows and columns
    nrow = data.shape[0]
    ncol = data.shape[1]
    
    driver = webdriver.Chrome()
    driver.get('https://translate.google.com/')
    
    # Navigate to Document Upload page   
    upload = driver.find_element_by_xpath("//div[@class='tlid-input-button input-button header-button tlid-input-button-docs documents-icon']")
    upload.click()
    time.sleep(5)
    
    # Upload file  
    button = driver.find_element_by_xpath("//input[@id='tlid-file-input']") 
    button.send_keys(path)
    
    # Detect Language 
    button = driver.find_element_by_xpath("//div[@class='goog-inline-block jfk-button jfk-button-standard jfk-button-collapse-right jfk-button-checked']")
    button.click()
    time.sleep(5)
    xpath = "//div[@class='language_list_item_wrapper language_list_item_wrapper-"+language_code+"']"
    button = driver.find_element_by_xpath(xpath)
    button.click() 
    time.sleep(5)


    # Click Translate button 
    trans = driver.find_element_by_xpath("//input[@class='tlid-translate-doc-button button']")
    trans.click() 
    time.sleep(90)

    # Get translated text 
    if store: 
        print('Please wait')        
        d = {}
        for col in range(ncol):
            d[col] = []
            for row in range(nrow):
                xpath = "//tr["+str(row+2)+"]//td["+str(col+1)+"]"
                body = driver.find_element_by_xpath(xpath)
                d[col].append(body.text) 
        trans_data = pd.DataFrame(d)
        trans_data.columns = data.columns
        return trans_data
    
    else:
        print('Take some time to Copy & Paste before return to homepage')
        time.sleep(90)
        driver.get('https://translate.google.com/')
        
         


