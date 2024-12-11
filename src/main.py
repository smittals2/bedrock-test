import asyncio
import sys
import os
import logging
from logger import setup_logger
from concurrent.futures import ThreadPoolExecutor

from api_request_schema import api_request_list, get_model_ids
from audio_input import MicStream
from transcription import EventHandler
from bedrock_wrapper import BedrockWrapper
from user_input_manager import UserInputManager
from config import config

setup_logger()
logger = logging.getLogger(__name__)

def main():
    info_text = f'''
    *************************************************************
    [INFO] Supported FM models: {get_model_ids()}.
    [INFO] Change FM model by setting <MODEL_ID> environment variable. Example: export MODEL_ID=meta.llama2-70b-chat-v1

    [INFO] AWS Region: {config['region']}
    [INFO] Amazon Bedrock model: {config['bedrock']['api_request']['modelId']}
    [INFO] Polly config: engine {config['polly']['Engine']}, voice {config['polly']['VoiceId']}
    [INFO] Log level: {config['log_level']}

    [INFO] Hit ENTER to interrupt Amazon Bedrock. After you can continue speaking!
    [INFO] Go ahead with the voice chat with Amazon Bedrock!
    *************************************************************
    '''
    print(info_text)
    
    logger.info("Starting event loop")
    loop = asyncio.get_event_loop()
    loop.run_in_executor(ThreadPoolExecutor(max_workers=1), UserInputManager.start_user_input_loop)

    i = 0
    try:
        logger.info("Starting MicStream Transcribe attempt %d", i)
        i += 1
        loop.run_until_complete(MicStream().basic_transcribe())
    except (KeyboardInterrupt, Exception) as e:
        logger.info("Keyboard interrupt received attempt")
        print(e)

if __name__ == "__main__":
    main()