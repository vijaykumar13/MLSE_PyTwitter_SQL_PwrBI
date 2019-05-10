import tweepy

import json
import pandas as pd
import pyodbc
from pandas.io import sql
from sqlalchemy import create_engine
from pandas.io.json import json_normalize


#Get your own Twitter keys
#--------------------------------------------------------------------------------
cKey =         "ENTER YOUR API KEY"
cSecret =      "ENTER YOUR API SECRET"
aToken =       "ENTER YOUR ACCESS TOKEN"
aTokenSecret = "ENTER YOUR ACCESS TOKEN SECRET"
#--------------------------------------------------------------------------------

auth = tweepy.OAuthHandler(cKey, cSecret)
auth.set_access_token(aToken, aTokenSecret)
api = tweepy.API(auth)


#Lets make a connection to Sql server Database 
engine = create_engine("mssql+pyodbc://MLSEDbUser:PA$$W0rd1/MLSETwitterTrends?driver=SQL+Server+Native+Client+11.0")



CountryWOEID = 23424775 #Canada
#CountryWOEID = 23424848 #India
Country_trends = api.trends_place(CountryWOEID) 
# Country_trends is a list with only one element in it, and make a dict which we'll put in data.
data = Country_trends[0] 
# grab the trends
trends = data['trends']
# grab the name from each trend
names = [trend['name'] for trend in trends]

# put all the names together with a 'linefeed' separating them
trendsName = '\n'.join(names)
print(trendsName)


for t in names:
    format_str = """INSERT INTO TwitterTrends (trend)
    VALUES ("{trend}"");"""

    sql_command = format_str.format(trend=t[0])
    cursor.execute(sql_command)

# time to commit and close the db connection
connection.commit()

connection.close()