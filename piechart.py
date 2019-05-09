import pyodbc


class DB:
    def __init__(self):
        self.server = 'tcp:twitter-server.database.windows.net'
        self.database = 'twitter_db' 
        self.username = 'thilakshi' 
        self.password = 'tikiz<3kav' 
        self.cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:twitter-server.database.windows.net,1433;Database=twitter_db;Uid=thilakshi@twitter-server;Pwd=tikiz<3kav;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
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

#calulating percentages for each emotions

def percentage():
    global db
    
    output = db.execute("Select emotion from emotiontb")
    emotionList = []

    for e in output:
        emotionList.append(e[0])

        
    list_len = len(emotionList)
    anger_count = 0
    disgust_count = 0
    fear_count = 0
    joy_count = 0
    sadness_count = 0
    surprise_count = 0

    #calculating tweet count for each emotion
    
    for e in emotionList:
        if (e == "Anger"):
            anger_count+=1
            
        elif(e == "Disgust"):
             disgust_count+=1

        elif(e == "Fear"):
             fear_count+=1
        
        elif(e == "Joy"):
             joy_count+=1
    
        elif(e == "Sadness"):
             sadness_count+=1

        else:
             surprise_count+=1

    try:
        #calculating the percentage of tweet count for each emotion
        
        anger_perc = round((anger_count/list_len)*100 , 2)
        disgust_perc = round((disgust_count/list_len)*100 , 2)
        fear_perc = round((fear_count/list_len)*100, 2)
        joy_perc = round((joy_count/list_len)*100, 2)
        sadness_perc = round((sadness_count/list_len)*100, 2)
        surprise_perc = round((surprise_count/list_len)*100 ,2)

    except (ZeroDivisionError):
        pass

    else:

        emotion_dict = {"Anger" : anger_perc , "Disgust" : disgust_perc ,
                    "Fear" : fear_perc , "Joy" : joy_perc, "Sadness" : sadness_perc , "Surprise" : surprise_perc}      


        #inserting percentages of each emotion to the database
        
        for key in emotion_dict :
            query = "insert into percentagetb (emotion , percen) values ('{0}','{1}')".format(key, emotion_dict[key])
            db.insert(query)

      
    





