import asyncio
import sounddevice
import logging
from amazon_transcribe.client import TranscribeStreamingClient
from transcription import EventHandler
from bedrock_wrapper import BedrockWrapper
from config import config

logger = logging.getLogger(__name__)

class MicStream:
    async def mic_stream(self):
        logger.info(f"Starting mic stream")
        loop = asyncio.get_event_loop()
        input_queue = asyncio.Queue()

        def callback(indata, frame_count, time_info, status):
            loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))
        
        stream = sounddevice.RawInputStream(
            channels=1, samplerate=16000, callback=callback, blocksize=2048 * 2, dtype="int16")
        with stream:
            logger.debug(f"RawInputStream started")
            while True:
                indata, status = await input_queue.get()
                yield indata, status

    async def write_chunks(self, stream):
        total_bytes = 0
        mic_stream = self.mic_stream()
        logger.info(f"Writing bytes to AWS Transcribe")
        async for chunk, status in mic_stream:
            await stream.input_stream.send_audio_event(audio_chunk=chunk)
            total_bytes += len(chunk)
        await stream.input_stream.end_stream()

    async def basic_transcribe(self):
        logger.info(f"Creating AWS Transcribe Client")
        transcribe_streaming = TranscribeStreamingClient(region=config['region'])
        stream = await transcribe_streaming.start_stream_transcription(
            language_code="en-US",
            media_sample_rate_hz=24000,
            media_encoding="pcm",
        )
        handler = EventHandler(stream.output_stream, BedrockWrapper())

        await asyncio.gather(self.write_chunks(stream), handler.handle_events())