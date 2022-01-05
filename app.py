# app.py

import os
import boto3
import uuid
from flask_cors import CORS

from flask import Flask, jsonify, request
app = Flask(__name__)
CORS(app)
FOOD_TABLE = os.environ['FOOD_TABLE']
client = boto3.client('dynamodb')


@app.route("/")
def hello():
    return "Hello World!"


#@app.route("/food-survey/<string:user_id>")
#def get_user(user_id):
#    resp = client.get_item(
#        TableName=FOOD_TABLE,
#        Key={
#            'userId': { 'N': user_id }
#        }
#    )
#    item = resp.get('Item')
#    if not item:
#        return jsonify({'error': 'User does not exist'}), 404

#    return jsonify({
#        'userId': item.get('userId').get('S'),
#        'name': item.get('name').get('S')
#    })


@app.route("/food-survey", methods=["POST"])
def create_user():

    user_id = str(uuid.uuid4())
    name = request.json.get('name')
    type_of_food = request.json.get('typeOfFood')
    recommend = request.json.get('recommend')
    rating = request.json.get('rating')

    if not name or not type_of_food or not recommend or not rating:
        return jsonify({'error': 'Please provide name, food type, recommendation, and rating'}), 400

    resp = client.put_item(
        TableName=FOOD_TABLE,
        Item={
            'userId': {'S': user_id},
            'name': {'S': name },
            'typeOfFood': {'S': type_of_food },
            'recommend': {'S': recommend},
            'rating': {'N': rating}
        }
    )

    return jsonify({
        'userId': {"S": user_id},
        'name': {'S': name },
        'typeOfFood': {'S': type_of_food },
        'recommend': {'S': recommend},
        'rating': {'N': rating}
    })

@app.route("/test2", methods=["GET"])

def scan_food():
    table_name = "food-table-dev-2"
    region_name = "us-west-2"
    resource = boto3.resource('dynamodb', region_name=region_name)
    
    #I dunno which one of these to use
    target_table = resource.Table(table_name)

    resp = target_table.scan(ProjectionExpression="recommend, typeOfFood, rating")
    return resp