import logging
import boto3
from botocore.exceptions import ClientError
import requests
from flask import Flask, render_template, request, jsonify
import os
client = boto3.client('s3')
s3 = boto3.resource('s3')

f = open('C:/Users/29735/Pictures/Sticker/download.jfif','rb')
key = 'hire2020-hire-archiegu-04010401/' + 'test2.jpg'
client.put_object(Bucket = 'hire2020', Key = key, Body = f)

def create_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket' : 'hire2020',
                'Key' : key
            },
            ExpiresIn = expiration
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response
'''
url = create_presigned_url('hire2020', key)
if url is not None:
    response = requests.get(url)
    print(url)

'''
dynamodb = boto3.resource('dynamodb', region_name='cn-north-1')
table = dynamodb.Table('hire2020-hire-archiegu-04010401')
scan = table.scan()
with table.batch_writer() as batch:
    for each in scan['Items']:
        batch.delete_item(
            Key={
                'ID': each['ID'],
            }
        )


