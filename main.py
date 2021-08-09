# https://aryaboudaie.com/python/technical/educational/web/flask/2018/10/17/flask.html
#
# TODO p
import os
import json
from flask import Flask, session, request, redirect, send_from_directory, abort
app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config['SESSION_TYPE'] = 'filesystem'

assets = os.path.join(os.getcwd(), "assets")

messages = [ { "id": 0, "username": "God", "message": "Welcome" } ];

@app.route('/messages')
def getMessages():
  return json.dumps(messages)

@app.route('/me')
def getMe():
  print("getMe", session)
  if "me" not in session:
    print("no me")
    return abort(403, "User is not logged in")

  me = session["me"]
  
  return json.dumps(me)

@app.route('/message', methods=['POST'])
def sendMessage():
  if not 'username' in session:
    return "Please login", 400
  
  username = session['username']
  message = request.form['message']

  ownedMessage = {
    "username": username,
    "message": message
  }
  
  messages.append(ownedMessage)
    
  return redirect("/")

@app.route('/login', methods=['POST'])
def login():
  print("login", request.data)

  content = request.get_json(force = True)
  if "username" in content:
    user = { "username": content['username'] }
  else:
    user = { "username": "Anonymous" }  

  session['me'] = user
    
  return json.dumps(user)

@app.route('/logout', methods=['POST'])
def logout():
  print("logout")
  session.clear()
  return json.dumps({})

@app.route('/')
def home():
    print("home")
    return send_from_directory(assets, 'index.html')

@app.route('/favicon.ico')
def favicon():
    print("favicon")
    return send_from_directory(assets, 'star.ico')
  
@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory(assets, path)


if __name__ == '__main__':
  app.run(host='0.0.0.0')


