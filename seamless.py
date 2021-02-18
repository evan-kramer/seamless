# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 22:12:45 2021
@author: evan.kramer
Pull Data from Seamless
"""
# Import modules
import os, requests, hashlib, hmac, base64, time
# from urllib.request import urlopen, Request
import pandas as pd

timestamp = time.time()
def get_signature(domain, url, method, uri):
    message = '{0}+{1}+{2}'.format(method, uri, round(timestamp))
    secret = os.getenv('seamless_api_secret')
    signature = hmac.new(bytes(secret, 'utf-8'), 
                         bytes(message, 'utf-8'),
                         digestmod = hashlib.sha256).hexdigest()
    return signature

# Example
base64.b64encode(hmac.new(bytes('uq7UKtK4NEBVqNPbHBTImuxxShp8ug', 'utf-8'),
                          bytes('POST+/form/CO15021000011408891/elements+1425589564+abc123', 'utf-8'),
                          digestmod = hashlib.sha256).digest())
hmac.new(bytes('uq7UKtK4NEBVqNPbHBTImuxxShp8ug', 'utf-8'),
         bytes('POST+/form/CO15021000011408891/elements+1425589564+abc123', 'utf-8'),
         digestmod = hashlib.sha256).hexdigest()

'0cdba187c5a2ce12f732ccbdb12a0c4d82cf8930f1d6aedef58cb38dcf9c6919'







# Get all forms
domain = 'dcgov'
uri = '/account/forms'
url = 'https://{domain}.seamlessdocs.com/api{uri}'.format(domain = domain, 
                                                          uri = uri)
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'api_key={} signature={}'.format(os.getenv('seamless_api_key'),
                                                      get_signature(domain, 
                                                                    url,
                                                                    "GET",
                                                                    uri)),
    'AuthDate': str(round(timestamp)),
    'Cache-Control': 'no-cache'
}
r = requests.get(url, headers = headers)
# print(r.content)

try:
    forms = pd.json_normalize(r.json()['items'])
except:
    pass

# Get form elements
# print(get_signature(domain, url, 'GET', uri))
# https://www.freeformatter.com/hmac-generator.html#ad-output


'''
curl -X GET -H "Content-Type: application/json" 
-H "Authorization: api_key=pXW4hc3JH7w3lc1Z" 
-H "AuthDate: 1611928508" -H "Cache-Control: no-cache" 
-d '' https://sandbox.seamlessdocs.com/api/account/forms
'''

# Budget package requests
# Data sharing agreement requests
# Direct voucher requests
# General document routing requests
# HR onboarding requests
# MOU routing requests
# OCP contract cert requests
# Pcard requests
# Priority hire requests