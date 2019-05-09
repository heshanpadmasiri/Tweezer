import tweepy
import sys
import re
import pyodbc
import datetime
import pandas as pd
import os
os.environ['KERAS_BACKEND'] = 'theano'
from emotion_predictor import EmotionPredictor

class DB:
    def __init__(self):
        self.server = 'tcp:twitter-server.database.windows.net'
        self.database = 'twitter_db' 
        self.username = 'thilakshi' 
        self.password = 'tikiz<3kav' 
        self.cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:twitter-server.database.windows.net,1433;Database=twitter_db;Uid=thilakshi@twitter-server;Pwd=tikiz<3kav;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        self.cursor = self.cnxn.cursor()

    def getConnection(self):
        return self.cursor

    def execute(self,query):
        self.cursor.execute(query)
        return self.cursor

    def insert(self,query):
        self.cursor.execute(query)
        self.cnxn.commit()
        return self.cursor
    
#Create the DB connection
db = DB()

# Pandas presentation options
pd.options.display.max_colwidth = 150   # show whole tweet's content
pd.options.display.width = 200          # don't break columns
# pd.options.display.max_columns = 7      # maximal number of columns


# Predictor for Ekman's emotions in multiclass setting.
model = EmotionPredictor(classification='ekman', setting='mc', use_unison_model=True)


def streaming(keyword):
    global db
    
    #consumer key, consumer secret, access token, access secret.
    consumer_key = "yzcqdp3QZmKQrrZfNNTmozUQb"
    consumer_secret = "3hVqVKHgP10SBhNSlcRAY5na6nBpQco5MqkhaK9ajUpHO1WIq0"
    access_token = "1085530428063150080-6zJrB79K09jQFgQ34NtmDZRHMIaoJM"
    access_secret = "ETRshaLITFSEKIhlfFwcpVF8daO1EDJHEAPAQ5bh1NxVZ"

    #Authenticate the app using Twitter API key and secret

    auth  = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)

    api  = tweepy.API(auth)

    #Collecting the tweets by given keyword

    #Collect 300 tweets for analyze(3 api calls)

    
    public_tweets = api.search(keyword,lang='en',tweet_mode='extended',count='100' )
    #public_tweets += api.search(keyword,lang='en',tweet_mode='extended',count='100' )
    

    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    cleaned_tweets = []
    timelist = []



    for tweet in public_tweets:
        
        #cleaning tweet
        text = tweet.full_text.translate(non_bmp_map)
        cleantext = preprocess(text)

        #getting the date when tweet was published
        datetime_ = str(tweet.created_at)
        twitId = tweet.id_str

        #checking for location by locating longitude and latitude
        coordinateX = None  
        coordinateY = None
        
        coordinate = tweet.coordinates
        
        if (coordinate != None) :
            coordinateX = str(coordinate.get('coordinates')[0])  
            coordinateY = str(coordinate.get('coordinates')[1])

            
        
        t = datetime.datetime.strptime(datetime_, "%Y-%m-%d  %H:%M:%S")

        if(len(cleantext))< 140:
        
            query="insert into tweetstb (tweetID, tweet,createdAt,lang,longi) values ('{0}','{1}','{2}','{3}','{4}')".format(twitId, cleantext,t.strftime('%Y-%m-%d %H:%M:%S'),coordinateY,coordinateX)
            
            db.insert(query)
            
    sentiment()  

# funcion to clean tweet
def preprocess(tweet):

     #removing "RT" string from tweets
    tweet = tweet.replace("RT","")
    
    tweet = tweet.replace("'","\\")

    #removing urls from tweet
    
    tweet = re.sub(r"http\S+", "", tweet)
    
    
    #removing numbers from tweets
    tweet = re.sub('[0-9]+', '', tweet)
    
    return tweet
    


def sentiment():
    global db
    tweets = []
    ids = []
    output = db.execute("Select * from tweetstb")
    items = [[r[0],r[1]] for r in output]

    for i in items :
        ids.append(i[0])
        tweets.append(i[1])
    
    #feeding tweets to the emotion analyze algorithm
    predictions = model.predict_classes(tweets)
    emotion_list = predictions["Emotion"].tolist()
    
    #saving the emotion of tweets in database
    for (i, e) in zip(ids, emotion_list):
        query = "insert into emotiontb (tweetID, emotion) values ('{0}','{1}')".format(i, e)
        db.insert(query)

    


