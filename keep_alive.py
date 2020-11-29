from flask import Flask, render_template, Markup
from threading import Thread

cmds = Markup("<h1>test</h1>")

def passcmd(cmd):
  a = cmd.replace("[", "")
  b = a.replace("'", "")
  c = b.replace("]", "")
  global cmds 
  cmds = Markup(c)

app = Flask('')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/commands')
def cmd():
    return render_template('commands.html', val = cmds)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()