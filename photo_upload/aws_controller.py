import boto3
dynamo_client = boto3.client('dynamodb')
def get_items():
    return dynamo_client.scan(
        TableName='hire2020-hire-archiegu-04010401'
    )