from email import contentmanager
import typing
import csv
import codecs
import urllib.request
import urllib.error
import pandas
import sys

class API_Reading():
    
    def __init__(self, BASE_URL, API_KEY, LOCATION, START_DATE, END_DATE, UNIT_GROUP, CONTENT_GROUP, INCLUDE):
        self.base_url = BASE_URL
        self.api_key = API_KEY
        self.location = LOCATION
        self.start_date = START_DATE
        self.end_date = END_DATE
        self.unit_group = UNIT_GROUP
        self.content_group = CONTENT_GROUP
        self.include = INCLUDE
        self.api_query = str()
        
    def create_api(self):
        self.api_query = self.base_url + self.location
        if(len(self.start_date)):
            self.api_query += "/" + self.start_date
            if(len(self.end_date)):
                self.api_query += "/" + self.end_date
        self.api_query += "?"
        if(len(self.unit_group)):
            self.api_query += "&unitGroup=" + self.unit_group
        if(len(self.content_group)):
            self.api_query += "&contentType=" + self.content_group
        if(len(self.include)):
            self.api_query += '&include='+self.include
        self.api_query += "&key="+self.api_key
    
    def run_api(self):
        
        try:
            CSV_Bytes = urllib.request.urlopen(self.api_query)
        except urllib.error.HTTPError as e:
            print("Can't process now! Failed load query")
            sys.exit()
        except urllib.error.URLError as e:
            print("Can't process now! Failed load query")
            sys.exit()
        
        CSVText = pandas.DataFrame(csv.DictReader(codecs.iterdecode(CSV_Bytes, 'utf-8'), delimiter=','))
        #print(CSVText.head())
        if(len(CSVText.datetime) == 0): 
            print("Can't process now! Failed to load CSV")
            sys.exit()
        return CSVText