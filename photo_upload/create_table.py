
from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='cn-north-1')
table = dynamodb.Table('hire2020-hire-archiegu-04010401')
table.put_item(
    Item = {
        'ID':'103.196.22.101 ',
        'PicID':'test.jpg',
        'PicURL':'test.url',
        'Date':'2020-4-2',
        'Time':'5.07.PM',
    }
)
'''
response = table.get_item(
    Key = {
        'ID':'103.196.22.101 '
    }
)
item = response['Item']
print(item)
'''
'''
table = dynamodb.create_table(
    TableName='hire2020-hire-archiegu-04010401',
    KeySchema=[
        {
            'AttributeName': 'UserIP',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'PicURL',
            'KeyType': 'RANGE'  #Sort key
        },
        
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'UserID',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'PicName',
            'AttributeType': 'S'  #Sort key
        },
        {
            'AttributeName': 'PicURL',
            'AttributeType': 'S'  #Sort key
        },
        {
            'AttributeName': 'Date',
            'AttributeType': 'S'  #Partition key
        },
        {
            'AttributeName': 'Time',
            'AttributeType': 'S'  #Partition key
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)
'''

print("Table status:", table.table_status)
