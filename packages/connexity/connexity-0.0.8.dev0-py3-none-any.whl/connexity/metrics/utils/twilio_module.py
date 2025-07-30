from asyncio import sleep

from twilio.rest import Client


class TwilioCallManager:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(self.account_sid, self.auth_token)

    async def get_call_duration(self, call_sid):

        call = self.client.calls(call_sid).fetch()

        duration = call.duration
        return duration

    async def get_call_recording_url(self, call_sid):

        recording_url = None
        i = 0

        while not recording_url:
            i += 1
            recordings = self.client.recordings.list(call_sid=call_sid)

            for recording in recordings:
                recording_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Recordings/{recording.sid}.wav"
                return recording_url

            await sleep(3)

            if i == 3:
                return None

    async def get_start_call_data(self, call_sid):

        call = self.client.calls(call_sid).fetch()

        start_time = call.start_time.isoformat().replace("+00:00", "Z")
        return start_time

    def start_call_recording(self, call_sid):
        recording = self.client.calls(call_sid).recordings.create()
        print(f"Recording started with SID: {recording.sid}")