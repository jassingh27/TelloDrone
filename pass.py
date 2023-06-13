import pyaudio
from djitellopy import Tello
from vosk import Model, KaldiRecognizer

tello = Tello()
tello.connect()

model = Model(r"/Users/jasdeepsingh/PycharmProjects/JasdeepTello/venv/bin/vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()

listening = False

def acquire_input():
    global listening 
    listening = True
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    while listening:
        stream.start_stream()
        try:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                response = result[14:-3]
                listening = False
                stream.close()
                return response
        except OSError:
            pass

def evaluate_input(input_text):  
    try:
        if input_text == "take off":
            tello.takeoff()
        elif input_text == "elevate":
            tello.move_up(40)
        elif input_text == "down":
            tello.move_down(40)
        elif input_text == "right":
            tello.move_right(40)
        elif input_text == "left":
            tello.move_left(40)
        elif input_text == "land":
            tello.land()
        else:
            print("Please give command again.")
    except Exception:
        pass

while True:
    print("Waiting for your command...")
    user_input = acquire_input()
    evaluate_input(user_input)
