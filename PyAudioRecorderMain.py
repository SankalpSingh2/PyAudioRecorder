import pyaudio
import wave
def list_audio_devices():
audio = pyaudio.PyAudio()
print("Available audio input devices:")
for i in range(audio.get_device_count()):
info = audio.get_device_info_by_index(i)
if info["maxInputChannels"] > 0:
print(f"Device ID {i}: {info['name']}")

#pycharm commit
audio.terminate()
def record_audio(device_index, output_filename="output.wav"):
# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

# Initialize PyAudio
audio = pyaudio.PyAudio()
# Try to open the stream
try:
stream = audio.open(format=FORMAT,
channels=CHANNELS,
rate=RATE,
input=True,
input_device_index=device_index,
frames_per_buffer=CHUNK)

except OSError as e:
print(f"Could not open stream: {e}")
audio.terminate()
return

print("Recording...")
frames = []
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
data = stream.read(CHUNK)
frames.append(data)
print("Finished recording.")
# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the audio data to a file
wf = wave.open(output_filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
print(f"Recording saved to {output_filename}")
# List devices
list_audio_devices()
# Ask user to select an input device
device_index = int(input("Enter the device ID to use for recording: "))
# Record audio using the selected device
record_audio(device_index)