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


def createTimeline():
    global db

    result = db.execute("select tweetstb.createdAt, emotiontb.emotion from tweetstb inner join emotiontb on (tweetstb.tweetID = emotiontb.tweetID)")

    tList = []
    eList = []
        
    for i in result :
        dt  = i[0].strftime("%Y-%m-%d %H:%M:%S")
        emotion = i[1]
        tList.append(dt)
        eList.append(emotion)


        
    correct_list = f7(tList)

    for i in correct_list:
        db.insert("insert into count (createdAt, anger, disgust, fear, joy, sadness, surprise) values ('{0}','{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(i,0,0,0,0,0,0))
         
        
    # calculating each as every emotion count at a time stamp    

    for t, e in zip(tList, eList):
            
            
        if (e == "Anger"):
            angerValue = db.execute("select anger from count where createdAt = '{0}'".format(t))
            angerf = iterate(angerValue) + 1
            db.insert("update count set anger = '{1}' where createdAt  = '{0}'".format(t, angerf))
                

        elif(e == "Disgust"):
            disgustValue = db.execute("select disgust from count where createdAt = '{0}'".format(t))
            disgustf = iterate(disgustValue) + 1
            db.insert("update count set disgust = '{1}' where createdAt  = '{0}'".format(t, disgustf))
                

        elif(e == "Fear"):
            fearValue = db.execute("select fear from count where createdAt = '{0}'".format(t))
            fearf = iterate(fearValue) + 1
            db.insert("update count set fear = '{1}' where createdAt  = '{0}'".format(t, fearf))


        elif(e == "Joy"):
            joyValue = db.execute("select joy from count where createdAt = '{0}'".format(t))
            joyf = iterate(joyValue) + 1
            db.insert("update count set joy = '{1}' where createdAt  = '{0}'".format(t, joyf))



        elif(e == "Sadness"):
            sadnessValue = db.execute("select sadness from count where createdAt = '{0}'".format(t))
            sadnessf = iterate(sadnessValue) + 1
            db.insert("update count set sadness = '{1}' where createdAt  = '{0}'".format(t, sadnessf))

        else:
            surpriseValue = db.execute("select surprise from count where createdAt = '{0}'".format(t))
            surprisef = iterate(surpriseValue) + 1
            db.insert("update count set surprise = '{1}' where createdAt  = '{0}'".format(t, surprisef))
            

    angerl, disgustl, fearl, joyl, sadnessl, surprisel = createDataSet()

    return angerl, disgustl, fearl, joyl, sadnessl, surprisel

    

    
def iterate(output):

    for i in output:
        return i[0]

# function to remove duplicates
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def createDataSet():

    output = db.execute("select createdAt, anger, disgust, fear, joy, sadness, surprise from count")
    
    angerl, disgustl, fearl, joyl, sadnessl , surprisel = [],[],[],[],[],[]

    # storing emotion counts at each time stamp in above lists 
    
    for i in output:
    
        angerl.append([i[0].strftime("%Y-%m-%d %H:%M:%S"),i[1]])
        disgustl.append([i[0].strftime("%Y-%m-%d %H:%M:%S"),i[2]])
        fearl.append([i[0].strftime("%Y-%m-%d %H:%M:%S"),i[3]])
        joyl.append([i[0].strftime("%Y-%m-%d %H:%M:%S"),i[4]])
        sadnessl.append([i[0].strftime("%Y-%m-%d %H:%M:%S"),i[5]])
        surprisel.append([i[0].strftime("%Y-%m-%d %H:%M:%S"),i[6]])

    
    return angerl, disgustl, fearl, joyl, sadnessl, surprisel





