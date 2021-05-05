#import the gpio pin module
import RPi.GPIO as GPIO
#import the module that returns date
from datetime import datetime
#import the module that return time
import time
#import the mysql connector that is used to connect to the db
import mysql.connector
#import the module that creates a thread that the script runs on
from threading import Event, Thread

# setting the waiting period of each read to 5 second.
WAIT_TIME_SECONDS = 5
gpio1 = 14
gpio2 = 15
gpio3 = 18
gpio4 = 17
gpio5 = 23
gpio6 = 24

mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="counter1234",
  database="counter"
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE TABLE counter (date VARCHAR(255), time VARCHAR(255), gpio1 VARCHAR(255), gpio2 VARCHAR(255), gpio3 VARCHAR(255), gpio4 VARCHAR(255), gpio5 VARCHAR(255), gpio6 VARCHAR(255))")

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# This class creates a thread that will repeat the function every 5 seconds
class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()
        
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0
counter5 = 0
counter6 = 0

def incrementcounter1(self):
    global counter1
    counter1 += 1
    print("counter 1 pulse detected")
def incrementcounter2(self):
    global counter2
    counter2 += 1
    print("counter 1 pulse detected")
def incrementcounter3(self):
    global counter3
    counter3 += 1
    print("counter 1 pulse detected")
def incrementcounter4(self):
    global counter4
    counter4 += 1
    print("counter 1 pulse detected")
def incrementcounter5(self):
    global counter5
    counter5 += 1
    print("counter 1 pulse detected")
def incrementcounter6(self):
    global counter6
    counter6 += 1
    print("counter 1 pulse detected")
    
# the if statement checks to make sure that none of the gpio have exceeded 999999
if counter1 < 999999 and counter2 < 999999 and counter3 < 999999 and counter4 < 999999 and counter5 < 999999 and counter6 < 999999:
    print("still going")
    GPIO.add_event_detect(gpio1, GPIO.RISING, callback=incrementcounter1)
    GPIO.add_event_detect(gpio2, GPIO.RISING, callback=incrementcounter2)
    GPIO.add_event_detect(gpio3, GPIO.RISING, callback=incrementcounter3)
    GPIO.add_event_detect(gpio4, GPIO.RISING, callback=incrementcounter4)
    GPIO.add_event_detect(gpio5, GPIO.RISING, callback=incrementcounter5)
    GPIO.add_event_detect(gpio6, GPIO.RISING, callback=incrementcounter6)   
else:
    #if any of the gpio pin count has exceeded 999999 the count is reset
    counter1 = 0
    counter2 = 0
    counter3 = 0
    counter4 = 0
    counter5 = 0
    counter6 = 0
    print("limit reached resetting")
# this method is used to add the count to the database
def addtoDb():
    print("Testing connection to db")    
    today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now()
    timenow = now.strftime("%H:%M:%S")
    try:
        # Executing the SQL command
        sql = "INSERT INTO counter (date, time, gpio1, gpio2, gpio3, gpio4, gpio5, gpio6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (today, timenow, counter1, counter2, counter3, counter4, counter5, counter6)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Data inserted")
    except:
        # Rolling back in case of error
        mydb.rollback()
    # Closing the connection
    #mydb.close()
# run the two methods at intervals of 5 second
rt = RepeatedTimer(WAIT_TIME_SECONDS, addtoDb)


