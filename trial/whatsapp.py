from django.http import HttpResponse
from grpc import Status
import requests
import json
bearer_token='Bearer EAAK0qnanlscBAGZByLnFOBXsL7XNDZCwO6A8oL4gzZCdg4cTH0sXFKvseuMKQND3cZCtjXX2PtvvWye8ery1stF3H2mNEEHItu8QDnJ8aqqk2fjN8bDGaJKOD7ZAI92k9fkqEjlc6VpOnncmt8z5ZC4xBuPqXtGiz03ZAff6pbmZAFZAVR6mY31uvObY8YfNTNmZBShDBjHAGZAOW9EnmRKufm7PiTLBusw4r4ZD'
phone_number_id='102222989247043'

def post_media(pdf):
    url = f'https://graph.facebook.com/v13.0/{phone_number_id}/media'
    payload={'messaging_product': 'whatsapp'}
    files={'file':("out.pdf",pdf,"application/pdf")}
    # files={'file':("out.pdf",open('C:/Users/USER/output.pdf','rb'),"application/pdf")}
    headers = {
    'Authorization': bearer_token
    }

    response = requests.post(url=url, headers=headers, data=payload, files=files)
    if response.status_code==200:
        json_data=json.loads(response.text)
        return json_data['id']
    else:
        return 0

def media_msg(id):
    url = f'https://graph.facebook.com/v13.0/{phone_number_id}/messages'

    payload = json.dumps({
    "messaging_product": "whatsapp",
    "to": "919573571256",
    "type": "document",
    "document": {
        "id": id
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': bearer_token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def text_msg(body):
    url = f'https://graph.facebook.com/v13.0/{phone_number_id}/messages'

    payload = json.dumps({
    "messaging_product": "whatsapp",
    "to": "919573571256",
    "type": "text",
    "text": {
        "preview_url": False,
        "body": body
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': bearer_token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def delete_media(id):
    url = f'https://graph.facebook.com/v13.0/{id}/'

    payload={}
    headers = {
    'Authorization': bearer_token
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    return response

def final_call(pdf,body):
    res=post_media(pdf)
    if res!=0:
        r=media_msg(res)
        if r.status_code==200:
            r=text_msg(body)
            if r.status_code==200:
                r=delete_media(res)
                if r.status_code==200:
                    return 1
    return 0