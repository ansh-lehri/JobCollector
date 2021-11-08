import concurrent.futures
import pandas as pd
import re
import requests
import threading
import time

from bs4 import BeautifulSoup


class Internshala:

    def __init__(self):

        self.to_crawl = "https://internshala.com/internships/computer%20science-internship/"
        self.base_url = "https://internshala.com"
        self.internshala_jobs = []

    def round_tabs_container(self, soup):
        
        required_skills = []
        
        try:
            skills_div = soup.find('div',class_='round_tabs_container')
            skills = skills_div.find_all('span',class_='round_tabs')

            for skill in skills:
                required_skills.append(str(skill.string))
        except Exception as e:
            print("Error occured while retrieving skills required.")

        print(4)
        return required_skills
            

    def extract_text(self, soup):

        text_strings = soup.body.find('div',class_='internship_details').stripped_strings
        content = ""
        content = " ".join(text for text in text_strings)

        #content = re.sub(r"[&*%$@!\(\)\'\/\\,<>\|:]+"," ", content)
        #content=re.sub(r'\.{2,}'," ",content)
        #content = re.sub(r'\s{2,}'," ",content)
        content=content.lower()

        return content


    def job_title_company(self, soup):
        

        try:
            title = str(soup.find('span',class_='profile_on_detail_page').string)
        except Exception as e:
            print("Error occured while retrieving skills required.")
            title = "NaN"
        
        print(1)
        try:
            company_name = str(soup.find('a',class_='link_display_like_text').string)
            company_name = company_name.lstrip("\n")
            company_name = company_name.lstrip(" ")
            company_name = company_name.rstrip(" ")
        except Exception as e:
            print("Error occured while retrieving skills required.")
            company_name = "NaN"
        print(2)

        # giving experience a default value of 0-1 yrs as no experience value present on internshala page
        experience = "0-1 years"

        return title, company_name, experience


    def extract_meta_desc(self,soup):
    
        try:
            short_desc_meta_tag = soup.find('meta',{'name':'twitter:description'})
            short_desc = re.sub(r'(\\r)?\\n{0,}'," ",short_desc_meta_tag['content'])
        except Exception as e:
            print(e)
            short_desc = ""
        return short_desc
    

    def extract_job_info(self, job, lock, ids_present):

        job_id = job['internshipid']

        if job_id in ids_present:
            print("JOB ALREADY PRESENT")
            return
        
        print("JOB NOT PRESENT")

        detail_job_page = job.find('a',class_="view_detail_button")
        job_page_link = detail_job_page['href']
        job_page_link = self.base_url + job_page_link

        page_request = requests.get(job_page_link)
        page_soup = BeautifulSoup(page_request.text,'html.parser')

        title, company_name, experience = self.job_title_company(page_soup)
        required_skills = self.round_tabs_container(page_soup)
        text = self.extract_text(page_soup)
        short_desc = self.extract_meta_desc(page_soup)
        
        #print(title,"   ",company_name,"   ",experience,"  ",required_skills," ",job_id," ",text)

        lock.acquire()
        try:
            self.internshala_jobs.append({'url': job_page_link, 'title':title, 'job_id': job_id, 'company_name':company_name, 'experience':experience, 'skills':required_skills, 'session':1, 'description':text,'short_desc':short_desc})
            print("DONE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        except Exception as e:
            print(e)
        lock.release()

        return

    
    def check_if_list_over(self, class_):

        class_=str(class_)
        if re.search("container-fluid individual_internship no_result_message no_result", class_):
            return True
        else:
            return False


    def check_sub(self, class_):
        
        class_=str(class_)
        if re.search("container-fluid individual_internship", class_):
            return True
        else:
            return False


    def crawl_internshala(self, ids_present):

        page_number = 50
        trials=0

        page_to_crawl = self.to_crawl + "page-" + f"{page_number}"
        r = requests.get(page_to_crawl)

        status = r.status_code


        while True:
            
            #print(page_number)
            soup = BeautifulSoup(r.text,'html.parser')
            job_listings = soup.find_all('div',class_=self.check_sub)

            
            if self.check_if_list_over(job_listings[0]):
                break


            print("******************************")
            #print(job_listings)
            print("*******************************")
            
            lock=threading.Lock()
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                {executor.submit(self.extract_job_info, job, lock, ids_present):job for job in job_listings}
            
            
            page_number+=1
            page_to_crawl = self.to_crawl + "page-" + f"{page_number}"
            #print(page_to_crawl)
            r = requests.get(page_to_crawl)
            status=r.status_code
            #print(status)
           

'''
if __name__=="__main__":

    internshala = Internshala()
    mongodb = MongoDB("Job_Collector")

    ids_present = mongodb.extract_ids_session1("Internshala")
    internshala.crawl_internshala(ids_present)

    #mongodb.delete_coll_data(['Internshala'])
    mongodb.update_session("Internshala")
    mongodb.insert_docs("Internshala",internshala_jobs)

'''







        
