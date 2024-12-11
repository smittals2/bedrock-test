import os
import sys
from api_request_schema import get_model_ids, api_request_list

model_id = os.getenv('MODEL_ID', 'meta.llama3-1-70b-instruct-v1:0')
aws_region = os.getenv('AWS_REGION', 'us-west-2')

if model_id not in get_model_ids():
    print(f'Error: Models ID {model_id} in not a valid model ID. Set MODEL_ID env var to one of {get_model_ids()}.')
    sys.exit(0)

api_request = api_request_list[model_id]

config = {
    'log_level': 'info',  # One of: info, debug, none
    'last_speech': "If you have any other questions, please don't hesitate to ask. Have a great day!",
    'region': aws_region,
    'polly': {
        'Engine': 'neural',
        'LanguageCode': 'en-US',
        'VoiceId': 'Danielle',
        'OutputFormat': 'pcm',
    },
    'translate': {
        'SourceLanguageCode': 'en',
        'TargetLanguageCode': 'en',
    },
    'bedrock': {
        'response_streaming': True,
        'api_request': api_request
    }
}

def printer(text, level):
    if config['log_level'] == 'info' and level == 'info':
        print(text)
    elif config['log_level'] == 'debug' and level in ['info', 'debug']:
        print(text)
