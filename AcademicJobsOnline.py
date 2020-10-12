# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 12:35:17 2020
(c) 2020
@author: Josephat Koima
PhD Candidate - Michigan State University
Dual Major: Economics / Agricultural,Food, & Resource Economics
email: koimajos@msu.edu
website: https://sites.google.com/msu.edu/josephat-koima

@Description:
    This code extracts job openings posted on https://academicjobsonline.org/ into an excel file. 
    The relevant fields extracted include: 
   'Institution', 'Position','Date Posted','Application Deadline','Location','Country',
   'Citizenship Requirements','Review Date','Application Requirements' 


**Comments are welcome
"""

#import necessary modules/libraries
import pandas as pd 
import requests, re
from bs4 import BeautifulSoup

#url for jobs posted 
url='https://academicjobsonline.org/ajo?joblist-0-0-0-0------'
#place a request and convert data to beautiful soup format
website_url = requests.get(url).text
soup = BeautifulSoup(website_url,'lxml')

#Find all listings
results=soup.findAll('dt',attrs={'class':'clr'})

#List to store all jobs
jobs=[]
#Go through each listing and extract important detailes
for result in results:
    #job lists for each insitution
    job_lists=result.findAll('li')
    
    #Go through each job description and extract key details
    for x in job_lists:
        link='https://academicjobsonline.org'+x.find('a')['href']
        joburl_data=requests.get(link).text
        soup2=BeautifulSoup(joburl_data,'lxml')
        
        details=soup2.find('table',attrs={'class':'nobr'})
        rows=details.findAll('tr')
        
        job_det={'ID':'','Title':'','Type':'','Location':'','Areas':'','Deadline':''}
        for row in rows[:-1]:
            keyval=row.findAll('td')
            key=(row.text).split(':')[0]
            key=key.split(' ')[1]
            if key=='Area':
                key='Areas'
            value=keyval[1].text 
            job_det[key]=value
        print(job_det)
        print('*******************************************************************************************')       
        
        #Position ID
        pid=(job_det['ID']).strip()
        print('Position ID:'+pid)
        
        #Position Title
        ptitle=(job_det['Title']).strip()
        print('Title:'+ptitle)

        #Position Type
        ptype=(job_det['Type']).strip()
        print('Type:'+ptype)
        #Position Location
        plocation=(job_det['Location']).strip()
        print('Location:'+plocation)
        pcountry=(plocation.split(',')[-1]).split(' [map]')[0]
        print('Country:'+pcountry)
        #Subject Area
        pArea=(job_det['Areas']).strip()
        print('Subject Area:'+pArea)
        #Deadline
        pdeadline=(job_det['Deadline']).split(' ')[0]
        print('Deadline:'+pdeadline)
        #Postinf date
        try:
            pposted=(job_det['Deadline'].split('posted ')[1]).split(',')[0]
            print('Posted:'+pposted)
        except: 
            pass
        #Description
        description=soup2.find('table',attrs={'class':'ads'}).text
        #citizenship requirements (e.g. US Citizenship Required)
        cit=description.replace('U.S.','US')
        citizen=re.findall(r"([^.]*?citizen[^.]*\.)",cit)   
        citizen=(''.join(citizen)).strip()
        print('Citizenship Requirements:'+citizen)
        
        #Contains important info on application review process: Some posts start reviewing applications before deadlines
        review=re.findall(r"([^.]*?review[^.]*\.)",description)   
        review=(''.join(review)).strip()
        if 'peer-review' in review:
            review=''    
        print('Review:'+review)
        #Application Requirements
        try:
            b=soup2.find('b', text=re.compile('Application Materials Required'))
            req=(b.next_sibling).find('ul').findAll('li')
            requirements=(req[0].text).strip()
            for r in req[1:]:
                requirements+=","+(r.text).strip()
            print(requirements)
        except:
            pass
        #Joblink
        print('url:'+link)
        print('*************************************************************************************')
        
        #Job detail
        job=[pid,ptitle,ptype,plocation,pcountry,pArea,pdeadline,pposted,citizen,review,requirements,link]
        #add the job to the list containing all jobs
        jobs.append(job)
#Export data to excel using pandas data-frames 
df = pd.DataFrame(jobs, columns =['Job ID', 'Title','Type','Location','Country','Subject Area','Deadline',
                                  'Posted','Citizenship Requirements','Review Date','Application Requirements','Job Link']) 
df.to_excel("AcademicJobsOnline.xlsx")
print('************DONE************')