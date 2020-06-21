# Hypemail

An email bot that will hype you up during conversations. Built using [O365 Python](https://github.com/O365/python-o365) package and [Flask](https://flask.palletsprojects.com/en/1.1.x/). Visiting the test server will make an api call to check unread messages of hyperobot@hotmail.com and send a randomized hype message. After the message is sent the page will refresh and start the process all over again depending on the preset refresh time.

## Quick Start

If you want to run the application connect to hyperobot@hotmail.com just run 
> set FLASK_APP=hypemail.py\
> python -m flask run -h localhost -p 5000 --cert=adhoc

## Use your account

Use [this](https://github.com/O365/python-o365#authentication) guide to create an Azure account and application for runnning this app. Then just replace the client id and secret and run 
> set FLASK_APP=hypemail.py\
> python -m flask run -h localhost -p 5000 --cert=adhoc

## Todo
Use giphy api to send gifs instead of text
