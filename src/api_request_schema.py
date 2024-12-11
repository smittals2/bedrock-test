api_request_list = {
    'meta.llama3-1-70b-instruct-v1:0': {
        "modelId": "meta.llama3-1-70b-instruct-v1:0",
        "contentType": "application/json",
        "accept": "*/*",
        "body": {"prompt":"You are my friend and You'll watch me play league of legends and teach me how to play it better. You are a good player, you don't like long conversations, you can chat like human.",
            "max_gen_len":250,
            "temperature":0.1,
            "top_p":0.9,
            }           
    },
    'meta.llama3-8b-instruct-v1:0': {
        "modelId": "meta.llama3-8b-instruct-v1:0",
        "contentType": "application/json",
        "accept": "*/*",
        "body": {"prompt":"",
            "max_gen_len":250,
            "temperature":0.5,
            "top_p":0.9,
            }           
    },
    'amazon.titan-text-express-v1': {
        "modelId": "amazon.titan-text-express-v1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "inputText": "",
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        }
    },
    'amazon.titan-text-lite-v1': {
        "modelId": "amazon.titan-text-lite-v1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "inputText": "",
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        }
    },
    'anthropic.claude-v2:1': {
        "modelId": "anthropic.claude-v2:1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "prompt": "",
            "max_tokens_to_sample": 300,
            "temperature": 0.5,
            "top_k": 250,
            "top_p": 1,
            "stop_sequences": [
                "\n\nHuman:"
            ],
            "anthropic_version": "bedrock-2023-05-31"
        }
    },
    'anthropic.claude-v2': {
        "modelId": "anthropic.claude-v2",
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "prompt": "",
            "max_tokens_to_sample": 300,
            "temperature": 0.5,
            "top_k": 250,
            "top_p": 1,
            "stop_sequences": [
                "\n\nHuman:"
            ],
            "anthropic_version": "bedrock-2023-05-31"
        }
    },
    'meta.llama2-13b-chat-v1': {
        "modelId": "meta.llama2-13b-chat-v1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "prompt": "",
            "max_gen_len": 512,
            "temperature": 0.2,
            "top_p": 0.9
        }
    },
    'meta.llama2-70b-chat-v1': {
        "modelId": "meta.llama2-70b-chat-v1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "prompt": "",
            "max_gen_len": 512,
            "temperature": 0.2,
            "top_p": 0.9
        }
    },
    'cohere.command-text-v14': {
        "modelId": "cohere.command-text-v14",
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "prompt": "",
            "max_tokens": 1024,
            "temperature": 0.8,
        }
    },
    'cohere.command-light-text-v14': {
        "modelId": "cohere.command-light-text-v14",
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "prompt": "",
            "max_tokens": 1024,
            "temperature": 0.8,
        }
    },
}


def get_model_ids():
    return list(api_request_list.keys())
