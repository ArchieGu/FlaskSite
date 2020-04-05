# -*- coding: utf-8 -*-
"""
    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import urllib
import re
import os
import boto3
import datetime
from flask import Flask, render_template, request, jsonify
from flask_dropzone import Dropzone
import logging
from botocore.exceptions import ClientError

#s3 setting
client = boto3.client('s3')
s3 = boto3.resource('s3')

basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'static'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=20,
    DROPZONE_UPLOAD_ON_CLICK=True
)

dropzone = Dropzone(app)

dynamodb = boto3.resource('dynamodb', region_name='cn-north-1')
table = dynamodb.Table('hire2020-hire-archiegu-04010401')

def update_table(PicID,PicName,UserIP,Date,Time):
    table.put_item(
        Item = {
            'ID': PicID,
            'PicName':PicName,
            'UserIP':UserIP,
            'Date':Date,
            'Time':Time
        }
    )


def create_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket' : 'hire2020',
                'Key' : object_name
            },
            ExpiresIn = expiration
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response
def get_out_ip():
    ip = request.remote_addr
    #ip = request.headers['X-Real-IP']
    return ip


def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    return False
    

@app.route('/', methods=['POST', 'GET'])

def upload():
    if request.method == 'POST':
        for key, f in request.files.items():
            
            if key.startswith('file') and allowed_file(f.filename):
                UserIP = get_out_ip()
                PicName = str(f.filename)
                PicID = str(hash(f.filename))
                Date = str(datetime.date.today())
                Time = str(datetime.datetime.now()).split(' ')[1]
                #s3 part
                s3_key = 'hire2020-hire-archiegu-04010401/' + str(PicID)
                client.put_object(Bucket = 'hire2020', Key = s3_key, Body = f)
                #PicURL = create_presigned_url('hire2020', s3_key)
                update_table(PicID,PicName,UserIP,Date,Time)
                '''
                reponse = table.get_item(
                    Key = {
                        'ID':PicID,
                    }
                )
                item = reponse['Item']
                print(item)
                '''
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('upload.html')

@app.route('/show', methods=['POST', 'GET'])
    
def show_photo():
    scan = table.scan()
    info = []
    imgURL = []
    with table.batch_writer() as batch:
        for each in scan['Items']:
            info.append(each)
            s3_key = 'hire2020-hire-archiegu-04010401/' + each['ID']
            PicURL = create_presigned_url('hire2020', s3_key)
            imgURL.append(PicURL)
    return render_template('image.html', images = imgURL)
            
if __name__ == '__main__':
    app.run(debug=True)
