import os
import urllib3

from flask import Flask, request, json, make_response
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

import watson_transcribe
import google_transcribe

app = Flask(__name__)

@app.route('/twilio', methods=['GET', 'POST'])
def twilio():
    """
    Listen for new calls, greet the caller, and record the note.
    """
    
    print("\n", 10 * '*' + 'Twilio Inbound Call' + 10 * '*') 
    print('Twilio Call SID: ' + request.args.get('CallSid'))
    print('Twilio From: ' + request.args.get('From'))
    print('Twilio To: ' + request.args.get('To'))
    
    #Save off the Caller and Callee numbers to send Notes later
    global fromNumber, toNumber
    fromNumber = request.args.get('From')
    toNumber = request.args.get('To')
    
    #Create the response to play to the caller
    resp = VoiceResponse()
    resp.say("Start taking notes after the beep, press # when finished.")
    resp.record(play_beep='true', max_length=20, finish_on_key='#', recording_status_callback="/twilio_recording")
    print(str(resp))
    return str(resp)

@app.route('/twilio_recording', methods=['GET', 'POST'])
def twilio_recording():
    """
    Listen for recording status from Twilio, when recieved 
        parse the recording URL, 
        download the recording, 
        send it off to be transcribed and
        then send the transcription back via SMS
    """
    
    print("\n", 10 * '*' + 'Twilio Recording' + 10 * '*') 
    print(request.values)
    
    #Download the recording
    recording_url = request.values.get('RecordingUrl')
    recording = get_twilio_recording(recording_url)
    
    #Get the transcription and send the SMS for each service (syncronous)
    send_note_to_sms(watson_transcribe.watson_transcribe(recording))
    send_note_to_sms(google_transcribe.google_transcribe(recording))
    return make_response('OK', 203)

def get_twilio_recording(recordingUrl):
    """
    Retrieve the Recording from Twilo and return the actual data
    """
    
    print("\n", 10 * '*' + 'Get Twilio Recording' + 10 * '*') 
    #Doing this the old fashion way
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_creadentials = twilio_account_sid + ':' + twilio_auth_token
    twilio_headers = urllib3.make_headers(basic_auth=twilio_creadentials)
    http = urllib3.PoolManager()
    recording = http.request('GET', recordingUrl, headers = twilio_headers)
    return recording.data

def send_note_to_sms(message):
    """
    Sends the Transcribed message back to the caller via SMS
    """

    print("\n", 10 * '*' + 'Send Twilio SMS' + 10 * '*') 
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
   
    #Create the Twilio Client
    twilio_client = Client(twilio_account_sid, twilio_auth_token)
   
    #Send the SMS
    sms_message = twilio_client.messages.create(
        to = fromNumber,
        from_ = toNumber,
        body = message
    )
    print(sms_message)

if __name__ == "__main__":
    print("\n",10 * '*' + 'Note Taker' + 10 * '*')
    note_taker_host = os.environ.get("NOTE_TAKER_HOST", "localhost")
    note_taker_port = int(os.environ.get("NOTE_TAKER_PORT", 8080))
    app.run(host=note_taker_host, port=note_taker_port, debug=True)
    