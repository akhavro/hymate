# PROJECT: Weather API call

This project is to be deployed in AWS serverless.
My suggestion would be to **run the code** itself using Lambda AWS and the reasoning is the following:

- Serverless
- The script runs quickly once per day
- It can integrate with other AWS serverless tools


**Schedule execution** using Amazon EventBridge

- Serverless
- Used for setting events that trigger actions (such as executing a Lambda function)


**Database: DynamoDB**

- Serverless
- NoSQL for scalability and if we want to add another field someday we don't have to worry with schema


**Code Logic:**
Since we run the function once a day to fetch 3 days of data, there is going to be **duplicated data**.
To avoid storing the duplicated weather data, the data is looped over, verifying if there is already a record
for that datestamp. If there is, then the value is not updated, else, a new entry is made.

Also, the data is reorganized so that for each timestamp we only have the specific values of the weather parameters that were requested.
That is, the objects that are written are as:

```
{
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
```