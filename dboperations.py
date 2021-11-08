# includes methods to query mongodb databases.


# importing python packages
from pymongo import MongoClient, collection
from pprint import pprint

# importing from user-developed module
from dbconnections import DbConnections
#from dbconnections import NeoConnections


# W R I T E    M E T H O D    T O    C L O S E    M O N G O     C O N N E C T I O N


class MongoDB:

    def __init__(self, db_name):

        # instantiating and establishing connection with database
        mongodb_open = DbConnections(db_name)
        self.db = mongodb_open.client[db_name]
        print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")


    def insert_docs(self, coll, documents=[]):

        """ insert data in given collection """
        collection = self.db[coll]
        print("???????????????????????????????????????????????????????????????????????????????????????")
        print(documents)
        print("???????????????????????????????????????????????????????????????????????????????????????")
            
        try:
            collection.insert_many(documents,ordered=False)
            print("Inserted Succesfully")
            return True
        except Exception as e:
            print("55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")
            print("Mongodb exception:", e)
            return False
        
        '''
        doc_count = 0
        total_docs = len(documents)
        
        while doc_count < total_docs:
            try:
                collection.insert_many(documents[doc_count])
                print("Inserted Succesfully document with index  -------->    ",doc_count)
            except Exception as e:
                print("55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")
                print("Duplicate Value")
            finally:
                doc_count+=1
                
        return
        '''
        
    def delete_coll_data(self, colls: list):
        """ delete all data in the collections passed in colls list """
        for coll in colls:
            collection = self.db[coll]
            try:
                collection.delete_many({})
                print("Deleted everything in %s" % (coll))
            except Exception as e:
                print(e)
    

    def extract_ids_session1(self, coll, query):

        collection = self.db[coll]
        try:
            job_ids = collection.find(query,{"job_id":1,"_id":0})
            print("Succesfully extracted.")
            ids = []
            for i in job_ids:
                ids.append(i["job_id"])
            return ids
        except Exception as e:
            print(e)

    
    def update_session(self, coll):

        collection = self.db[coll]
        try:
            collection.update_many({},{"$inc":{"session":1}})
            print("Successfully Updated the Session Values.")
        except Exception as e:
            print("Some Error Occurred while incrementing Session value.")
            print(e)
            
            
    
    def extract_description(self, coll):
    
        collection = self.db[coll]
        try:
            job_descriptions = collection.find({},{"description":1,"_id":0})
            print("Succesfully extracted.")
            descriptions = []
            for i in job_descriptions:
                descriptions.append(i["description"])
            return descriptions
        except Exception as e:
            print(e)
            
            
    def fetch_doc(self,coll,id):
    
        collection = self.db[coll]
        try:
            job_descriptions = collection.find({},{"url":1,"_id":0,"job_id":1})
            print("Succesfully extracted.")
            descriptions = []
            for i in job_descriptions:
                print(i)
        except Exception as e:
            print(e)
            
            
    def extract_urls(self, coll, query):

        collection = self.db[coll]
        try:
            job_ids = collection.find({},{"job_id":1,"job_url":1,"_id":0})
            print("Succesfully extracted.")
            ids = []
            for i in job_ids:
                ids.append((i["job_id"],i["job_url"]))
            return ids
        except Exception as e:
            print(e)
            
            
    def update_docs(self, coll, docs):

        collection = self.db[coll]
        try:
            for job_id, desc in docs:    
                collection.update_one({"job_id":job_id},{"$set":{"description":desc}})            
        except Exception as e:
            print("Some Error Occurred while incrementing Session value.")
            print(e)
            
            
    def extract_docs(self, coll):
    
        collection = self.db[coll]
        try:
            job_descriptions = collection.find({},{"_id":0})
            print("Succesfully extracted.")
            return job_descriptions
        except Exception as e:
            print(e)
            
    
        
    
    
class Neo4j:

    def __init__(self):
        self.neo4j=NeoConnections()
        
        
    def create_job_node(self):
    
        self.job_node = """unwind $properties as props merge (n:JOB{job_id:props.job_id}) on create set n = {job_id:props.job_id, job_title:props.job_title, company_name:props.company_name, job_url:props.job_url}"""
    
    def create_job_entities(self):
    
        self.job_entity = """unwind $properties as props merge(n:JOB_ENTITIES{name:props.name}) on create set n = {name:props.name,status:props.status}"""
    
    def create_tech_rel(self):
    
        self.tech_skill_rel = """ unwind $properties as props match(n:JOB{job_id:props.job_id}),(p:JOB_ENTITIES{name:props.name}) merge (n)-[:REQUIRES_TECH_SKILL]->(p)"""
        
    def create_soft_rel(self):
    
        self.soft_skill_rel = """ unwind $properties as props match(n:JOB{job_id:props.job_id}),(p:JOB_ENTITIES{name:props.name}) merge (n)-[:REQUIRES_SOFT_SKILL]->(p)"""
        
    def create_subject_rel(self):

        self.subject_rel = """ unwind $properties as props match(n:JOB{job_id:props.job_id}),(p:JOB_ENTITIES{name:props.name}) merge (n)-[:REQUIRES_DEGREE_IN]->(p)"""

    def create_degree_rel(self):

        self.degree_rel = """ unwind $properties as props match(n:JOB{job_id:props.job_id}),(p:JOB_ENTITIES{name:props.name}) merge (n)-[:REQUIRES_DEGREE]->(p)"""    
            
    def create_job_title_rel(self):
    
        self.job_title_rel = """ unwind $properties as props match(n:JOB{job_id:props.job_id}),(p:JOB_ENTITIES{name:props.name}) merge (n)-[:JOB_TITLE]->(p)"""  


        
    
    



'''

m = MongoDB("Job_Collector")
x=m.extract_urls("Naukri")
print(x)

'''




