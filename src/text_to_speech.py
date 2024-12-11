import time
import boto3
import pyaudio
import logging
from config import config
from user_input_manager import UserInputManager

p = pyaudio.PyAudio()
polly = boto3.client('polly', region_name=config['region'])
logger = logging.getLogger(__name__)

class Reader:
    def __init__(self):
        self.polly = boto3.client('polly', region_name=config['region'])
        self.audio = p.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)
        self.chunk = 1024

    def read(self, data):
        response = self.polly.synthesize_speech(
            Text=data,
            Engine=config['polly']['Engine'],
            LanguageCode=config['polly']['LanguageCode'],
            VoiceId=config['polly']['VoiceId'],
            OutputFormat=config['polly']['OutputFormat'],
        )
        logger.info(f"Generating audio from AWS Polly, data: {data}")
        stream = response['AudioStream']
        
        logger.info("Writing audio to speaker stream")
        while True:
            if UserInputManager.is_executor_set() and UserInputManager.is_shutdown_scheduled():
                UserInputManager.start_shutdown_executor()

            data = stream.read(self.chunk)
            self.audio.write(data)
            if not data:
                break

    def close(self):
        time.sleep(1)
        self.audio.stop_stream()
        self.audio.close()

def aws_polly_tts(polly_text):
    byte_stream_list = []
    polly_text_len = len(polly_text.split('.'))
    for i in range(0, polly_text_len, 20):
        polly_text_chunk = '. '.join(polly_text.split('. ')[i:i + 20])

        response = polly.synthesize_speech(
            Text=polly_text_chunk,
            Engine=config['polly']['Engine'],
            LanguageCode=config['polly']['LanguageCode'],
            VoiceId=config['polly']['VoiceId'],
            OutputFormat=config['polly']['OutputFormat'],
        )
        byte_stream = response['AudioStream']
        byte_stream_list.append(byte_stream)

    byte_chunks = []
    chunk = 1024
    for bs in byte_stream_list:
        while True:
            data = bs.read(chunk)
            byte_chunks.append(data)

            if not data:
                bs.close()
                break

    read_byte_chunks(b''.join(byte_chunks))

def read_byte_chunks(data):
    polly_stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)
    polly_stream.write(data)

    time.sleep(1)
    polly_stream.stop_stream()
    polly_stream.close()
    time.sleep(1)