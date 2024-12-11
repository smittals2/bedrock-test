import sys
import asyncio
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent, TranscriptResultStream
from concurrent.futures import ThreadPoolExecutor
from text_to_speech import aws_polly_tts
from user_input_manager import UserInputManager
from config import printer, config

class EventHandler(TranscriptResultStreamHandler):
    text = []
    last_time = 0
    sample_count = 0
    max_sample_counter = 20

    def __init__(self, transcript_result_stream: TranscriptResultStream, bedrock_wrapper):
        super().__init__(transcript_result_stream)
        self.bedrock_wrapper = bedrock_wrapper

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        if not self.bedrock_wrapper.is_speaking():
            if results:
                for result in results:
                    EventHandler.sample_count = 0
                    if not result.is_partial:
                        for alt in result.alternatives:
                            print(alt.transcript, flush=True, end=' ')
                            EventHandler.text.append(alt.transcript)
            else:
                EventHandler.sample_count += 1
                if EventHandler.sample_count == EventHandler.max_sample_counter:
                    if len(EventHandler.text) == 0: 
                        # last_speech = config['last_speech']
                        # print(last_speech, flush=True)
                        # aws_polly_tts(last_speech)
                        # sys.exit(0)
                        EventHandler.sample_count = 0
                    if len(EventHandler.text) != 0:
                        input_text = ' '.join(EventHandler.text)
                        printer(f'\n[INFO] User input: {input_text}', 'info')

                        executor = ThreadPoolExecutor(max_workers=1)
                        UserInputManager.set_executor(executor)
                        asyncio.get_event_loop().run_in_executor(
                            executor,
                            self.bedrock_wrapper.invoke_bedrock,
                            input_text
                        )

                    EventHandler.text.clear()
                    EventHandler.sample_count = 0