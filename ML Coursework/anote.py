import wave 
import struct
from pvrecorder import PvRecorder
import whisper

def capture_audio():
  recorder = PvRecorder(device_index=-1, frame_length=512)
  audio = []

  try:
    recorder.start()
    print("Recording... Ctrl + C to stop")

    while True:
      frame = recorder.read()
      audio.extend(frame)
  except KeyboardInterrupt:
    print("Recording stopped")
    recorder.stop()

    with wave.open("output.wav", 'w') as f:
      f.setparams((1, 2, 16000, 0, "NONE", "NONE"))
      f.writeframes(struct.pack("h" * len(audio), *audio))
    print("Audio saved to output.wav")
  finally:
    recorder.delete()


  model = whisper.load_model("base")
  result = model.transcribe("./output.wav")
  print(result["text"])

# print("finished")
capture_audio()