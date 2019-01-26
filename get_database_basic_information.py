# -*- coding: utf-8 -*-
# @Time    : 2019/01/26 20:52
# @Author  : Ramble Dong
# @File    : get_database_basic_information.py

from pymongo import MongoClient
import numpy as np
import pprint
import pandas as pd


# set the global variable
# connect the database of cloud servers
client = MongoClient(
    host='113.108.181.146',
    port=27701, username='aduser1',
    password='ok1b8W@8YKg3P8%i'
)

# see the list of database names
db_names = client.list_database_names()
print(db_names)

# the way to get databases
trade_record_database = client["trade_record_database"]
tick_record_database = client["tick_record_database"]
strategy_status = client["strategy_status"]

# the way to get the collection names list of a database
coll_names_trade = trade_record_database.list_collection_names(session=None)
coll_names_tick = tick_record_database.list_collection_names(session=None)
coll_names_strategy = strategy_status.list_collection_names(session=None)
print(coll_names_trade)
print(coll_names_tick)
print(coll_names_strategy)

# get the document of a collection and there are other functions
# SH601390 = tick_record_database["601390.SH"]
# for post in SH601390.find():
#       pprint.pprint(post)
trade_collection = trade_record_database["trade"]
# print the first document
pprint.pprint(trade_collection.find_one())

# get the number of documents
print(trade_collection.count_documents({}))

# convert the collection to dataframe
data = pd.DataFrame(list(trade_collection.find()))
print(data)
