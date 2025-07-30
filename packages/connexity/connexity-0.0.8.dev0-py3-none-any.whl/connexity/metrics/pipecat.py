import sys
from math import trunc
from typing import Literal

from connexity.client import ConnexityClient
from pipecat.frames.frames import (
    BotStartedSpeakingFrame,
    BotStoppedSpeakingFrame,
    UserStartedSpeakingFrame,
    UserStoppedSpeakingFrame,
    TTSTextFrame, TranscriptionFrame, CancelFrame, MetricsFrame, FunctionCallInProgressFrame, FunctionCallResultFrame
)
from pipecat.observers.base_observer import BaseObserver, FramePushed

from pipecat.processors.frame_processor import FrameDirection
from pipecat.transports.network.fastapi_websocket import FastAPIWebsocketOutputTransport
from connexity.calls.base_call import BaseCall
from connexity.metrics.utils.twilio_module import TwilioCallManager
from connexity.calls.messages.user_message import UserMessage
from connexity.calls.messages.assistant_message import AssistantMessage
from connexity.calls.messages.tool_call_message import ToolCallMessage
from connexity.calls.messages.tool_result_message import ToolResultMessage
from connexity.metrics.utils.validate_json import validate_json
from loguru import logger


class ConnexityTwilioObserver(BaseObserver):

    MIN_SEPARATION = 0.5

    def __init__(self):

        self.call: BaseCall | None = None
        self.user_data = {"start": None, "content": "", "end": None, "role": 'user'}
        self.assistant_data = {"start": None, "content": "", "end": None, "role": "assistant",
                               "latency": {"tts": None, "llm": None, "stt": None}}
        self.tool_calls = {"start": None, "content": "", "end": None, "role": "tool_call"}
        self.messages = []

        # additional data for connexity
        self.sid = None
        self.twilio_client: TwilioCallManager | None = None
        self.final = False

    async def initialize(self,
                         agent_id: str,
                         api_key: str,
                         sid: str,
                         phone_call_provider: str,
                         user_phone_number: str,
                         agent_phone_number: str,
                         twilio_account_sid: str,
                         twilio_auth_token: str,
                         voice_provider: str,
                         llm_provider: str,
                         llm_model: str,
                         call_type: Literal["inbound", "outbound", "web"],
                         transcriber: str,
                         ):
        self.sid = sid
        self.twilio_client = TwilioCallManager(twilio_account_sid, twilio_auth_token)
        connexity_client = ConnexityClient(api_key=api_key)
        self.twilio_client.start_call_recording(sid)

        self.call = await connexity_client.register_call(
            sid=sid,
            agent_id=agent_id,
            user_phone_number=user_phone_number,
            agent_phone_number=agent_phone_number,
            created_at=None,
            voice_engine='pipecat',
            voice_provider=voice_provider,
            call_type=call_type,
            llm_provider=llm_provider,
            llm_model=llm_model,
            phone_call_provider=phone_call_provider,
            transcriber=transcriber,
            stream=False
        )

    def check_min_separation(self, prev_time, current_time):
        if prev_time is None or (current_time - prev_time) > self.MIN_SEPARATION:
            return current_time
        else:
            return prev_time

    async def on_push_frame(
            self,
            data: FramePushed,
    ):

        src = data.source
        dst = data.destination
        frame = data.frame
        direction = data.direction
        timestamp = data.timestamp

        # Convert timestamp to seconds for readability
        time_sec = timestamp / 1_000_000_000

        if isinstance(frame, BotStartedSpeakingFrame) and isinstance(src,
                                                                     FastAPIWebsocketOutputTransport) and direction == FrameDirection.DOWNSTREAM:

            self.assistant_data['start'] = self.check_min_separation(self.assistant_data.get('start'), time_sec)
            print(f"CONNEXITY SDK DEBUG| BOT START SPEAKING: {time_sec}", flush=True)

        elif isinstance(frame, BotStoppedSpeakingFrame) and isinstance(src,
                                                                       FastAPIWebsocketOutputTransport) and direction == FrameDirection.DOWNSTREAM:

            self.assistant_data['end'] = self.check_min_separation(self.assistant_data.get('end'), time_sec)
            print(f"CONNEXITY SDK DEBUG| BOT STOP SPEAKING: {time_sec}", flush=True)

        elif isinstance(frame, UserStartedSpeakingFrame) and isinstance(src,
                                                                        FastAPIWebsocketOutputTransport) and direction == FrameDirection.DOWNSTREAM:
            self.user_data['start'] = time_sec
            print(f"CONNEXITY SDK DEBUG| USER START SPEAKING: {time_sec}", flush=True)

        elif isinstance(frame, UserStoppedSpeakingFrame) and isinstance(src,
                                                                        FastAPIWebsocketOutputTransport) and direction == FrameDirection.DOWNSTREAM:
            self.user_data['end'] = time_sec
            print(f"CONNEXITY SDK DEBUG| USER STOP SPEAKING: {time_sec}", flush=True)

        if isinstance(frame, MetricsFrame) and isinstance(src,
                                                          FastAPIWebsocketOutputTransport) and direction == FrameDirection.DOWNSTREAM:
            for metric in frame.data:
                if hasattr(metric, 'processor') and hasattr(metric, 'value'):
                    if 'LLMService' in metric.processor:
                        self.assistant_data["latency"]["llm"] = metric.value * 1000
                        print(f"CONNEXITY SDK DEBUG| LLM METRIC: {metric.value * 1000}", flush=True)

                    elif 'TTSService' in metric.processor:
                        self.assistant_data["latency"]["tts"] = metric.value * 1000
                        print(f"CONNEXITY SDK DEBUG| TTS METRIC: {metric.value * 1000}", flush=True)

                    elif 'STTService' in metric.processor:
                        self.assistant_data["latency"]["stt"] = metric.value * 1000
                        print(f"CONNEXITY SDK DEBUG| STT METRIC: {metric.value * 1000}", flush=True)


        # TODO FUNCTION CALLS NEED ADDITIONAL CHECKING
        if isinstance(frame, FunctionCallInProgressFrame) and isinstance(src,
                                                                         FastAPIWebsocketOutputTransport) and direction == FrameDirection.DOWNSTREAM:
            self.tool_calls['start'] = self.check_min_separation(self.tool_calls.get('start'), time_sec)
            self.tool_calls['tool_call_id'] = frame.tool_call_id
            self.tool_calls['function_name'] = frame.function_name
            self.tool_calls['arguments'] = frame.arguments
            await self.call.register_message(ToolCallMessage(arguments=frame.arguments, tool_call_id=frame.tool_call_id,
                                                             content='', name=frame.function_name,
                                                             seconds_from_start=time_sec))
            print(f"CONNEXITY SDK DEBUG| FUNCTION CALL STARTED: {frame.tool_call_id, frame.function_name, frame.arguments}")

        # TODO FUNCTION RESULT NEED ADDITIONAL CHECKING
        if isinstance(frame, FunctionCallResultFrame) and isinstance(src,
                                                                     FastAPIWebsocketOutputTransport) and direction == FrameDirection.DOWNSTREAM:
            self.tool_calls['end'] = self.check_min_separation(self.tool_calls.get('end'), time_sec)
            self.tool_calls['content'] = frame.result

            is_json, json_data = validate_json(frame.result)

            await self.call.register_message(ToolResultMessage(content="",
                                                               tool_call_id=frame.tool_call_id,
                                                               result_type="JSON" if is_json else "string",
                                                               result=json_data if is_json else frame.result,
                                                               seconds_from_start=time_sec
                                                               ))
            print(f"CONNEXITY SDK DEBUG| FUNCTION CALL END: {frame.tool_call_id, frame.function_name, frame.result}", flush=True)

        if isinstance(frame, TranscriptionFrame):
            self.user_data['content'] += frame.text

        if isinstance(frame, TTSTextFrame) and isinstance(src, FastAPIWebsocketOutputTransport):
            self.assistant_data['content'] += frame.text + " "

        if self.user_data.get('start') and self.user_data.get('end') and self.user_data.get('content') and self.user_data.get('start') < self.user_data.get('end'):
            self.messages.append(self.user_data)
            await self.call.register_message(
                UserMessage(content=self.user_data.get('content'), seconds_from_start=self.user_data.get('start')))

            print(f"CONNEXITY SDK DEBUG| USER DATA COLLECTED: {self.user_data}", flush=True)

            self.user_data = {"start": None, "content": "", "end": None, "role": 'user'}

        if self.assistant_data.get('start') and self.assistant_data.get('end') and self.assistant_data.get('content') and self.assistant_data.get('start') < self.assistant_data.get('end'):
            latency = None
            if self.messages and self.messages[-1].get('role') == 'user':
                latency = (self.assistant_data['start'] - self.messages[-1]['end']) * 1000

            self.messages.append(self.assistant_data)

            await self.call.register_message(AssistantMessage(content=self.assistant_data['content'],
                                                              time_to_first_audio=latency,
                                                              seconds_from_start=self.assistant_data['start'],
                                                              latency=self.assistant_data.get("latency")))

            print(f"CONNEXITY SDK DEBUG| BOT DATA COLLECTED: {self.assistant_data}", flush=True)

            self.assistant_data = {"start": None, "content": "", "end": None, "role": 'user',
                                   "latency": {"tts": None, "llm": None, "stt": None}}

        if isinstance(frame, CancelFrame) and not self.final:
            self.final = True
            created_at = await self.twilio_client.get_start_call_data(self.sid)
            duration = await self.twilio_client.get_call_duration(self.sid)
            recording_url = await self.twilio_client.get_call_recording_url(self.sid)

            print('CONNEXITY SDK DEBUG| CALL COLLECTED DATA:', flush=True)
            print(self.messages, flush=True)

            await self.call.init_post_call_data(recording_url=recording_url, created_at=created_at,
                                                duration_in_seconds=duration)
