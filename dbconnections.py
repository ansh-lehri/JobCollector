# central file to create connection pool for Server and Compressor database which 
# every process of crawler can use.

from pymongo import MongoClient
from pprint import pprint
#from neo4j import GraphDatabase, basic_auth


class DbConnections:

    def __init__(self, db_name):
        """ connect to database """
        try:
            self.client = MongoClient(
                "mongodb+srv://job_collector:JobCollector25050206@cluster0.rgbts.mongodb.net/%s?retryWrites=true&w=majority" % (
                    db_name)
            )
            print("Connection established to online mongodb.")

        except Exception as e:
            print(e)
            print("Online db not available. Connecting to local mongodb")
            self.client = MongoClient()



class NeoConnections:

    def __init__(self):

        try:
            self.driver = GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j", "Kheri@123"))
            print("Successfully established connection with Neo4j")
        except Exception as e:
            print("Neo4j Error")
            print(e)