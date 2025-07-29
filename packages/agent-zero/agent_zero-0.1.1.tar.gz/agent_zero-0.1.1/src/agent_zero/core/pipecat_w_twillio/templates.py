twiml_template_inbound = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="wss://{wss_url}/inbound/ws"></Stream>
    </Connect>
    <Pause length="40"/>
</Response>
"""

twiml_template_inbound_partial = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="wss://{wss_url}/inbound/ws"></Stream>
  </Connect>
  <Pause length="40"/>
</Response>
"""

twiml_template_outbound = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="wss://{wss_url}/outbound/ws"></Stream>
  </Connect>
  <Pause length="40"/>
</Response>
"""

twiml_template_outbound_partial = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Start>
    <Transcription statusCallbackUrl="https://{transcription_url}/twilio_transcription" track="outbound_track" speechModel="telephony" transcriptionEngine="google" outboundTrackLabel="core" partialResults="true" />
  </Start>
  <Connect>
    <Stream url="wss://{wss_url}/outbound/ws"></Stream>
  </Connect>
  <Pause length="40"/>
</Response>
"""

twiml_template_outbound_with_play = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Play>{audio_url}</Play>
  <Connect>
    <Stream url="wss://{wss_url}/outbound/ws"></Stream>
  </Connect>
  <Pause length="40"/>
</Response>
"""
