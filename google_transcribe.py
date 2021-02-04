import urllib3
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build


def google_transcribe(recording):
  """
  Send Recorded Audio to Google Cloud for Transcription and return the transcription as formated word per line.
  """
  
  print("\n", 10 * "*" + "Google Transcribe" + 10 * "*")
  google_developer_key = os.environ.get('GOOGLE_DEVELOPER_KEY')
  scopes = ['https://www.googleapis.com/auth/cloud-platform']
  service = build('speech', 'v1', developerKey = google_developer_key )

  #Create the Google Client
  gsclient = speech.SpeechClient()

  #Make sure Google knows what type of audio file it is recieving
  audio = types.RecognitionAudio(content = recording)
  config = types.RecognitionConfig(
      encoding=enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
      sample_rate_hertz=8000,
      language_code='en-US')

  #Send the audio and wait for the response (syncronous)
  response = gsclient.recognize(config, audio)

  #Parse the response to get just the transcription and return
  print(response)
  print(response.results[0].alternatives[0].transcript)
  message = response.results[0].alternatives[0].transcript
  message = message.replace(' ', '\n')
  message = "[Google Transcription]\n" + message + "\n + \n"
  return message
