from agent_zero.data.consts import TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_ID

account_sid = TWILIO_ACCOUNT_ID
auth_token = TWILIO_AUTH_TOKEN
from twilio.rest import Client

client = Client(account_sid, auth_token)


def start_call_recording(call_sid):
    try:
        recording = client.calls(call_sid).recordings.create()
        print(f"Recording started with SID: {recording.sid}")
        return recording.sid
    except Exception as e:
        print(f"Error starting recording: {e}")
        return None


import os
from asyncio import sleep

from twilio.rest import Client


async def get_audio_url_and_call_duration(call_sid):
    client = Client(os.environ["TWILIO_ACCOUNT_ID"], os.environ["TWILIO_AUTH_TOKEN"])

    call = client.calls(call_sid).fetch()

    duration = call.duration

    recording_url = None
    i = 0

    while not recording_url:
        i += 1
        recordings = client.recordings.list(call_sid=call_sid)

        # Print the download URL for each recording
        for recording in recordings:
            recording_url = f"https://api.twilio.com/2010-04-01/Accounts/AC1a6945ca60362f4460c15c6583e2e63f/Recordings/{recording.sid}.mp3"
            print(f"Download URL for recording {recording.sid}: {recording_url}")
            return recording_url, duration
        await sleep(3)
        if i == 3:
            return None, duration
