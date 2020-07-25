#medicine='lorazepam Concentrate'
medicine='Nortriptyline HCL'

import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

cwd=os.path.dirname(os.path.abspath(__file__))

web_driver='chromedriver.exe'
web_driver_path=os.path.join(cwd, web_driver)
driver = webdriver.Chrome(web_driver_path)
url='''https://www.webmd.com/drugs/'''

def extract_webpage(driver, medicine, url):
    all_data={}
    
    driver.get(url)
    drug_search=driver.find_element_by_id("drugs-query")
    drug_search.send_keys(medicine)
    drug_search.send_keys(Keys.ENTER)
    
    #new_page
    driver.switch_to.window(driver.window_handles[-1])
    # get the link of exact match
    try:
        div=driver.find_element_by_class_name('exact-match')
    
        searched_link_of_url = div.find_element_by_css_selector('a').get_attribute('href')
        driver.get(searched_link_of_url)
    except:
        pass
    
    # extract fields
    div=driver.find_element_by_class_name('drug-names')
    Drug_Name = div.find_element_by_css_selector('h1').text
    all_data['Drug_Name'] = Drug_Name
    
    for tag in div.find_elements_by_css_selector('p'):
        other_field = tag.text.split(':')
        if len(other_field)>1:
            all_data[other_field[0][:-3]] = str(other_field[1]).strip()
            
    try:
        div=driver.find_element_by_class_name('show-more')
        div.click()
    except:
        pass
    
    try:
        div=driver.find_element_by_class_name('fdb-warnings')
        all_data['Warning'] = div.find_element_by_css_selector('p').text[:400]
    except:
        all_data['Warning'] = None
    
    # Move to read_review section
    div=driver.find_element_by_class_name('drug-review')
    
    read_review_link = div.get_attribute('href')
    
    driver.get(read_review_link)
    
    try:
        Effectiveness = int(driver.find_element_by_id('EffectivenessSummaryValue').text.split('.')[0][-1])
        all_data['Effectiveness']=Effectiveness
    except:
        all_data['Effectiveness']=None
    
    try:
        Ease_of_use=int(driver.find_element_by_id('EaseOfUseSummaryValue').text.split('.')[0][-1])
        all_data['Ease_of_use']=Ease_of_use
    except:
        all_data['Ease_of_use']=None
    
    try:
        Satisfaction = int(driver.find_element_by_id('SideEffectsSummaryValue').text.split('.')[0][-1])
        all_data['Satisfaction']=Satisfaction
    except:
        all_data['Satisfaction']=None
    
    return all_data
    
if __name__=="__main__":
    all_data=extract_webpage(driver, medicine, url)
    df=pd.DataFrame(all_data, index=['i',])
    print(df.head(10))
    df.to_csv(os.path.join(cwd, 'drug_details.csv'))

