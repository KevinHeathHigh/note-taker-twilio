import os

from watson_developer_cloud import SpeechToTextV1

def watson_transcribe(recording):
  """
  Send Recorded Audio to IBM Watson for Transcription and return the transcription as formated word per line.
  """
  print(10 * "*" + "Watson Transcribe" + 10 * "*")

  watson_username = os.environ.get('WATSON_USERNAME')
  watson_password = os.environ.get('WATSON_PASSWORD')

  #Connect to the Service
  speech_to_text = SpeechToTextV1(username=watson_username, password=watson_password, url='https://stream.watsonplatform.net/speech-to-text/api')
  
  #Send the audio and wait for the response (syncronous)
  response = speech_to_text.recognize(audio=recording,model='en-US_NarrowbandModel', content_type='audio/wav',timestamps=True,word_confidence=True)

  #Parse the response to get just the transcription and return
  print(response)
  message = response['results'][0]['alternatives'][0]['transcript']
  print(message)
  message = message.replace(' ', '\n')
  message = "[Watson Transcription]\n" + message + "\n"
  return message