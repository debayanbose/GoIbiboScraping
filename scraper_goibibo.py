# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 10:43:12 2020

@author: debayan.bose
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 16:07:34 2020

@author: debayan.bose
"""

import csv
import selenium.webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
#from multiprocessing.pool import ThreadPool, Pool
#import threading
from selenium import webdriver
#from multiprocessing import Process
#import multiprocessing
import time
import warnings
import datetime
from dateutil.rrule import rrule, DAILY
#import config
import pandas as pd
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from pymongo import MongoClient 
from selenium.webdriver.firefox.options import Options
warnings.filterwarnings("ignore")


def get_driver():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,executable_path=r'C:/D Backup/geckodriver.exe')
    return driver

def find_all(a_str, sub):
            start = 0
            while True:
                start = a_str.find(sub, start)
                if start == -1: return
                yield start
                start += len(sub) # use start += 1 to find overlapping matches
                
def scrape_goibibo(url,depdate):
    depdate = str(datetime.datetime.strptime(depdate, "%m/%d/%Y").date().strftime('%d/%m/%Y'))
    driver=get_driver()
    driver.get(url)  			 # URL requested in browser.
    time.sleep(20)
    for i in range(50): # adjust integer value for need
       driver.execute_script("window.scrollBy(0, 500)")
       time.sleep(0.5)
       
    body = driver.page_source
    soup = BeautifulSoup(body, "lxml")
    info = soup.find_all('div', attrs={'class': "clr"})
    temp1 = url.replace('https://www.goibibo.com/flights/air-','')
    temp2 = temp1[len(temp1)-12:len(temp1)]
    temp1 = temp1.replace(temp2,'')
    temp1 = temp1.replace('-','')
    
    if len(info)<=1:
        if not(driver is None):
            driver.close()
            driver.quit()
        driver=get_driver()
        driver.get(url)  			 # URL requested in browser.
        time.sleep(10)
        for i in range(50): # adjust integer value for need
           driver.execute_script("window.scrollBy(0, 500)")
           time.sleep(0.5)
        body = driver.page_source
        soup = BeautifulSoup(body, "lxml")
        info = soup.find_all('div', attrs={'class': "clr"})
        if len(info)<=1:
            if not(driver is None):
                driver.close()
                driver.quit()
            print('NO RECORDS FOUND FOR '+url)
            return None
    
    flightData = []
    for i in range(len(info)):
        data = str(info[i])
        ## fetch flight number
        
        flt_position = list(find_all(data,temp1))
        if len(flt_position)>0:
            flt_end_position = list(find_all(data,'">'))
            y = list(filter(lambda x: x > int(flt_position[0]), flt_end_position))[0]
            temp3 = data[flt_position[0]:y]
            flight_number = temp3.split(':')[1]
            
            split_carrier = flight_number[0:2]
            flight_number_split = flight_number.split(split_carrier)
            flght_number_new=[]
            for k in range(len(flight_number_split)):
                if(flight_number_split[k] !=''):
                    flght_number_new.append(split_carrier + '-' + flight_number_split[k])
                    
            flght_number_new = ','.join(flght_number_new)
            
            try:
                flight_name = info[i].find('span', attrs={'class': "greyLt ico13 padR10 padL5"}).text
            except:
                flight_name = info[i].find('span', attrs={'class': "ico13 padR10 padL5"}).text
            origin = info[i].find('span', attrs={'class': "ico11 greyLt padL5"}).text #origin
            destination = info[i].find('span', attrs={'class': "greyLt ico11 padL5"}).text #destination
            deptime = info[i].find('span', attrs={'class': "fb ico18 padT5 quicks"}).text #depatime
            arrtime = info[i].find('span', attrs={'class': "fb dF alignItemsCenter ico18 padT5 quicks"}).text #arrtime
            duration = info[i].find('div', attrs={'class': "ico15 fb txtCenter quicks padT5"}).text #duration
            fare = info[i].find('span', attrs={'class': "ico20 fb quicks"}).text #duration
            ## calculate number of stops
            stops_position = list(find_all(data,'stopsLength'))
            stops_end_position = list(find_all(data,'">'))
            
            x = list(filter(lambda x: x > int(stops_position[0]), stops_end_position))[0]
            stops = data[x-1]
            flightData.append([depdate, flight_name,flght_number_new,deptime,origin,duration,arrtime,destination,fare,stops])
    flightData = pd.DataFrame(flightData)
    print('no of records found - '+str(len(flightData)) + ' for '+url)
    driver.close()
    driver.quit()
    return flightData


def scrape_goibibo_int(url,depdate):
    depdate = str(datetime.datetime.strptime(depdate, "%m/%d/%Y").date().strftime('%d/%m/%Y'))
    driver=get_driver()
    driver.get(url)  			 # URL requested in browser.
    time.sleep(10)
    for i in range(50): # adjust integer value for need
       driver.execute_script("window.scrollBy(0, 500)")
       time.sleep(0.5)
       
    body = driver.page_source
    soup = BeautifulSoup(body, "lxml")
    info = soup.find_all('div', attrs={'class': "clr"})
    temp1 = url.replace('https://www.goibibo.com/flights/air-','')
    temp2 = temp1[len(temp1)-12:len(temp1)]
    temp1 = temp1.replace(temp2,'')
    temp1 = temp1.replace('-','')
    
    if len(info)<=1:
        if not(driver is None):
            driver.close()
            driver.quit()
        driver=get_driver()
        driver.get(url)  			 # URL requested in browser.
        time.sleep(10)
        for i in range(50): # adjust integer value for need
           driver.execute_script("window.scrollBy(0, 500)")
           time.sleep(0.5)
        body = driver.page_source
        soup = BeautifulSoup(body, "lxml")
        info = soup.find_all('div', attrs={'class': "clr"})
        if len(info)<=1:
            if not(driver is None):
                driver.close()
                driver.quit()
            print('NO RECORDS FOUND FOR '+url)
            return None
    
    element = driver.find_elements_by_xpath("//a[@class='dF alignItemsCenter curPointFlt fr']")

            # click on every Flight Details element
    for i in range(len(element)):
                driver.execute_script("arguments[0].click();", element[i])
                #time.sleep(1.5)


            #Get Flight Details individual tabs
    for elem in driver.find_elements_by_xpath(".//span[@class='curPointFlt ']"):
                if  elem.text in "FARE DETAILS":
                    driver.execute_script("arguments[0].click();", elem)
    body = driver.page_source
    soup = BeautifulSoup(body, "lxml")
    info = soup.find_all('div', attrs={'class': "clr"})
    fil = open("out_goibibo_int_fare.txt", "w", encoding='utf-8')
    fil.write(str(info))
    flightData = []
    for i in range(len(info)):
        data = str(info[i])
        ## fetch flight number
        
        flt_position = list(find_all(data,temp1))
        if len(flt_position)>0:
            flt_end_position = list(find_all(data,'">'))
            y = list(filter(lambda x: x > int(flt_position[0]), flt_end_position))[0]
            temp3 = data[flt_position[0]:y]
            flight_number = temp3.split(':')[1]
            
            split_carrier = flight_number[0:2]
            flight_number_split = flight_number.split(split_carrier)
            flght_number_new=[]
            for k in range(len(flight_number_split)):
                if(flight_number_split[k] !=''):
                    flght_number_new.append(split_carrier + '-' + flight_number_split[k])
                    
            flght_number_new = ','.join(flght_number_new)
            
            try:
                flight_name = info[i].find('span', attrs={'class': "greyLt ico13 padR10 padL5"}).text
            except:
                flight_name = info[i].find('span', attrs={'class': "ico13 padR10 padL5"}).text
            origin = info[i].find('span', attrs={'class': "ico11 greyLt padL5"}).text #origin
            destination = info[i].find('span', attrs={'class': "greyLt ico11 padL5"}).text #destination
            deptime = info[i].find('span', attrs={'class': "fb ico18 padT5 quicks"}).text #depatime
            arrtime = info[i].find('span', attrs={'class': "fb dF alignItemsCenter ico18 padT5 quicks"}).text #arrtime
            duration = info[i].find('div', attrs={'class': "ico15 fb txtCenter quicks padT5"}).text #duration
            fare = info[i].find('span', attrs={'class': "ico20 fb quicks"}).text #duration
            ## calculate number of stops
            stops_position = list(find_all(data,'stopsLength'))
            stops_end_position = list(find_all(data,'">'))
            fare_breakup = info[i].find('div',attrs={'class':"fareBreak marginB20"}).text
            fare_breakup = fare_breakup.replace('Base Fare (1 Adult)','-----')
            fare_breakup = fare_breakup.replace('Taxes and Fees (1 Adult)','-----')
            fare_breakup = fare_breakup.replace('Total Fare (1 Adult)','-----')
            fare_breakup = fare_breakup.split('-----')
            base_fare = fare_breakup[1]
            base_fare = int(base_fare.replace(',',''))
            taxes_fare = fare_breakup[2]
            taxes_fare = int(taxes_fare.replace(',',''))
            total_fare = fare_breakup[3]
            total_fare = int(total_fare.replace(',',''))
            fare = int(fare.replace(',',''))
            discounts = fare - total_fare
            
            x = list(filter(lambda x: x > int(stops_position[0]), stops_end_position))[0]
            stops = data[x-1]
            flightData.append([depdate, flight_name,flght_number_new,deptime,origin,duration,arrtime,destination,stops,fare,base_fare,taxes_fare,discounts])
    flightData = pd.DataFrame(flightData)
    print('no of records found - '+str(len(flightData)) + ' for '+url)
    driver.close()
    driver.quit()
    return flightData

def scrapenew_goibibo(origin,destin,fromdate,todate,job_time, passengers, stops):
    a = datetime.datetime.strptime(fromdate, "%d/%m/%Y").date()
    b = datetime.datetime.strptime(todate, "%d/%m/%Y").date()
    trDate = list()
    for dt in rrule(DAILY, dtstart=a, until=b):
        dept_date = str(dt.strftime("%m/%d/%Y"))
        trDate.append(dept_date)
    all_urls = list()  
    for j in range(len(trDate)):
        url = 'https://www.goibibo.com/flights/air-'
        url = url + origin + '-' + destin
        dt_format = str(datetime.datetime.strptime(trDate[j], "%m/%d/%Y").date().strftime('%Y%m%d'))
        url = url + '-' +dt_format+'--'
        
        passengers = 'A-1_C-0_I-0'
        adults = passengers[2]
        children = passengers[6]
        infants = passengers[10]
        url = url + adults + '-' + children + '-' + infants + '-E-D/'
        all_urls.append(url)
        
    data=list()
    for urls in range(len(all_urls)):
        print(trDate[urls])
        temp1 = scrape_goibibo(all_urls[urls],trDate[urls])
        if not (temp1 is None):
            data.append(temp1)
    if len(data) == 0:
        return 0
    df = pd.concat(data)
    df.columns = ['DepartureDate','FlightName', 'FlightCode', 'DepTime','DepCity','FlightDuration','ArrivalTime','ArrivalCity','fare','stops']
#    for i in range(len(data)):
#        for j in range(len(data[i])):
#            df = df.append(pd.Series(data[i][j],index = ['DepartureDate','FlightName', 'FlightCode', 'DepTime','DepCity','FlightDuration','ArrivalTime','ArrivalCity','fare','stops']),ignore_index=True)
#   
                 
    df['fare'] = [w.replace('₹ ', '') for w in df['fare']]
    df['fare'] = [w.replace(',', '') for w in df['fare']]
    df['fare']= np.array(df['fare'],float)
    df['sector']= origin +'_'+destin
    df['job_time'] = job_time
    df['stops'] = np.array(df['stops'],int)
    if (stops >= 0):
        df = df.query("stops == "+str(stops))

    if len(df.index) == 0:
        return 0
    df['source'] = 'GOIBIBO'
#    conn = MongoClient(config.LOCAL_DB_SERVER)
#    db = conn.database 
#    new_database = db.scrapedb  
#    data = df.to_dict(orient='records') 
#    result = new_database.insert_many(data)
#    
#    return len(result.inserted_ids)
    return df




def scrapenew_goibibo_int(origin,destin,fromdate,todate,job_time, passengers, stops):
    a = datetime.datetime.strptime(fromdate, "%d/%m/%Y").date()
    b = datetime.datetime.strptime(todate, "%d/%m/%Y").date()
    trDate = list()
    for dt in rrule(DAILY, dtstart=a, until=b):
        dept_date = str(dt.strftime("%m/%d/%Y"))
        trDate.append(dept_date)
    all_urls = list()  
    for j in range(len(trDate)):
        url = 'https://www.goibibo.com/flights/air-'
        url = url + origin + '-' + destin
        dt_format = str(datetime.datetime.strptime(trDate[j], "%m/%d/%Y").date().strftime('%Y%m%d'))
        url = url + '-' +dt_format+'--'
        
        passengers = 'A-1_C-0_I-0'
        adults = passengers[2]
        children = passengers[6]
        infants = passengers[10]
        url = url + adults + '-' + children + '-' + infants + '-E-D/'
        all_urls.append(url)
        
    data=list()
    for urls in range(len(all_urls)):
        print(trDate[urls])
        temp1 = scrape_goibibo_int(all_urls[urls],trDate[urls])
        if not (temp1 is None):
            data.append(temp1)
    if len(data) == 0:
        return 0
    df = pd.concat(data)
    df.columns = ['DepartureDate','FlightName', 'FlightCode','DepTime','DepCity','FlightDuration','ArrivalTime','ArrivalCity','stops','fare','BaseFare','SurchargeFare','Discounts']
                 
    df['sector']= origin +'_'+destin
    df['job_time'] = job_time
    df['stops'] = np.array(df['stops'],int)
    if (stops >= 0):
        df = df.query("stops == "+str(stops))

    if len(df.index) == 0:
        return 0
    df['source'] = 'GOIBIBO'
#    conn = MongoClient(config.LOCAL_DB_SERVER)
#    db = conn.database 
#    new_database = db.scrapedb  
#    data = df.to_dict(orient='records') 
#    result = new_database.insert_many(data)
#    
#    return len(result.inserted_ids)
    return df

if __name__ == '__main__':
    mydata = scrapenew_goibibo_int('BOM','DXB','11/03/2020','11/03/2020','11/01/2020 00:10',
                       passengers='A-1_C-0_I-0', stops = 0 )
