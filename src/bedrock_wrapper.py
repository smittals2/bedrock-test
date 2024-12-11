import json
import time
import boto3
import logging
from config import config
from text_to_speech import Reader
from user_input_manager import UserInputManager
from config import printer

bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name=config['region'])
logger = logging.getLogger(__name__)

class BedrockModelsWrapper:
    @staticmethod
    def define_body(text):
        model_id = config['bedrock']['api_request']['modelId']
        model_provider = model_id.split('.')[0]
        body = config['bedrock']['api_request']['body']

        if model_provider == 'amazon':
            body['inputText'] = text
        elif model_provider == 'meta':
            body['prompt'] = text
            printer(f"prompt: {text}", 'debug')
        elif model_provider == 'anthropic':
            body['prompt'] = f'\n\nHuman: {text}\n\nAssistant:'
        elif model_provider == 'cohere':
            body['prompt'] = text
        else:
            raise Exception('Unknown model provider.')

        return body

    @staticmethod
    def get_stream_chunk(event):
        return event.get('chunk')

    @staticmethod
    def get_stream_text(chunk):
        model_id = config['bedrock']['api_request']['modelId']
        model_provider = model_id.split('.')[0]

        chunk_obj = json.loads(chunk.get('bytes').decode())
        if model_provider == 'amazon':
            text = chunk_obj['outputText']
        elif model_provider == 'meta':
            text = chunk_obj['generation']
        elif model_provider == 'anthropic':
            text = chunk_obj['completion']
        elif model_provider == 'cohere':
            text = ' '.join([c["text"] for c in chunk_obj['generations']])
        else:
            raise NotImplementedError('Unknown model provider.')

        printer(f'[DEBUG] {chunk_obj}', 'debug')
        return text

class BedrockWrapper:
    def __init__(self):
        self.speaking = False

    def is_speaking(self):
        return self.speaking

    def invoke_bedrock(self, text):
        self.speaking = True

        body = BedrockModelsWrapper.define_body(text)
        logger.info(f"Bedrock generation started with body {str(body)}")

        try:
            body_json = json.dumps(body)
            response = bedrock_runtime.invoke_model_with_response_stream(
                body=body_json,
                modelId=config['bedrock']['api_request']['modelId'],
                accept=config['bedrock']['api_request']['accept'],
                contentType=config['bedrock']['api_request']['contentType']
            )

            bedrock_stream = response.get('body')

            audio_gen = self.to_audio_generator(bedrock_stream)
            logger.info(f"Creating bedrock to audio generator (AWS Polly) stream")

            reader = Reader()
            for audio in audio_gen:
                reader.read(audio)

            reader.close()
            logger.info("Finished streaming text to Polly")

        except Exception as e:
            logger.error(f"Execption: {e}")
            print(e)
            time.sleep(2)
            self.speaking = False

        time.sleep(1)
        self.speaking = False
        logger.info("Bedrock generation complete")

    def to_audio_generator(self, bedrock_stream):
        logger.info(f"Preparing and cleaning text to sent to Polly")
        prefix = ''

        if bedrock_stream:
            # Iterate over bedrock_stream, an EventStream object
            for event in bedrock_stream:
                # obtain response chunk of data and get the bytes for it
                chunk = BedrockModelsWrapper.get_stream_chunk(event)
                if chunk:
                    text = BedrockModelsWrapper.get_stream_text(chunk)
                    # ensure complete sentence is being sent, otherwise append to prefix 
                    # TO-DO: only splitting on full stop, should be splitting on other punctuation?
                    if '.' in text:
                        a = text.split('.')[:-1]
                        to_polly = ''.join([prefix, '.'.join(a), '. '])
                        prefix = text.split('.')[-1]
                        print(to_polly, flush=True, end='')
                        yield to_polly
                    else:
                        prefix = ''.join([prefix, text])

            if prefix != '':
                print(prefix, flush=True, end='')
                yield f'{prefix}.'

            print('\n')