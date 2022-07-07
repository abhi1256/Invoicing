import requests
import base64, json

headers = {
    'X-Api-Key': 'c7hf4l2dc007534ff8qgEHjqQUiSsj',
    'X-Api-Secret': 'FSjYwMfBDJlUXBUAttOtGBmfjvUOuBrwMEiuhYNd.WDWYxiTw2Zj6dh42TxSfPD',
    'Content-Type': 'application/json'
}



with open("C:\\Users\\dell\\Desktop\\invoice_models\\invoice\\trial\\Hello man.pdf", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

encoded_string = json.stringify(encoded_string)

json_data = {
    'to': [
        'john@example.com',
    ],
    'from': 'Sender <sender@example.com>',
    'subject': 'Hello, World!',
    'content': [
        {
            'type': 'text/plain',
            'value': 'Hey! .....',
        },
        {
            'type': 'text/html',
            'value': 'Hey! .....',
        },
    ],
    'attachments': [
        {
            'type': 'application/pdf',
            'file_name': 'example.pdf',
            'content': encoded_string,
        },
    ],
}
json_data1 = json.dumps(json_data)
response = requests.post('https://api.mailazy.com/v1/mail/send', headers=headers, json=json_data1)

# Note: the data is posted as JSON, which might not be serialized by
# Requests exactly as it appears in the original command. So
# the original data is also given.
#data = '{\n        "to" : ["john@example.com"],\n        "from": "Sender <sender@example.com>",\n        "subject": "Hello, World!",\n        "content": [{\n            "type": "text/plain",\n            "value": "Hey! ....."\n        },{\n            "type": "text/html",\n            "value": "Hey! ....."\n        }],\n        "attachments": [{\n            "type": "application/pdf",\n            "file_name": "example.pdf",\n            "content": "<base64-encoded-file>"\n        }]\n    }'
#response = requests.post('https://api.mailazy.com/v1/mail/send', headers=headers, data=data)