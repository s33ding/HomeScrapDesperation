import boto3
import config

# Initialize a session using Amazon SNS
sns_client = boto3.client('sns', region_name='us-east-1')  # Replace with your desired AWS region

def create_sns_topic(topic_name):
    try:
        # Create SNS topic
        response = sns_client.create_topic(Name=topic_name)
        
        # Extract the topic ARN from the response
        topic_arn = response['TopicArn']
        
        print(f"Successfully created SNS topic: {topic_name}")
        print(f"Topic ARN: {topic_arn}")
        
        return topic_arn
    except Exception as e:
        print(f"Error creating SNS topic: {str(e)}")

# Usage
if __name__ == "__main__":
    topic_name = config.topic_name
    create_sns_topic(topic_name)

