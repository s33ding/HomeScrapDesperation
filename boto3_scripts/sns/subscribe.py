import boto3
import config

# Initialize a session using Amazon SNS
sns_client = boto3.client('sns', region_name='us-east-1')  # Replace with your desired AWS region

def subscribe_to_sns_topic(topic_arn, my_email):
    try:
        # Subscribe the phone number to the topic using the 'sms' protocol
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=my_email
        )
        
        # Extract subscription ARN from the response
        subscription_arn = response['SubscriptionArn']
        
        print(f"Successfully subscribed {my_email} to topic: {topic_arn}")
        print(f"Subscription ARN: {subscription_arn}")
        
        return subscription_arn
    except Exception as e:
        print(f"Error subscribing to SNS topic: {str(e)}")

# Usage
if __name__ == "__main__":
    topic_arn = config.topic_arn
    my_email = config.my_email
    subscribe_to_sns_topic(topic_arn, my_email)
