from pymongo import MongoClient
import os
import requests
import json
import csv
outputFile = open('test3.csv', 'w', newline='',encoding='utf-8-sig')
outputWriter = csv.writer(outputFile)

class DB():
    mongoUrl = config.get('DB','mongoUrl')
    print(mongoUrl)
    name = config.get('DB','name')
    password = config.get('DB','password')
    dbName = config.get('DB','dbName')
    collName = config.get('DB','collName')
    client = None
    db = None
    coll = None
    
    def connect(self):
        self.client = MongoClient(self.mongoUrl) # host uri 
        self.db = self.client[self.dbName] # Select the database
        self.db.authenticate(name=self.name,password=self.password)
        self.coll = self.db[self.collName]
    def close(self):   
        self.client.close()

class Member():
	name = None
	alias = None
	department = None
	email = None
	cuisine = None
	accompany = None
	greeting = None

	def __init__(self, name, alias, department, email, cuisine, accompany, greeting):
		self.name = name
		self.alias = alias
		self.department = department
		self.email = email
		self.cuisine = cuisine
		self.accompany = accompany
		self.greeting = greeting

class RegisterDB(DB):
    def __init__(self):
        self.connect()
    def register(self, name, alias, department, email, cuisine, accompany,greeting):
        newMember = Member(name, alias, department, email, cuisine, accompany, greeting)
        try:
            self.coll.insert(newMember.__dict__)
            print('success in register')
        except:
            print('failed in register')
#flash('failed in register')

        mail = RegisterMail(newMember)
        mail.send()
        print('register done')

    def login(self, alias):
        print('login done')

    def remove(self, alias):
        self.coll.remove({"alias": alias})
    def list(self):
        memberList = self.coll.find()
        for m in memberList: 
            outputWriter.writerow([m['name'],m['alias'],m['department'],m['email'],m['cuisine'],m['greeting'],m['accompany']])
if __name__=="__main__":
    print('start...')
    rdb = RegisterDB()
    rdb.list()
