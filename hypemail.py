from O365 import Account
from O365.message import Message
from O365.mailbox import MailBox
from O365.mailbox import Message
import random
from flask import Flask

app = Flask(__name__)

CLIENT_ID = '5c03807f-4363-4c78-ac85-2f903305d917'
CLIENT_SECRET = 'Eri07B8vVW:HQQ/_eNX4tNeEKl-wPVy['
credentials = (CLIENT_ID, CLIENT_SECRET)

scopes = ['basic', 'message_all']

#account = Account(credentials)
#if account.authenticate(scopes = ['basic', 'message_all']):
 #   print('Authenticated!')


@app.route('/')
def hello_world():
    return 'Hello, World!'


@route('/stepone')
def auth_step_one():

    callback = 'http://localhost:5000/steptwo'
    account = Account(credentials)
    url, state = account.con.get_authorization_url(requested_scopes=scopes redirect_uri= callback)

    # the state must be saved somewhere as it will be needed later
    my_db.store_state(state) # example...   

    return Flask.redirect(url)

@route('/steptwo')
def auth_step_two_callback():
    account = Account(credentials)
    
    # retreive the state saved in auth_step_one
    my_saved_state = my_db.get_state()  # example...
    
    # rebuild the redirect_uri used in auth_step_one
    callback = 'my absolute url to auth_step_two_callback'
    
    result = account.con.request_token(request.url, 
                                       state=my_saved_state,
                                       redirect_uri=callback)
    # if result is True, then authentication was succesful 
    #  and the auth token is stored in the token backend
    if result:
        return Flask.render_template('auth_complete.html')
    
    
def main():
    account = Account(credentials)
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