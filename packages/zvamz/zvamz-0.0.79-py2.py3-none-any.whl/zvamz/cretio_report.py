import os
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import pytz
import requests
import json
import time
import http.client

def cretio_get_access_token(grant_type, client_id, client_secret):
    url = "https://api.criteo.com/oauth2/token"

    payload = {
        "grant_type": grant_type,
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    try:
        access_token = response.json()['access_token']
        print(f'Access Token: {access_token}')
        return access_token
    except:
        print(response.json())

def criteo_campaign_report(access_token, version, report_type, ids, start_date, end_date, file_path_name):
    #create report
    url = f"https://api.criteo.com/{version}/retail-media/reports/campaigns"

    payload = json.dumps({
      "data": {
        "attributes": {
          "endDate": end_date,
          "startDate": start_date,
          "timezone": "EST",
          "salesChannel": "all",
          "campaignType": "all",
          "clickAttributionWindow": "none",
          "viewAttributionWindow": "none",
          "format": "csv",
          # "id": "619284442499084288",
          "ids": ids,
          "reportType": report_type,
          # "dimensions": [],
          # "metrics": [],
          # "searchTermTargetings": [,
          # "searchTermTypes": [],
        },
        # "type": "<string>"
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        report_id = response.json()['data']['id']
        print(report_id)
    except:
        print(response.json())

    # check status
    url = f"https://api.criteo.com/{version}/retail-media/reports/{report_id}/status"

    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Bearer {access_token}'
    }

    status = None
    tries = 0
    while status != 'success' and tries < 10:
        response = requests.request("GET", url, headers=headers, data=payload)
        status = response.json()['data']['attributes']['status']
        print(status)
        if status == 'success':
            break
        else:
            tries += 1
            time.sleep(20)

    # download file
    url = f"https://api.criteo.com/{version}/retail-media/reports/{report_id}/output"

    payload={}
    headers = {
      'Accept': 'application/octet-stream',
      'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        with open(file_path_name, 'wb') as f:
            f.write(response.content)
        print("Report saved!")
    except:
        print(response.json())

