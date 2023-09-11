import os
from datetime import datetime as dt
from datetime import timedelta

import boto3
import requests

#####################################################################################################################
# THIS IS ONLY TO BE ABLE TO RUN LOCALLY
# IN AWS IT WOULD BE REMOVED
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ["AWS_LAMBDA_WEATHER_URL"] = \
    "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&start_date={}&end_date={}&hourly=temperature_2m,relativehumidity_2m,rain,snowfall,snow_depth,cloudcover,direct_radiation,diffuse_radiation"
#######################################################################################################################

# AWS Lambda for running this code
# DynamoDB (serverless)

start_date = (dt.now() - timedelta(days=2)).strftime("%Y-%m-%d")
end_date = dt.now().strftime("%Y-%m-%d")

url = os.getenv("AWS_LAMBDA_WEATHER_URL").format(start_date, end_date)

# Create a DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("weather-history-table")     # Should be created on AWS before running


def lambda_handler(event, context):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()
    except Exception as e:
        print(f'Some error occured when calling API: {e}')
        raise SystemExit(e)

    for date, temperature, humidity, rain, snowfall, snowdepth, cloudcover, direct_radiation, diffuse_radiation in zip(
         response['hourly']['time'],
         response['hourly']['temperature_2m'],
         response['hourly']['relativehumidity_2m'],
         response['hourly']['rain'],
         response['hourly']['snowfall'],
         response['hourly']['snow_depth'],
         response['hourly']['cloudcover'],
         response['hourly']['direct_radiation'],
         response['hourly']['diffuse_radiation']
    ):
        Item = {
            'date': date,
            'temperature': temperature,
            'humidity': humidity,
            'rain': rain,
            'snowfall': snowfall,
            'snowdepth': snowdepth,
            'clodcover': cloudcover,
            'direct_radiation': direct_radiation,
            'diffuse_radiation': diffuse_radiation
        }

        # Retrieve weather by date if available
        response = table.get_item(Key={"date": date})
        if not response.get('Item'):
            # Insert the new weather data into the table if it doesn't already exist
            table.put_item(Item=Item)