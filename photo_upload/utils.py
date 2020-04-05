import requests
import boto3
import re, os, datetime



def get_out_ip():
    sohu_ip_url = 'http://txt.go.sohu.com/ip/soip'
    r = urllib.request.urlopen(sohu_ip_url)
    text = r.read().decode()
    result = re.findall(r'\d+.\d+.\d+.\d+', text)
    if result:
        return result[0]
    else:
        return None