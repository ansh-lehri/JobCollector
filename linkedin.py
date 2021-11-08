import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options



class Linkedin:

    def __init__(self):

        # filters already applied - Freshness: Last 1 day, Experience: 0 years, Education: B.Tech
        self.base_url = ['https://www.linkedin.com/jobs/search?keywords=UI/UX%20Development&location=India&locationId=&geoId=102713980&sortBy=R&f_TPR=r86400&f_JT=F&f_E=1%2C2&position=1&pageNum=0',
                         'https://www.linkedin.com/jobs/search?keywords=Devops&location=India&locationId=&geoId=102713980&sortBy=R&f_TPR=r86400&f_JT=F&f_E=1%2C2&position=1&pageNum=0',
                         'https://www.linkedin.com/jobs/search?keywords=Software%20Development&location=India&locationId=&geoId=102713980&sortBy=R&f_TPR=r86400&f_JT=F&f_E=1%2C2&position=1&pageNum=0',
                         'https://www.linkedin.com/jobs/search?keywords=Machine%20Learning%20Developer&location=India&locationId=&geoId=102713980&sortBy=R&f_TPR=r86400&f_JT=F&f_E=1%2C2&position=1&pageNum=0',
                         'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=India&locationId=&geoId=102713980&sortBy=R&f_TPR=r86400&f_JT=F&f_E=1%2C2&position=1&pageNum=0',
                         'https://www.linkedin.com/jobs/search?keywords=Frontend%20Development&location=India&locationId=&geoId=102713980&sortBy=R&f_TPR=r86400&f_JT=F&f_E=1%2C2&position=1&pageNum=0',
                         'https://www.linkedin.com/jobs/search?keywords=Backend%20Development&location=India&locationId=&geoId=102713980&sortBy=R&f_TPR=r86400&f_JT=F&f_E=1%2C2&position=1&pageNum=0',
                         'https://www.linkedin.com/jobs/search?keywords=Android%20App%20Development&location=India&locationId=&geoId=102713980&sortBy=R&f_TPR=r86400&f_JT=F&f_E=1%2C2&position=1&pageNum=0',
                         'https://www.linkedin.com/jobs/search?keywords=UI/UX%20Development&location=India&locationId=&geoId=102713980&sortBy=R&f_TPR=r86400&f_JT=F&f_E=1%2C2&position=1&pageNum=0',
                         'https://www.linkedin.com/jobs/search?keywords=Full-stack%20Development&location=India&locationId=&geoId=102713980&sortBy=R&f_TPR=r86400&f_JT=F&f_E=1%2C2&position=1&pageNum=0',
        ]

        '''
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
        '''
        
        options=webdriver.ChromeOptions()
        options.headless=True
        self.driver = webdriver.Chrome("C:\\Drivers\\chromedriver.exe")
        self.driver.implicitly_wait(25)
        
        self.linkedin_jobs = []

    
    def extract_job_desc(self):
    
        for job in self.linkedin_jobs:
            
            
            try:
                print(5)
                #print(":::::::::::::::::::::::::::::::::::::::::::::         Changing page          :::::::::::::::::::::::::::::::::::::::::::::::::::")
                url = job['url']
                print(url)
                self.driver.get(job['url'])
                #time.sleep(3)
                #self.driver.get(job['url'])
                #self.driver.implicitly_wait(25)
                self.driver.implicitly_wait(25)
                
                job_page = BeautifulSoup(self.driver.page_source,'html.parser') 
                print(job_page)
                print(100)                
                time.sleep(2)
                job_desc = job_page.body.find('div',class_='show-more-less-html__markup').stripped_strings
                desc= ""
                
                for string in job_desc:
                    desc+=string
                    desc+=" "
                desc = desc.rstrip(" ")
                job['job_desc'] = desc.lower()
                print(desc)
                time.sleep(5)
                '''
                desc = self.driver.find_element_by_class_name("show-more-less-html__markup")
                job_desc = desc.text
                
                job_desc_split = job_desc.split("\n")
                job_desc = ""
                for job_desc_sentences in job_desc_split:
                    job_desc+=job_desc_sentences
                    job_desc+=" "
                job_desc = job_desc.rstrip(" ")
                                
                job['job_desc'] = job_desc.lower()
                print(":::::::::::::::::::::::::::::::::::::::::::::         Extracted Job Desc from the current page          :::::::::::::::::::::::::::::::::::::::::::::::::::")
                '''
            except Exception as e:
                print("Exception occured while extracting job info\n")
                print(e)


        return
    
    def extract_job_info(self, linkedin_jobs, ids_present):    
        
        
        for job in linkedin_jobs:
            

            try:
                print(1)
                #time.sleep(3)
                id_val = str(job.find("div")['data-entity-urn']).split(":")
                #job_id_str = id_val.get_attribute("data-entity-urn").split(":")
                print(id_val)
                job_id = int(id_val[-1])
                print(job_id)

                if job_id in ids_present:
                    continue
            except Exception as e:
                print(e)
                continue


            try:
                print(2)
                #title = job.find_element_by_class_name("base-search-card__title").text 
                title = str(job.find("h3").string)
                title = title.lstrip("\n")
                title = title.lstrip(" ")
                title = title.rstrip("\n")
                title = title.rstrip(" ")
                title = title.rstrip("\n")
                print(title)
            except Exception as e:
                print(e)

            try:
                print(3)
                job_company = job.find("h4")
                #company_name = job_company.find_element_by_class_name("hidden-nested-link").text
                company_name = str(job_company.find("a").string)
                company_name = company_name.lstrip("\n")
                comapny_name = company_name.rstrip("\n")
                company_name = company_name.lstrip(" ")
                company_name = company_name.rstrip(" ")
                print(company_name)
            except Exception as e:
                print(e)

            try:
                print(4)
                #href = job.find_elements_by_class_name("base-card__full-link")[0]
                job_url = str(job.find("a",class_="base-card__full-link")['href'])
                #job_url = href.get_attribute("href")
                print(job_url)
            except Exception as e:
                print(e)                                
            '''
            try:
                print(5)
                print(":::::::::::::::::::::::::::::::::::::::::::::         Changing page          :::::::::::::::::::::::::::::::::::::::::::::::::::")
                self.driver.get(job_url)
                self.driver.implicitly_wait(25)

                desc = self.driver.find_element_by_class_name("show-more-less-html__markup")
                job_desc = desc.text

                print(":::::::::::::::::::::::::::::::::::::::::::::         Extracted Job Desc from the current page          :::::::::::::::::::::::::::::::::::::::::::::::::::")

            except Exception as e:
                print("Exception occured while extracting job info\n")
                print(e)
            '''
            try:
                print(6)
                self.linkedin_jobs.append({'url':job_url, 'title':title, 'job_id': job_id, 'company_name':company_name, 'session':1})
                print("DONE  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
            except Exception as e:
                print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
                print(e)

        return
    
    
    
    
    def crawl_linkedin(self, ids_present):
        
        #self.driver.get("https://in.linkedin.com/jobs/view/moveinsync-frontend-developer-react-js-angularjs-at-workinsync-2766206212?refId=7gw5LOQ%2FJF1kd15iEGDEVQ%3D%3D&trackingId=23HujI8SK85zebHa%2FbWljA%3D%3D&position=22&pageNum=0&trk=public_jobs_jserp-result_search-card")
        #self.driver.implicitly_wait(25)
        #time.sleep(5)
        
        
        linkedin_jobs_per_page = []
        i=0
        for base_url in self.base_url:
            
            #i+=1
            #if i>1:
            #    break
            try:
                print(base_url)
                self.driver.get(base_url)
                self.driver.implicitly_wait(25)
                #time.sleep(360)
                # no. of jobs present
                no_of_jobs = int(self.driver.find_element_by_css_selector("h1>span").get_attribute("innerText"))
            except Exception as e:
                print("Not able to open url:     ",base_url)
                print(e)
                continue
            page_number = 1
            linkedin_jobs_per_page=[]
            while page_number <= int(no_of_jobs//25)+1:
                #if page_number==2:
                #    break                
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")                
                try:
                    self.driver.find_element_by_xpath("/html/body/div[1]/div/main/section[2]/button").click()
                    time.sleep(2)
                except Exception as e:
                    print("Exception occured while changing page: ")
                    print(e)
                    
                page_number+=1
        
              
            '''
            jobs = []
            print("Number of jobs extracted till page:  ---------------------=============================================>          ", page_number-1,"  for url  ",base_url)
            print(len(linkedin_jobs_per_page))
            print()
            '''
            
            try:
                soup = BeautifulSoup(self.driver.page_source,'html.parser')
                print(soup)
                jobs_collection = soup.find('ul',class_="jobs-search__results-list")
                linkedin_jobs = jobs_collection.find_all('li')
                #job_lists = self.driver.find_element_by_class_name("jobs-search__results-list")
                #jobs = job_lists.find_elements_by_tag_name("li")
                #linkedin_jobs_per_page.extend(jobs)
            except Exception as e:
                print("Error during job list extractiom: ")
                print(e)
            
            #page_number+=1
            '''
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")                
            try:
                self.driver.find_element_by_xpath("/html/body/div[1]/div/main/section[2]/button").click()
                time.sleep(3)
            except Exception as e:
                print("Exception occured while changing page: ")
                print(e)
            '''
            
            print("------------------------------------------------------------------------------------------------------------------------------------------------")
            #print(len(linkedin_jobs_per_page))
            print(len(linkedin_jobs))
            print("-------------------------------------------------------------------------------------------------------------------------------------------------")
            #self.extract_job_info(linkedin_jobs_per_page, ids_present)
            self.extract_job_info(linkedin_jobs, ids_present)
            #self.extract_job_desc()
        
        #self.extract_job_info(linkedin_jobs_per_page, ids_present)
        #print(len(self.linkedin_jobs))
        self.extract_job_desc()

        return
        