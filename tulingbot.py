#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests


def get_data(text):
    inputText = {'text': text}
    key = "1f58481f27d941e89e1f6d71e959b686"
    userInfo = {'apiKey':key, 'userId': "361928"}
    perception = {'inputText': inputText}
    data = {'perception': perception, 'userInfo': userInfo}
    return data

def get_answer(text):
    data = get_data(text)
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    response = requests.post(url=url, data=json.dumps(data))
    response.encoding = 'utf-8'
    result = response.json()
    answer = result['results'][0]['values']['text']
    return answer

