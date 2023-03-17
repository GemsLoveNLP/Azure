#!/usr/local/bin/python3
import requests

def notify(msg):
    url = 'https://notify-api.line.me/api/notify'
    token = 'g8qmd2kClnMnQSKVHZovuqgH38dktkYUYBnO5TW33lN'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    r = requests.post(url, headers=headers, data = {'message':msg})
    print (r.text)

