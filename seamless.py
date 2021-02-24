# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 22:12:45 2021
@author: evan.kramer
Pull Data from Seamless
"""
# Import modules
import os, requests, hashlib, hmac, time, re
import pandas as pd

timestamp = time.time()
def get_signature(domain, url, method, uri):
    message = '{0}+{1}+{2}'.format(method, uri, round(timestamp))
    secret = os.getenv('seamless_api_secret')
    signature = hmac.new(bytes(secret, 'utf-8'), 
                         bytes(message, 'utf-8'),
                         digestmod = hashlib.sha256).hexdigest()
    return signature

# Get all forms
form_dict = {}
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
try:
    forms = pd.json_normalize(r.json()['items'])
except:
    pass


# Form pipeline
uri = '/form/{form_id}/pipeline'.format(form_id = forms.form_id[24])
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
try:
    pipeline = pd.json_normalize(r.json()['items'])
except:
    pass


search_string = ['^Budget Routing', '^Data Sharing Agreement', '^OSSE Direct Voucher', 
                 '^Document Routing', '^OSSE New Hire Onboarding', '^OSSE MOU Routing', 
                 '^OSSE Contract', '^OSSE P\-CARD', '^OSSE Recruitment Request']
for s in search_string:
    for i in list(forms.item_name):
        if re.search(s, i):
            form_dict[i] = forms.form_id[forms.item_name == i].to_string(index = False)
print(form_dict)


# Budget package requests
# Data sharing agreement requests
forms.form_id[forms.item_name == 'Data Sharing Agreement Routing Form']
# Direct voucher requests
# General document routing requests
# HR onboarding requests
# MOU routing requests
# OCP contract cert requests
# Pcard requests
# Priority hire requests