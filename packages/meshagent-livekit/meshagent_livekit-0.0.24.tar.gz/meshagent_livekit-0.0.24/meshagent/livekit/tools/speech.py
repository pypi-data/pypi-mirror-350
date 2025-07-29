import uuid
from livekit import rtc
from livekit.agents.tts import TTS
from typing import Optional

from ..agents.voice import VoiceConnection
from meshagent.tools.toolkit import Toolkit, Tool, FileResponse, ToolContext, TextResponse

from livekit.plugins import elevenlabs
from livekit.plugins import cartesia
from livekit.plugins import openai
from livekit.plugins import playai

class SpeechTools(Toolkit):
    def __init__(self):
        super().__init__(
        name="meshagent.speech",
        title="voice",
        description="speech to text tools",    
        tools=[
            ElevenTextToSpeech(),
            CartesiaTextToSpeech(),
            OpenAITextToSpeech(),
            PlayHTTextToSpeech(),
        ])


async def synthesize(tts: TTS, text:str):

    frames = list[rtc.AudioFrame]()
    stream = tts.synthesize(text=text)
    try:
        async for chunk in stream:
            frame : rtc.AudioFrame = chunk.frame
            frames.append(frame)

        merged = rtc.combine_audio_frames(frames)
        return FileResponse(data=merged.to_wav_bytes(), name= str(uuid.uuid4())+".wav", mime_type="audio/wav")
    finally:
        await stream.aclose()


class PlayHTTextToSpeech(Tool):
    def __init__(self):
        super().__init__(
            name="playht_text_to_speech",
            title="PlayHT text to speech",
            description="generate an audio file, converting text to speech",
            input_schema={
                "type" : "object",
                "properties" : {
                    "input_text" : {
                        "type" : "string",
                        "description" : "the text to convert to speech",
                    },
                    "model" : {
                        "type": "string",
                        "description" : "(default: PlayDialog)",
                        "enum" : [ "Play3.0-mini", "PlayDialog", "PlayHT2.0-turbo" ]
                    },
                    "sample_rate" : {
                        "type" : "number",
                        "description" : "(default: 48000)",
                        "enum" : [ 48000, 24000 ]
                    }
                },
                "required": ["input_text","model","sample_rate"],
                "additionalProperties" : False,   
        })

  
    
    async def execute(self, *, context: ToolContext, input_text: str, sample_rate: int, model: str):
        tts = playai.TTS(
            model=model,
            sample_rate=sample_rate,
        )

        return await synthesize(tts, input_text)

class ElevenTextToSpeech(Tool):
    def __init__(self):
        super().__init__(
            name="eleven_labs_text_to_speech",
            title="ElevenLabs text to speech",
            description="generate an audio file, converting text to speech",
            input_schema={
                "type" : "object",
                "properties" : {
                    "input_text" : {
                        "type" : "string",
                        "description" : "the text to convert to speech",
                    },
                    "voice_id" : {
                        "type" : "string",
                        "description" : "the id of a voice to use (default: EXAVITQu4vr4xnSDxMaL)",
                    },
                    "voice_name" : {
                        "type" : "string",
                        "description" : "the name of the voice to use (optional)",
                    },
                    "voice_category" : {
                        "type" : "string",
                        "description" : "the category of the voice to use (optional, default: premade)",
                        "enum" : [
                            "generated", "cloned", "premade", "professional", "famous", "high_quality"
                        ]
                    },
                    "model" : {
                        "type": "string",
                        "description" : "(default: eleven_flash_v2_5)",
                        "enum" : [ "eleven_multilingual_v2", "eleven_flash_v2_5", "eleven_flash_v2", "eleven_multilingual_sts_v2", "eleven_english_sts_v2" ]
                    },
                    "encoding" : {
                        "type" : "string",
                        "description" : "(default: pcm_44100)",
                        "enum" : [ "pcm_44100", "mp3_22050_32" ]
                    }
                },
                "required": ["input_text","voice_id","model","encoding", "voice_name", "voice_category"],
                "additionalProperties" : False,   
        })

  
    
    async def execute(self, *, context: ToolContext, input_text: str, voice_id: str, voice_name:str, voice_category:str, model: str, encoding: str):
        tts = elevenlabs.TTS(
            model_id=model,
            encoding=encoding,
            voice=elevenlabs.Voice(id=voice_id, name=voice_name, category=voice_category)
        )

        return await synthesize(tts, input_text)


class CartesiaTextToSpeech(Tool):
    def __init__(self):
        super().__init__(
            name="cartesia_text_to_speech",
            title="Cartesia text to speech",
            description="generate an audio file, converting text to speech",
            input_schema={
                "type" : "object",
                "properties" : {
                    "input_text" : {
                        "type" : "string",
                        "description" : "the text to convert to speech",
                    },
                    "voice" : {
                        "type" : "string",
                        "description" : "the id of a voice to use (default: c2ac25f9-ecc4-4f56-9095-651354df60c0)"
                    },
                    "model" : {
                        "type": "string",
                        "description" : "(default: sonic-english)",
                        "enum" : [ "sonic", "sonic-preview", "sonic-2024-12-12", "sonic-2024-10-19", "sonic-english", "sonic-multilingual" ]
                    },
                    "speed" : {
                        "type" : "string",
                        "description" : "(default: normal)",
                        "enum" : ["fastest", "fast", "normal", "slow", "slowest" ]
                    },
                    "encoding" : {
                        "type" : "string",
                        "description" : "(default: pcm_s16le)",
                        "enum" : [ "pcm_s16le" ]
                    },
                    "emotion" : {
                        "type" : "array",
                        "items" : {
                            "type": "string",
                            "enum" : [ 
                                "anger:lowest", 
                                "positivity:lowest",
                                "surprise:lowest",
                                "sadness:lowest",
                                "curiosity:lowest" 
                                "anger:low", 
                                "positivity:low",
                                "surprise:low",
                                "sadness:low",
                                "curiosity:low" 
                                "anger:medium", 
                                "positivity",
                                "surprise",
                                "sadness",
                                "curiosity" 
                                "anger:high", 
                                "positivity:high",
                                "surprise:high",
                                "sadness:high",
                                "curiosity:high",
                                "anger:highest", 
                                "positivity:highest",
                                "surprise:highest",
                                "sadness:highest",
                                "curiosity:highest" 

                            ]
                        }
                    }
                },
                "required": ["input_text", "voice","speed","emotion","encoding","model"],
                "additionalProperties" : False,   
        })
    
    async def execute(self, *, context: ToolContext, input_text: str, voice: str, model: str, speed: str, emotion: list, encoding: str):
        tts = cartesia.TTS(
            encoding=encoding,
            model=model,
            voice=voice,
            emotion=emotion,
            speed=speed
        )

        return await synthesize(tts, input_text)  


class OpenAITextToSpeech(Tool):
    def __init__(self):
        super().__init__(
            name="openai_text_to_speech",
            title="OpenAI text to speech",
            description="generate an audio file, converting text to speech",
            input_schema={
                "type" : "object",
                "properties" : {
                    "input_text" : {
                        "type" : "string",
                        "description" : "the text to convert to speech",
                    },
                    "voice" : {
                        "type" : "string",
                        "description" : "the id of a voice to use (default: alloy)",
                        "enum" : [
                            "alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"
                        ]
                    },
                    "model" : {
                        "type": "string",
                        "description" : "(default: tts-1)",
                        "enum" : [ "tts-1", "tts-1-hd" ]
                    },
                    "speed" : {
                        "type" : "number",
                        "description" : "(default: 1.0)",
                    },
                },
                "required": ["input_text", "voice", "model", "speed"],
                "additionalProperties" : False,   
        })
    
    async def execute(self, *, context: ToolContext, input_text: str, voice: str, model: str, speed: float):
        tts = openai.TTS(
            model=model,
            voice=voice,
            speed=speed
        )

        return await synthesize(tts, input_text)