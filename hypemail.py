from O365 import Account
from O365.message import Message
from O365.mailbox import MailBox
from O365.mailbox import Message
import random
import requests
from flask import Flask,request, redirect, render_template
from tinydb import TinyDB, Query

app = Flask(__name__)

db = TinyDB('db.json') 

CLIENT_ID = '5c03807f-4363-4c78-ac85-2f903305d917'
CLIENT_SECRET = 'Eri07B8vVW:HQQ/_eNX4tNeEKl-wPVy['
credentials = (CLIENT_ID, CLIENT_SECRET)



#account = Account(credentials)
#if account.authenticate(scopes = ['basic', 'message_all']):
 #   print('Authenticated!')


#@app.route('/')
#def hello_world():
#    return 'Hello, World!'


@app.route('/')
def auth_step_one():
    
    callback = 'http://127.0.0.1:5000/steptwo'
    scopes = ['https://graph.microsoft.com/Mail.ReadWrite', 'https://graph.microsoft.com/Mail.Send', 'https://graph.microsoft.com/Offline.Access', 'https://graph.microsoft.com/User.Read']
    account = Account(credentials, scopes = ['https://graph.microsoft.com/Mail.ReadWrite', 'https://graph.microsoft.com/Mail.Send', 'https://graph.microsoft.com/Offline.Access', 'https://graph.microsoft.com/User.Read'])
    url, state = account.con.get_authorization_url(requested_scopes=scopes, redirect_uri= callback)

    # the state must be saved somewhere as it will be needed later
    db.insert({'state':state})
    
    return redirect(url)

@app.route('/steptwo')
def auth_step_two_callback():
    account = Account(credentials, scopes = ['https://graph.microsoft.com/Mail.ReadWrite', 'https://graph.microsoft.com/Mail.Send', 'https://graph.microsoft.com/Offline.Access', 'https://graph.microsoft.com/User.Read'])
    q = Query
    states = db.search(q.state.exists())
    # retreive the state saved in auth_step_one
    my_saved_state = states[0]['state']
    
    # rebuild the redirect_uri used in auth_step_one
    callback = 'http://127.0.0.1:5000/steptwo'
    
    result = account.con.request_token(request.url, 
                                       state=my_saved_state,
                                       redirect_uri=callback)
    # if result is True, then authentication was succesful 
    #  and the auth token is stored in the token backend
    if result:
        return render_template('auth_complete.html')
    
    
def main():
    account = Account(credentials, scopes = ['https://graph.microsoft.com/Mail.ReadWrite', 'https://graph.microsoft.com/Mail.Send', 'https://graph.microsoft.com/Offline.Access', 'https://graph.microsoft.com/User.Read'])
    mailbox = account.mailbox()
    inbox = mailbox.inbox_folder()

    messages = []
    hype = ['POG,','It\'s Hype Robot, here at world email contest and we have a tough challenge between 2 world class emailers, but the one who will clearly win is the one who called me here.']
    for message in inbox.get_messages():
        if not message.is_read():
            messages.append(message)
        
    for message in messages:
        message.mark_as_read()
        m = message.reply()
        body = random.choice(hype) + '\n\nthis is an automated message, hope the person who request the hype is satisfied'
        m.body = body
        m.send()