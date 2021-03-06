import RPi.GPIO as GPIO
import time
from flask import Flask, render_template
import threading
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer = 4
GPIO.setup(buzzer,GPIO.OUT)
czujnik = 18
GPIO.setup(czujnik,GPIO.IN)

go = False
iloscwejscdzis = 0
today = "NULL"
status = 0

app = Flask(__name__)

def start():
   for pulse in range(60):
      GPIO.output(buzzer, True)
      time.sleep(0.00042)
      GPIO.output(buzzer, False)
      time.sleep(0.00042)
   time.sleep(0.02)
   for pulse in range(60):
      GPIO.output(buzzer, True)
      time.sleep(0.00037)
      GPIO.output(buzzer, False)
      time.sleep(0.00037)
   time.sleep(0.02)
   for pulse in range(60):
      GPIO.output(buzzer, True)
      time.sleep(0.00032)
      GPIO.output(buzzer, False)
      time.sleep(0.00032)
   time.sleep(0.02)

def stop():
   for pulse in range(60):
      GPIO.output(buzzer, True)
      time.sleep(0.00032)
      GPIO.output(buzzer, False)
      time.sleep(0.00032)
   time.sleep(0.02)
   for pulse in range(60):
      GPIO.output(buzzer, True)
      time.sleep(0.00037)
      GPIO.output(buzzer, False)
      time.sleep(0.00037)
   time.sleep(0.02)
   for pulse in range(60):
      GPIO.output(buzzer, True)
      time.sleep(0.00042)
      GPIO.output(buzzer, False)
      time.sleep(0.00042)
   time.sleep(0.02)

def savelog():
    now = datetime.now()
    tosave = now.strftime("%d-%m-%Y %H:%M:%S")
    f = open("/home/czujnik/log/log.txt", "a")
    f.write("\n"+tosave)
    f.close()
    
def wejsciadzis():
    data = datetime.now()
    teraz = data.strftime("%d-%m-%Y")
    global iloscwejscdzis
    iloscwejscdzis = 0
    f = open("/home/czujnik/log/log.txt")
    #with list(open("/home/czujnik/log/log.txt")) as f:
    for line in reversed(list(f)):
        datawejscia = line[0:10]
        if (datawejscia == teraz):
            iloscwejscdzis += 1
        else:
            break
    f.close()
    
def check_date():
    global today
    date = datetime.now()
    now = date.strftime("%d-%m-%Y")
    if not (today == now):
        today = now
        return False
    else:
        return True

def beep(repeat):
   for i in range(0, repeat):
      for pulse in range(60):
         GPIO.output(buzzer, True)
         time.sleep(0.00046)
         GPIO.output(buzzer, False)
         time.sleep(0.00046)
      time.sleep(0.02)

def startczujnika(arg):
    global iloscwejscdzis
    while True:
        n=GPIO.input(18)
        if n==1:
            if (status == 1):
                beep(3)
            savelog()
            iloscwejscdzis += 1
            time.sleep(1)
        global go
        if (go == False):
            break
        else:
            time.sleep(0.1)

@app.route('/')
def index():
    global go
    global iloscwejscdzis
    if not check_date():
        wejsciadzis()
    dane = {
       'status' : go,
       'ilosc' : iloscwejscdzis,
       'data' : today,
    }
    return render_template('main.html', **dane)
    
@app.route("/<akcja>")
def action(akcja):
    global go
    global iloscwejscdzis
    global pobranadata
    global status
    if not check_date():
        wejsciadzis()
    if (akcja == "on"):
        if (go==False):
          go = True
          status = 1
          x = threading.Thread(target=startczujnika, args=(0,))
          x.start()
          start()
    if (akcja == "off"):
        if (go==True):
          go = False
          time.sleep(0.25)
          if(status == 1):
              stop()
              time.sleep(0.25)
          status = 0
    if (akcja == "silent"):
        go = True
        status = 2
        x = threading.Thread(target=startczujnika, args=(0,))
        x.start()
        
    dane = {
       'status' : status,
       'ilosc' : iloscwejscdzis,
       'data' : today,
    }     
    return render_template('main.html', **dane)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
