import boto3
import datetime
import requests
import subprocess
import time
import threading
import os
from fabric import Connection
from dotenv import load_dotenv

load_dotenv()


class Automate:

    def __init__(self):
        
        self.ner_instance_id = os.getenv('NER_INSTANCE_ID')
        self.region_name = os.getenv('REGION_NAME')
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.ec2_username = os.getenv('EC2_USERNAME ')
    
    def crawler(self):
        
        from Central import Center
        
        file = open("crawler_log.txt","a")
        file.write("\n")
        file.write("Starting crawler at: ")
        file.write(str(datetime.datetime.now()))
        file.write("\n")
        file.close()
        center = Center()
        center.multithread()
        file = open("crawler_log.txt","a")
        file.write("Stopped crawler at: ")
        file.write(str(datetime.datetime.now()))
        file.write("\n")
        file.write("  -----------------------------------------------------------  ")
        file.close()
        return
        
        
        
    def start_server(self,conn):
        with conn.cd('singular_jobs/singular_jobs_ner'):
            conn.run('ls')
            conn.run('python3 manage.py runserver 0.0.0.0:8000')
        return
    
    def send_request(self,url):
        result = requests.get(url)        
        print(url)
        print(result)
        
        return
       
    def ner(self):
    
        #start ec2_instance
        
        file = open("ner_log.txt","a")
        file.write("\n\n")
        header_msg = "Lifecycle of EC2 instance with instance id = "+f"{self.ner_instance_id}"+"\n\n"
        file.write(header_msg)
        
        ec2 = boto3.client('ec2', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name=self.region_name)
        print(ec2.meta.region_name)
        
        try:
            print("Startig at: ")
            file.write("Starting at: ")
            file.write(str(datetime.datetime.now()))
            file.write("\n")
            ec2.start_instances(InstanceIds=[self.ner_instance_id])
            file.write("Started at: ")
            file.write(str(datetime.datetime.now()))
            file.write("\n")
        except Exception as e:
            print("BOTO3 EXCEPTION:")
            print(e)
            file.write("Starting failed because: ")
            file.write(str(e))
            file.write("\n")
            
            file.close()
            return
        
            
        time.sleep(30)
        
        
        # access instance ip address
        #ip = self.extract_ip
        
        reservations = ec2.describe_instances(InstanceIds=[self.ner_instance_id]).get("Reservations")

        for reservation in reservations:
            print(reservation)
            for instance in reservation['Instances']:
                #print(instance.get("PublicIpAddress"))
                ip = instance.get("PublicIpAddress")
        
        print("####################")
        print(ip)
        print(type(ip))
        
        file.write("New IP addres: ")
        file.write(str(ip))
        file.write("\n")
        
        host_ip = ip.replace(".","-")
        host = "ec2-"+f"{host_ip}"+".ap-south-1.compute.amazonaws.com"
        print(host)
        print(self.ec2_username)
        try:
            
            file.write("Establishing remote connection with the EC2 instance using fabric at: ")
            file.write(str(datetime.datetime.now()))
            file.write("\n")
                       
            conn = Connection(
                host=host,
                user="ubuntu",
                connect_kwargs={
                    "key_filename": "singular_jobs.pem",
                }
            )
            
            file.write("Successfully established connection with the EC2 instance at: ")
            file.write(str(datetime.datetime.now()))
            file.write("\n")
            
        except Exception as e:
            print("Deployment was unsuccessful.\nError:\n")
            print(e)
            file.write("Connection setup failed due to: ")
            file.write(e)
            file.write("\n")
            
            file.close()
            return
        
        '''
        url = "http://"+f"{ip}"+":8000"+"/jobs_ner/start_ner/"
        
        
        t1 = threading.Thread(target=self.start_server,args=(conn,))
        t2 = threading.Thread(target=self.send_request,args=(url,))
        
        
        t1.start()
        
        file.write("starting ner django server at: ")
        file.write(str(datetime.datetime.now()))
        file.write("\n")
        
        time.sleep(10)
        print("MOVING")
        
        file.write("Calling NER API at: ")
        file.write(str(datetime.datetime.now()))
        file.write("\n")
        
        t2.start()        
        t2.join()
        '''
        
        file.write("NER work started at: ")
        file.write(str(datetime.datetime.now()))
        file.write("\n")
        
        try:
            with conn.cd("/job_collector"):
                conn.run("ls")
                conn.run("python3 Central.py",warn=True)
                print("cron completed successfully.")
        except Exception as e:
            print("Some error occured while executing NER")
            file.write("Error Occured in NER: ")
            file.write(str(e))
            file.write("\n")
        

        print("Checking if SSH still exists: ")
        try:
            with conn.cd("/job_collector"):
                conn.run("ls")
                print("ls executed successfully. SSH exisits")
        except Exception as e:
            print(e)
            print("SSH does not exists.")

        file.write("NER work ended at: ")
        file.write(str(datetime.datetime.now()))
        file.write("\n")
                
        print("ANSH    PRANJULLLLL    MAAMAAAA")   
        #url = "http://"+f"{ip}"+":8000"+"/jobs_ner/start_ner/"
       
        '''
        file.write("Killing ner django server at: ")
        file.write(str(datetime.datetime.now()))
        file.write("\n")
        conn.run("sudo pkill -f runserver")
        '''
        
        try:
            print("Starting EC2")
            file.write("Killing the EC2 instance at: ")
            file.write(str(datetime.datetime.now()))
            file.write("\n")
            ec2.stop_instances(InstanceIds=[self.ner_instance_id])        
        except Exception as e:
            print("BOTO3 EXCEPTION:")
            print(e)
            file.write("EC2 instance could not be stopped because : ")
            file.write(e)
            file.write("\n")
            
        file.write("\n")
        file.write("                -----------------------------------------------------------------------------------------------             \n\n")
        print("DONE ALL THE TASKS.")
        file.close()
        
    
    # call backend deployed at heroku.
    def create_new_jobs(self):

        file = open("job_creation.txt","a")
        file.write("\n\n")
        file.write("Starting to predict suitable jobs at: ")
        file.write(str(datetime.datetime.now()))
        file.write("\n")
        
        status = requests.get("https://singularjobapi.herokuapp.com/user_account/new_jobs/")
        
        file.write("Status returned: ")
        #file.write(status)
        file.write("Predicting jobs completed at: ")
        file.write(str(datetime.datetime.now()))
        file.write("\n")
        
        return


    def update_neo4j_job_session(self):
    
        file = open("job_creation.txt","a")
        file.write("\n\n")
        file.write("Updating neo4j job nodes session value at: ")
        file.write(str(datetime.datetime.now()))
        file.write("\n")
        
        status = requests.get("https://singularjobapi.herokuapp.com/user_account/update_neo4j_session/")
        
        file.write("Status returned: ")
        file.write("Updation completed at: ")
        file.write(str(datetime.datetime.now()))
        
        return
    
    
    
if __name__=='__main__':

    automate = Automate()
    automate.crawler()
    time.sleep(30)
    automate.update_neo4j_job_session()
    
    time.sleep(100)
    '''
    try:
        result = subprocess.run(["sudo","kill","-9","$(sudo","lsof","-t","-i:22"])
        print(result)
        print("successfully killed process on port 22")
    except Exception as e:
        print("Could not kill process on port 22 because: \n")
        print(e)
    '''
    #automate.ner()
    #time.sleep(10)
    #automate.create_new_jobs()
