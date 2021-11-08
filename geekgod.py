import concurrent.futures
import feedparser as fp
import re
import requests
import time

from bs4 import BeautifulSoup


class GeeksGod:

    def __init__(self):

        self.geeksgod_jobs = []


    def process_description(self, text):

        soup = BeautifulSoup(text, 'html.parser')

        desc=""
        
        try:
            for string in soup.stripped_strings:
                desc+=string
                desc+=" "
        except:
            print("NO DESCRIPTION.")

        return desc
    
    
    def desc_extract(self,url):
    
        page = requests.get(url)
        soup = BeautifulSoup(url.text,'html.parser')
        meta = str(soup.find('meta',{'property':'og:title'}))
    
        return meta
    
    
    def crawl_geeksgod_feed(self, ids_present):

        url_to_crawl = ["https://geeksgod.com/category/internships/feed/","https://geeksgod.com/category/campus-drives/feed/"]

        for url in url_to_crawl:
            
            feeds = fp.parse(url)
            for feed in feeds.entries:
                
                print("**************************")
                #print(feed)
                print("****************")

                print()
                print()

                job_id = feed.id.split('=')[1]
                if job_id in ids_present:
                    break

                try:
                    job_page_url = feed.link
                except:
                    job_page_url = " "

                try:
                    title = feed.title
                except:
                    title = " "
                
                #try:
                #    company_name = feed.tags[1]['term']
                #except:
                #    company_name = " "

                description = self.process_description(feed.content[0]['value'])
                if job_page_url!=" ":
                    short_title_desc = self.desc_extract(job_page_url)
                else:
                    short_title_desc = " "

                self.geeksgod_jobs.append({'url':job_page_url, 'job_id':job_id, 'title':title, 'company_name':" ",'experience':" ",'session':1, 'description':description,'short_desc':short_title_desc})

        return


'''
geeks = GeeksGod()

geeks.crawl_geeksgod_feed([])
print(geeks.geeksgod_jobs)
'''



