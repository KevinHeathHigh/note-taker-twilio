import urllib3
import json
import os

def deepgram_transcribe(recording):
  """
  Send Recorded Audio to Deepgram for Transcription and return the transcription as formated word per line.
  """
  print("\n", 10 * "*" + "Deepgram Transcribe" + 10 * "*")

  deepgram_account_sid = os.environ.get('DEEPGRAM_ACCOUNT_SID')
  deepgram_auth_token = os.environ.get('DEEPGRAM_AUTH_TOKEN')
  
  content_type = {'Content-Type':'application/octet-stream'}
  
  #There is no SDK, so have to do this the old fashion way
  deepgram_url = 'https://brain.deepgram.com/speech:recognize?async=false'
  
  #The a Basic Authorization header
  deepgram_creadentials = deepgram_account_sid + ':' + deepgram_auth_token
  deepgram_headers = urllib3.make_headers(basic_auth=deepgram_creadentials)
  deepgram_headers.update(content_type)
  http = urllib3.PoolManager()
  
  #POST the audio to Deepgram and wait for a response (syncronous)
  response = http.request('POST', deepgram_url, headers = deepgram_headers, body=recording)
  
  #Parse the transcription and return
  print(response.data)
  message = json.loads(response.data)['transcript']
  print(message)
  message = message.replace(' ', '\n')
  message = "[Deepgram Transcription]\n" + message + "\n"

  return message