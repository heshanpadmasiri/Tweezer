from flask import Flask , render_template , url_for, request
import pyodbc
from flask_cors import CORS, cross_origin
from streamnew import streaming
from piechart import percentage
from timeline import createTimeline
from worldmap import createMap

#creating the database connection
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

db = DB()


app = Flask(__name__)
CORS(app)

#home page
@app.route('/',methods=['GET' , 'POST'])
def home():
    global db
    
    if request.method == 'POST':
        
        #fetch form data
        keyword = request.form['keyword']

        #delete existing data in tables before the new keyword is searched
        
        db.insert("delete from emotiontb")    
        db.insert("delete from tweetstb")
        db.insert("delete from count")
        db.insert("delete from percentagetb")

        
        streaming(str(keyword))    #streaming the keyword from twitter
        percentage()            #calculating emotion percentages
        
        
    else:
        #display nothing in tabs if no keyword is searched
        db.insert("delete from emotiontb")    
        db.insert("delete from tweetstb")
        db.insert("delete from count")
        db.insert("delete from percentagetb")

        
    return render_template('index.html')

#map page
@app.route("/map")
def worldmap():
    global db
    coordinate_list = createMap()    # retrieve the list of tweets with coordinates 
    return render_template("map.html", coordinate_list= coordinate_list)

#timeline page
@app.route("/timeline")
def timeline():
    global db

    #retrieve lists containing emotion counts
    anger, disgust , fear, joy , sadness , surprise = createTimeline()

    
    return render_template("timeline.html", anger=anger, disgust = disgust, fear = fear, joy = joy, sadness = sadness, surprise = surprise)
   

#tweets page
@app.route("/tweets")
def tweets():
    global db

    #retrieving details of tweets in order to represent in the table
    resultValue = db.execute("select tweetstb.createdAt, tweetstb.tweet, emotiontb.emotion from tweetstb inner join emotiontb on (tweetstb.tweetID = emotiontb.tweetID)")
   
    return render_template("tweets.html", resultValue = resultValue)


#pie chart page
@app.route("/piechart")
def piechart():
    global db
       
    output = db.execute("Select * from percentagetb")   #retrieving emotion percentages from the database
    percentage_list = [(r[0],round(r[1], 2)) for r in output]
    
    return render_template("piechart.html" , percentage_list = percentage_list )



if __name__ == "__main__":
    app.run(debug=True, threaded=True)           #start the web server
