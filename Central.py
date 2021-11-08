import concurrent.futures
import threading
import time

from dboperations import MongoDB
from geekgod import GeeksGod
from intern import Internshala
from naukri2 import Naukri
from linkedin import Linkedin


class Center:

    def __init__(self):

        self.mongodb = MongoDB("Job_Collector")
        #self.mongodb.delete_coll_data(["Linkedin"])
        self.job_boards = ["Linkedin"]
        #"Internshala","Indeed","Naukri"
        #,"Internshala","GeeksGod","Naukri"

    def indeed(self):
        
        print("YYYYEEEEEEEEEEEEEEEEEEEESSSSSSSSSSSSSSSSSSSSSSS")
        indeed_posts = Indeed()

        ids_present = self.mongodb.extract_ids_session1("Indeed", {})
        indeed_posts.crawl_indeed('computer science internship', 'india', ids_present)
        
        indeed_jobs = indeed_posts.indeed_jobs

        self.mongodb.update_session("Indeed")
        print(indeed_jobs)
        self.mongodb.insert_docs("Indeed",indeed_jobs)

        return 


    def naukri(self):

        naukri_posts = Naukri()
        print("ttttttttttttttttttttttttttttttttttttttttttt")
        ids_present = self.mongodb.extract_ids_session1("Naukri", {})
        print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        naukri_posts.crawl_naukri(ids_present)
        
        naukri_jobs = naukri_posts.naukri_jobs

        self.mongodb.update_session("Naukri")
        print(naukri_jobs)
        self.mongodb.insert_docs("Naukri",naukri_jobs)

        return

    def internshala(self):
        time.sleep(60)
        internshala_posts = Internshala()

        ids_present = self.mongodb.extract_ids_session1("Internshala",{})
        internshala_posts.crawl_internshala(ids_present)
        
        internshala_jobs = internshala_posts.internshala_jobs

        self.mongodb.update_session("Internshala")
        print(internshala_jobs)
        self.mongodb.insert_docs("Internshala",internshala_jobs)

        return


    def linkedin(self):
    
        time.sleep(60)
        linkedin_posts = Linkedin()

        ids_present = self.mongodb.extract_ids_session1("Linkedin",{})
        linkedin_posts.crawl_linkedin(ids_present)
        
        linkedin_jobs = linkedin_posts.linkedin_jobs

        self.mongodb.update_session("Linkedin")
        print(linkedin_jobs)
        self.mongodb.insert_docs("Linkedin",linkedin_jobs)

        return

    
    def geekgod(self):

        geeksgod_posts = GeeksGod()

        ids_present = self.mongodb.extract_ids_session1("GeeksGod",{})
        
        geeksgod_posts.crawl_geeksgod_feed(ids_present)
        
        geeksgod_jobs = geeksgod_posts.geeksgod_jobs

        self.mongodb.update_session("GeeksGod")
        time.sleep(5)
        #print(geeksgod_jobs)
        self.mongodb.insert_docs("GeeksGod",geeksgod_jobs)

        return 

        
    def distribute(self, job_board):

        if job_board=="Internshala":
            self.internshala()
        elif job_board=="Naukri":
            self.naukri()
        elif job_board=="Indeed":
            self.indeed()
        elif job_board=="GeeksGod":
            self.geekgod()
        elif job_board=="Linkedin":
            self.linkedin()


    def multithread(self):

        start_time =  time.time()
        print("YES")
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                {executor.submit(self.distribute, job_board):job_board for job_board in self.job_boards}
            
        print(time.time()-start_time)
        
  

if __name__=="__main__":

    center = Center()
    center.multithread()
    
    
