import json
import os

import requests
import datetime

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

def get_tmpKey(fileName):
    url = 'https://sit.builtopia.cn/v1/asset/upload/tmp_key'
    payload_data = {
        'fileName': fileName
    }
    payload_header = {
        'Host': 'sit.builtopia.cn',
        'Content-Type': 'application/json',
        'cookie': 'ajs_anonymous_id=2edb1281-ea92-40b8-b20d-9a5ada7b627d; themeMode=light; themeDirection=ltr; themeColorPresets=default; themeLayout=horizontal; themeStretch=false; goc-jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTQ4MjcwMTYsImlhdCI6MTY1NDc0MDYxNiwiaXNzIjoiZ29jeWJlciIsInN1YiI6ImdvY3liZXIiLCJhY2NvdW50SWQiOiJMODU1eEQiLCJ0eXBlIjoib3JnX21lbWJlciIsInVzZXJJZCI6ImRxUXBqRCIsIm9yZ0lkIjoiNnEzbG0wIiwibmFtZSI6IumCk-W4g-WIqeWkmiDpnI3moLzkvI3lhbnotJ_otKPkuroiLCJ2ZXJzaW9uIjowfQ.kaNgZW3MzqW7x5S1DrHH80cBymnUnBAtTtn1JwC8NvY'
    }
    timeout = 30
    json_data = json.dumps(payload_data)
    result = requests.post(url=url, data=json_data, headers=payload_header, timeout=timeout, allow_redirects=True)
    return result.text

def uploadtoCos(bucket,key,filePath,secretId,secretKey,token):
    region = 'ap-shanghai'
    scheme = 'https'
    config = CosConfig(Region=region, SecretId=secretId, SecretKey=secretKey, Token=token, Scheme=scheme)
    client = CosS3Client(config)
    response = client.upload_file(
        Bucket=bucket,
        Key=key,
        LocalFilePath=filePath
    )
    return response

def assetUpload(contentPath,name):
    url = 'https://sit.builtopia.cn/v1/asset'
    payload_data = {
        'contentPath': contentPath,
        'library': "enterprise",
        'name': name,
        'tmpToken': "H34zes2XKn23ZFlItClRLrVgLwmh5ooa07f2945f4a0d21be54b360960610a087Mgo0cyeyVLNL8ui1_nzGrK3BG_BXThebx5lE3OoGPW9lLXyR-rF390WMn5z-E0LNMPwPPF21-pZMNqWHeJisSxYzT5mxIH6so4INLBmvOfq2tNWepfBaK3X9WJCcIct9cIow-AtHavUm9DiFYg5g3eZiI4qKxpofLjtUwYfppeaHtdblCKcLgF2KHkeJb431xLPfB390fZJWc5j-vJh3YE4xqJYVxl3nY3h_TC6-rvm0mU05YlfB32HAnMzMtJMMTHwpKVnkd2y7_FWEpBigj5oRcA0yVKTcSL8msF4MWoef9EkPpARil2V95oj2GjCbSyQwapTD5R3spMwteIkg2P3pks5be8iZqyejczu_b37M5vv0Fgx2NOZr5XUP28U5HAF7bVsUsRduRO4KikiCyGsEguFgv1e0tnwFl4Md4oBDkMZZab81uHg0YhT0l7CSQSBZQKfq5GcAJE5B4V34fagtNU72buGagGvsC9GESWdecxPWJkSfB5R84y4fCvOqVAghhW0MqljvTTpAf3Al-6XX7fwm_O_tFE9BiObXPIp4zRsTWqGy0_kyo0tDB32PWu4UrTOSh63NdgnF5nCC1yY-fQfzuVQtvevwIVuiixIIksoLcvdKcE2w6KnPf6zS7fcnpd_n2BbCD_ktJ47f6w"
    }
    payload_header = {
        'Host': 'sit.builtopia.cn',
        'Content-Type': 'application/json',
        'cookie': 'ajs_anonymous_id=2edb1281-ea92-40b8-b20d-9a5ada7b627d; themeMode=light; themeDirection=ltr; themeColorPresets=default; themeLayout=horizontal; themeStretch=false; goc-jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTQ4MjcwMTYsImlhdCI6MTY1NDc0MDYxNiwiaXNzIjoiZ29jeWJlciIsInN1YiI6ImdvY3liZXIiLCJhY2NvdW50SWQiOiJMODU1eEQiLCJ0eXBlIjoib3JnX21lbWJlciIsInVzZXJJZCI6ImRxUXBqRCIsIm9yZ0lkIjoiNnEzbG0wIiwibmFtZSI6IumCk-W4g-WIqeWkmiDpnI3moLzkvI3lhbnotJ_otKPkuroiLCJ2ZXJzaW9uIjowfQ.kaNgZW3MzqW7x5S1DrHH80cBymnUnBAtTtn1JwC8NvY'
    }
    timeout = 30
    json_data = json.dumps(payload_data)
    result = requests.post(url=url, data=json_data, headers=payload_header, timeout=timeout, allow_redirects=True)
    return result


if __name__ == '__main__':
    glbs = os.listdir("data")
    for glb in glbs:
        fileName = glb
        filePath = "data/"+glb
        params = json.loads(str(get_tmpKey(fileName=fileName)))
        secretId = params["data"]["tmpSecretId"]
        secretKey = params["data"]["tmpSecretKey"]
        contentPath = params["data"]["contentPath"]
        token = params["data"]["tmpToken"]

        uploadtoCos(bucket="sit-asset-static-1308250937",key=contentPath,filePath=filePath,secretId=secretId,secretKey=secretKey,token=token)

        assetUpload(contentPath=contentPath,name=fileName.replace(".glb",""))

        print datetime.datetime.now()



