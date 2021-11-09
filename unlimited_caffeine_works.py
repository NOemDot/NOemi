import os
import time
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Star Platinum, The world!"

def run():
  app.run(host='0.0.0.0',port=8080)

def caffeine():
    t = Thread(target=run)
    t.start()

def run_lavalink():
  os.system("java -jar Lavalink.jar")

def tea():
  t = Thread(target=run_lavalink)
  t.start()
