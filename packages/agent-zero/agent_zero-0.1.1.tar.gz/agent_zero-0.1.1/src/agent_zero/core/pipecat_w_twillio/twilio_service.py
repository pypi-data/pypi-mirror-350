from twilio.rest import Client
from agent_zero.data.consts import (
    SERVER_ADDRESS,
    TWILIO_ACCOUNT_ID,
    TWILIO_AUTH_TOKEN,
)


class TwilioClient:
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_ID, TWILIO_AUTH_TOKEN)

    # Create a new phone number and route it to use this server
    def create_phone_number(self, area_code, agent_id):
        try:
            local_number = self.client.available_phone_numbers("US").local.list(
                area_code=area_code, limit=1
            )
            if local_number is None or local_number[0] == None:
                raise "No phone numbers of this area code."
            phone_number_object = self.client.incoming_phone_numbers.create(
                phone_number=local_number[0].phone_number,
                voice_url=f"https://phone.whoneedshumans.ai/twilio-voice-webhook/{agent_id}",
            )
            print("Getting phone number:", vars(phone_number_object))
            return phone_number_object
        except Exception as err:
            print(err)

    # Update this phone number to use provided agent id for inbound calls. Also updates voice URL address.
    def register_inbound_agent(self, phone_number, agent_id):
        try:
            phone_number_objects = self.client.incoming_phone_numbers.list(limit=200)
            numbers_sid = ""
            for phone_number_object in phone_number_objects:
                if phone_number_object.phone_number == phone_number:
                    number_sid = phone_number_object.sid
            if number_sid is None:
                print(
                    "Unable to locate this number in your Twilio account, is the number you used in BCP 47 format?"
                )
                return
            phone_number_object = self.client.incoming_phone_numbers(number_sid).update(
                voice_url=f"phone.whoneedshumans.ai/twilio-voice-webhook/{agent_id}"
            )
            print("Register phone agent:", vars(phone_number_object))
            return phone_number_object
        except Exception as err:
            print(err)

    # Release a phone number
    def delete_phone_number(self, phone_number):
        try:
            phone_number_objects = self.client.incoming_phone_numbers.list(limit=200)
            numbers_sid = ""
            for phone_number_object in phone_number_objects:
                if phone_number_object.phone_number == phone_number:
                    number_sid = phone_number_object.sid
                if number_sid is None:
                    print(
                        "Unable to locate this number in your Twilio account, is the number you used in BCP 47 format?"
                    )
                    return
                phone_number_object = self.client.incoming_phone_numbers(
                    number_sid
                ).delete()
                print("Delete phone number:", phone_number)
                return phone_number_object
        except Exception as err:
            print(err)

    # Use LLM function calling or some kind of parsing to determine when to let AI end the call
    def end_call(self, sid):
        try:
            call = self.client.calls(sid).update(
                twiml="<Response><Hangup/></Response>",
            )
            print(f"Ended call: ", vars(call))
        except Exception as err:
            print(err)

    # Use LLM function calling or some kind of parsing to determine when to transfer away this call
    def transfer_call(self, sid, to_number):
        try:
            call = self.client.calls(sid).update(
                twiml=f"<Response><Dial>{to_number}</Dial></Response>",
            )
            print(f"Transferred call: ", vars(call))
        except Exception as err:
            print(err)

    # Create an outbound call
    def create_phone_call(self, from_number, to_number):
        call = self.client.calls.create(
            machine_detection="Enable",  # detects if the other party is IVR
            machine_detection_timeout=8,
            async_amd="true",  # call webhook when determined whether it is machine
            async_amd_status_callback=f"https://{SERVER_ADDRESS}/outbound/webhook",  # Webhook url for machine detection
            url=f"https://{SERVER_ADDRESS}/outbound/webhook",
            to=to_number,
            from_=from_number,
            status_callback=f"https://{SERVER_ADDRESS}/call_status",
            status_callback_method="POST",
            status_callback_event=[
                "initiated",
                "ringing",
                "answered",
                "completed",
                "failed",
                "busy",
            ],
        )
        print(f"Calling {to_number} from {from_number}")
        return call.sid
