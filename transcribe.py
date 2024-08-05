import requests
import json

# Constants
DEEPGRAM_API_URL = 'https://api.deepgram.com/v1/listen'
API_KEY = '5f4fe351582b00798d7356af58e56d5042e6e681'  # Replace with your actual Deepgram API key
AUDIO_FILE_PATH = 'output.wav'  # Replace with your audio file name
OUTPUT_FILE_PATH = 'transcription.txt'

# Read audio file
with open(AUDIO_FILE_PATH, 'rb') as audio_file:
    audio_data = audio_file.read()

# Make API request
headers = {
    'Authorization': f'Token {API_KEY}',
    'Content-Type': 'audio/wav'
}
response = requests.post(DEEPGRAM_API_URL, headers=headers, data=audio_data)

if response.status_code != 200:
    print(f'Error: {response.status_code}')
    print(response.text)
    exit()

# Extract and save transcription
transcription_data = response.json()
transcription_text = transcription_data['results']['channels'][0]['alternatives'][0]['transcript']

with open(OUTPUT_FILE_PATH, 'w') as output_file:
    output_file.write(transcription_text)

print(f'Transcription saved to {OUTPUT_FILE_PATH}')
