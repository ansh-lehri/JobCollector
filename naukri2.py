import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

class Naukri:

    def __init__(self):

        # filters already applied - Freshness: Last 1 day, Experience: 0 years, Education: B.Tech
        
        self.base_url = ['https://www.naukri.com/information-technology-jobs?xt=catsrch&qi[]=25&jobAge=1&experience=0&ugTypeGid=12',
        'https://www.naukri.com/ecommerce-jobs?jobAge=1&experience=0&ugTypeGid=12',
        'https://www.naukri.com/mainframe-jobs?xt=catsrch&qi[]=25&jobAge=1&experience=0&ugTypeGid=12',
        'https://www.naukri.com/telecom-software-jobs?xt=catsrch&qi[]=25&jobAge=1&experience=0&ugTypeGid=12',
        'https://www.naukri.com/mobile-jobs?xt=catsrch&qi[]=25&jobAge=1&experience=0&ugTypeGid=12',
        'https://www.naukri.com/dba-jobs?xt=catsrch&qi[]=25&jobAge=1&experience=0&ugTypeGid=12',
        'https://www.naukri.com/client-server-jobs?xt=catsrch&qi[]=25&jobAge=1&experience=0&ugTypeGid=12',
        'https://www.naukri.com/system-programming-jobs?xt=catsrch&qi[]=25&jobAge=1&experience=0&ugTypeGid=12',
        'https://www.naukri.com/application-programming-jobs?xt=catsrch&qi[]=25&jobAge=1&experience=0&ugTypeGid=12',
        ]
        
        #self.base_url = ['https://www.naukri.com/information-technology-jobs?xt=catsrch&qi[]=25&jobAge=1&experience=0&ugTypeGid=12',]

        try:
            chrome_options = Options()
            print(1)

            chrome_options.add_argument("--headless")
            print(2)

            chrome_options.add_argument("--no-sandbox")
            print(3)

            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
            chrome_options.add_argument(f'user-agent={user_agent}')
            print(4)

            self.driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",chrome_options=chrome_options)
            print(5)

            self.driver.implicitly_wait(30)
        except Exception as e:
            print(e)
        self.naukri_jobs = []




    def jobTupleHeader(self, job):

        #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        header = job.find(class_="jobTupleHeader")

        try:
            title = header.find(class_='info fleft').find('a').string
        except Exception as e:
            print("Error Occured while retrieving Title")
            title = "NaN"
            #print(1)

        try:
            job_url_atag = header.find('a',class_='title')
            job_url = job_url_atag.get('href')
        except Exception as e:
            print("No Job URL Available")
            job_url = "Nan"

        try:
            company_name = header.find(class_='mt-7 companyInfo subheading lh16').find('a').string
        except Exception as e:
            print("Error Occured while retrieving Company_Name")
            company_name = "NaN"
            #print(2)
        try:
            experience = header.find('ul').find('li').find('span').string
        except Exception as e:
            print("Error Occured while retrieving Experience")
            experience = "NaN"
            #print(3)
        return title, company_name, experience, job_url


    def tags_has_descriptions(self, job):

        #print("?????????????????????????????????????????????????????????????")
        required_skills = []

        try:
            skills = job.find('ul',class_='tags has-description').find_all('li')
            for skill in skills:
                required_skills.append(str(skill.string))
        except Exception as e:
            print("Error occured while retrieving Skills.")
            print(4)
        return required_skills


    def check_if_disabled(self, next_page_a_tag):

        if next_page_a_tag.has_attr('disabled'):
            return True
        return False


    def extract_job_info(self, job, ids_present):

        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #print(job)
        job_id = job['data-job-id']

        if job_id in ids_present:
            print("NAUKRI JOB ALREADY PRESENT.")
            return

        print("NEW NAUKRI LISTING")

        # check if job_id already exists.
        # self.check_job_id(job_id)

        title, company_name, experience, job_url = self.jobTupleHeader(job)
        required_skills = self.tags_has_descriptions(job)
        #self.jobTupleFooter(job)

        print(title,"	 ",company_name,"	 ",experience,"	",required_skills," ",job_id)


        try:
            self.naukri_jobs.append({'url':job_url, 'title':title, 'job_id': job_id, 'company_name':company_name, 'experience':experience, 'skills':required_skills, 'session':1})
            print("DONE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        except Exception as e:
            print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
            print(e)
        return


    def crawl_naukri(self, ids_present):

        for base_url in self.base_url:

            url=base_url
            base_url_split = url.split('?')
            print()
            print()
            print("THE	BASE	URL	----------------->		 ",base_url)
            print()
            print()
            page_number = 1

            while True:

                print()
                print()
                print()
                print()

                self.driver.get(url)
                #time.sleep(3)
                self.driver.implicitly_wait(70)
                print("YYAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHOOOOOOOOOOOOOOOOOOOOOOOOOO")
                time.sleep(60)
                soup = BeautifulSoup(self.driver.page_source,'html.parser')
                print(soup)
                job_listings = soup.find_all('article',class_="jobTuple bgWhite br4 mb-8")

                #print("******************************")
                print(job_listings)
                print("*******************************")


                for job in job_listings:
                    _ = self.extract_job_info(job, ids_present)
                
                page_number+=1
                print("P A G E	 N U M B E R		-------			",page_number)

                pagination = soup.find('div',class_='pagination')
                
                
                print("MUMMY       MR>       BROWN::::::::::::::::::::::::::::::")
                print(pagination)
                print("PAPA         MR         BROWN::::::::::::::::::::::::::::::::::::")
                if pagination == None:
                    break
                break 
                next_page_a_tag = pagination.find('a',class_='fright')

                if self.check_if_disabled(next_page_a_tag):
                    print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                    break
                else:
                    url=base_url_split[0]+"-"+f'{page_number}'+'?'+base_url_split[1]
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
                    print(url)

        print(len(self.naukri_jobs))
        print("=================================================================++++++++++++++++++++++++++++++++++++++++++++++")
        for job in self.naukri_jobs:
            url = job['url']
            print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
            self.driver.get(url)
            try:
                job_page = BeautifulSoup(self.driver.page_source,'html.parser')
                
                print(100)
                
                time.sleep(2)
                job_desc = job_page.body.find('section',class_='job-desc')
                print(101)
                short_job_desc = str(job_page.head.find('meta',{'name':'description'})['content'])
                print(102)
            except Exception as e:
                print("EXCEPTION     1  ---------------------------------------")
                print(e)
            desc=""
            if short_job_desc == None:
                short_job_desc=""
            try:
                for string in job_desc.stripped_strings:

                    desc+=string
                    desc+=" "
            except Exception as e:
                print(e)
                print("Description not available")

            job['description']=desc
            job['short_desc']=short_job_desc
