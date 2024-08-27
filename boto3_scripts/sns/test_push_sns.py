import boto3
import config


# Initialize a session using Amazon SNS
sns_client = boto3.client('sns', region_name='us-east-1')  # Replace with your desired AWS region

def publish_message_to_sns(topic_arn, message):
    try:
        # Publish a message to the SNS topic
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message
        )
        
        # Extract message ID from the response
        message_id = response['MessageId']
        
        print(f"Message sent successfully! Message ID: {message_id}")
        return message_id
    except Exception as e:
        print(f"Error publishing message to SNS topic: {str(e)}")

# Usage
if __name__ == "__main__":
    topic_arn = config.topic_arn
    message = "this is a test"
    publish_message_to_sns(topic_arn, message)
