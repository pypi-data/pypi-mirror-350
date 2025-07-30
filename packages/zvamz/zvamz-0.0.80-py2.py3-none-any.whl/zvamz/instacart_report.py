import pandas as pd
import numpy as np
from datetime import datetime, timezone
import requests
import json
import time
import os

def insta_api_get_refresh_token(client_id, client_secret, code):
    token_url = "https://api.ads.instacart.com/oauth/token"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": 'https://zvdataautomation.com/',
        "code": code,
        "grant_type": 'authorization_code',
    }

    response = requests.post(
        token_url,
        headers=headers,
        json=data,
    )

    try:
      refresh_token = response.json()['refresh_token']
      return refresh_token

    except:
      message = response.text
      raise ValueError(message)

def insta_api_get_access_token(client_id, client_secret, refresh_token):
    token_url = "https://api.ads.instacart.com/oauth/token"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": 'https://zvdataautomation.com/',
        "refresh_token": refresh_token,
        "grant_type": 'refresh_token',
    }

    response = requests.post(
        token_url,
        headers=headers,
        json=data,
    )

    try:
        access_token = response.json()['access_token']
        return access_token
    except:
        message = response.text
        raise ValueError(message)

def insta_api_get_product_report(start_date, end_date, file_path, access_token):
    # Request Report
    url = "https://api.ads.instacart.com/api/v2/reports/products"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    payload = {
        'date_range': {
            'start_date': start_date,
            'end_date': end_date,
        },
        'segment': 'day',
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        report_id = response.json()['data']['id']
        print(f'report_id: {report_id}')
    except:
        message = response.text
        raise ValueError(message)

    #Download Report
    url = f"https://api.ads.instacart.com/api/v2/reports/{report_id}"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    for attempt in range(10):
        response = requests.get(url, headers=headers)

        try:
            status = response.json()['data']['attributes']['status']
            print(f'Report Status: {status}')

            if status == 'completed':
                url = f"https://api.ads.instacart.com/api/v2/reports/{report_id}/download"

                headers = {
                    'Accept': 'application/json',
                    'Authorization': f'Bearer {access_token}',
                }

                response = requests.get(url, headers=headers)
                fileName = os.path.join(file_path, f'instacart_report_{report_id}.csv')

                with open(fileName, 'wb') as f:
                    f.write(response.content)

                print('Report Downloaded')
                return fileName

                break

        except:
            message = response.text
            print(message)
            break

        time.sleep(60)
    else:
        raise ValueError('Report Failed after 10 attempts')

def insta_ads_report(filePath:str):
    instaDf = pd.read_csv(filePath)
    instaDf['date'] = pd.to_datetime(instaDf['date'])

    req_columns = [
        'date',
        'status',
        'campaign',
        'ad_group',
        'product',
        'product_size',
        'upc',
        'spend',
        'attributed_sales',
        'attributed_quantities',
        'roas',
        'impressions',
        'clicks',
        'ctr',
        'average_cpc',
        'ntb_attributed_sales',
        'percent_ntb_attributed_sales',
        'id',
        'campaign_uuid',
        'ad_group_uuid'
    ]

    missingColumns = set(req_columns) - set(instaDf.columns)
    newColumns = set(instaDf.columns) - set(req_columns)

    if missingColumns or newColumns:
        message = (
        f"""
        missing columns: {', '.join(missingColumns)}
        new columns: {', '.join(newColumns)}
        """
        )

        raise ValueError(message)

    instaDf = instaDf[req_columns]

    schema = {
        'date' : 'datetime64[ns]',
        'status' : str,
        'campaign' : str,
        'ad_group' : str,
        'product' : str,
        'product_size' : str,
        'upc' : str,
        'spend' : float,
        'attributed_sales' : float,
        'attributed_quantities' : float,
        'roas' : float,
        'impressions' : float,
        'clicks' : float,
        'ctr' : float,
        'average_cpc' : float,
        'ntb_attributed_sales' : float,
        'percent_ntb_attributed_sales' : float,
        'id' : str,
        'campaign_uuid' : str,
        'ad_group_uuid' : str
    }

    instaDf = instaDf.astype(schema)
    return instaDf

def insta_api_get_marketshare(access_token, start_date, end_date):
    url = 'https://api.ads.instacart.com/api/v2/charts/tables'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    payload = {
        "source": "sds",
        "query": {
            "series": {
                "columns": [
                    "sds.date",
                    "sds.brand_name",
                    "sds.category_name",
                    "sds.super_category_name",
                    "sds.department_name",
                    "sds.share",
                    "sds.brand_sales_usd",
                    "sds.brand_ad_spend_usd"
                ],
                "filters": [
                    {
                        "column": "sds.date",
                        "operation": "GTE",
                        "value": start_date
                    },
                    {
                        "column": "sds.date",
                        "operation": "LTE",
                        "value": end_date
                    },
                ],
                "order_bys": [
                    {
                        "column": "sds.date",
                        "direction": "DESC"
                    }
                ],
              "pagination": {
                  "page": 1,
                  "page_size": 500
              }
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    columns_info = response.json()['data']['attributes']['header']['series']['columns']
    column_names = [col['name'].split('.')[-1] for col in columns_info]

    data_section = response.json()['data']['attributes']['data']['rows']
    shareDf = pd.DataFrame(data_section, columns=column_names)

    req_columns = [
        'date',
        'brand_name',
        'category_name',
        'super_category_name',
        'department_name',
        'share',
        'brand_sales_usd',
        'brand_ad_spend_usd'
    ]

    missingColumns = set(req_columns) - set(shareDf.columns)
    newColumns = set(shareDf.columns) - set(req_columns)

    if missingColumns or newColumns:
        message = (
        f"""
        missing columns: {', '.join(missingColumns)}
        new columns: {', '.join(newColumns)}
        """
        )

        raise ValueError(message)

    shareDf = shareDf[req_columns]

    schema = {
        'date': 'datetime64[ns]',
        'brand_name': str,
        'category_name': str,
        'super_category_name': str,
        'department_name': str,
        'share': float,
        'brand_sales_usd': float,
        'brand_ad_spend_usd': float
        
    }
    
    shareDf = shareDf.astype(schema)
    return shareDf

