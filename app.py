from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# Initialize DynamoDB client
region_name = 'us-east-1'  # Replace with your AWS region
dynamodb = boto3.resource('dynamodb', region_name=region_name)

table_name = os.environ.get('DYNAMODB_TABLE', 'ReflectionsTable')
table = dynamodb.Table(table_name)

@app.route('/')
def home():
    return jsonify(message="Hello from Flask in Lambda!")

@app.route('/example')
def example():
    return jsonify(message="This is an example route.")

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    item = {
        'id': data['id'],
        'content': data['content']
    }
    table.put_item(Item=item)
    return jsonify(item), 201

@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    response = table.get_item(Key={'id': item_id})
    item = response.get('Item')
    if item:
        return jsonify(item)
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    table.delete_item(Key={'id': item_id})
    return jsonify({'message': 'Item deleted'})


# import os
# import pymysql

# def lambda_handler(event, context):
#     db_host = os.environ['DATABASE_HOST']
#     db_user = os.environ['DATABASE_USER']
#     db_password = os.environ['DATABASE_PASSWORD']
#     db_name = os.environ['DATABASE_NAME']

#     connection = pymysql.connect(
#         host=db_host,
#         user=db_user,
#         password=db_password,
#         database=db_name
#     )

#     # Example query and response
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT 'Hello from the database!'")
#         result = cursor.fetchone()

#     connection.close()

#     return {
#         'statusCode': 200,
#         'body': result[0]
#     }
