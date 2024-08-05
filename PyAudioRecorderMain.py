import pyaudio
import wave
import threading
import sys
import time


def list_audio_devices():
    audio = pyaudio.PyAudio()
    print("Available audio input devices:")
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"Device ID {i}: {info['name']}")
    audio.terminate()


def record_audio(device_index, output_filename="output.wav"):
    # Audio parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

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

    print("Recording... Press 'q' and Enter to stop.")
    frames = []
    stop_recording = threading.Event() # an object that can be set (event has occurred) and cleared

    def check_for_stop(): # helper function to be threaded to run in conjunction with audio function to watch for user input
        while not stop_recording.is_set(): # checking if stop_recording is not set, if it is set the loop exits
            user_input = input() # input
            if user_input.lower() == 'q':
                stop_recording.set() # sets stop_recording, exits loop

    # Start a thread to monitor user input
    input_thread = threading.Thread(target=check_for_stop)
    input_thread.start()

    # Record audio until 'q' is pressed
    while not stop_recording.is_set():
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Wait for the input thread to finish
    input_thread.join()

    # Save the audio data to a file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Recording saved to {output_filename}")


# List devices
list_audio_devices()

# Ask user to select an input device
device_index = int(input("Enter the device ID to use for recording: "))

# Record audio using the selected device
record_audio(device_index)
