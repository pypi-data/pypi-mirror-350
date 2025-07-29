from twilio.rest import Client
from agent_zero.data.consts import TWILIO_ACCOUNT_ID, TWILIO_AUTH_TOKEN


def end_call(sid: str) -> None:
    """
    End a Twilio call by setting its status to 'completed'.

    Args:
        sid (str): The SID of the Twilio call to end.
    """
    client = Client(TWILIO_ACCOUNT_ID, TWILIO_AUTH_TOKEN)
    client.calls(sid).update(status="completed")
