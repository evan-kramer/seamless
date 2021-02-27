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
search_string = ['^Budget Routing', '^Data Sharing Agreement', '^OSSE Direct Voucher', 
                 '^Document Routing', '^OSSE New Hire Onboarding', '^OSSE MOU Routing', 
                 '^OSSE Contract', '^OSSE P\-CARD', '^OSSE Recruitment Request']

# Loop overall forms
for s in search_string:
    for i in list(forms.item_name):
        if re.search(s, i):
            # Capture form_id
            form_id = forms.form_id[forms.item_name == i].to_string(index = False)
            # URI and URL
            uri = '/form/{form_id}/pipeline'.format(form_id = form_id)
            url = 'https://{domain}.seamlessdocs.com/api{uri}'.format(domain = domain,
                                                                      uri = uri)
            # Define headers
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
            # Send request, convert to dataframe, and save
            r = requests.get(url, headers = headers)
            pipeline = pd.DataFrame()
            
            # Create breaks
            for j in range(0, (r.json()['items_count'] // 50 + 1) * 50, 50):
                try:
                    r = requests.get(url, headers = headers, 
                                     params = {'offset': j})
                    pipeline = pipeline.append(pd.json_normalize(r.json()['items']))
                except:
                    pass    
            pipeline.to_csv('C:/Users/evan.kramer/OneDrive - Government of The District of Columbia/Seamless Data/{i}.csv'.format(i = i), 
                            index = False)           
            
# Check whether limiting worked
file_list = os.listdir('C:/Users/evan.kramer/OneDrive - Government of The District of Columbia/Seamless Data')
for f in file_list:
    if '.csv' in f:
        try:
            temp = pd.read_csv('C:/Users/evan.kramer/OneDrive - Government of The District of Columbia/Seamless Data/{f}'.format(f = f))
            print(f)
            print(len(temp))
        except:
            pass
    else:
        pass