import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# the duration of the recording in seconds
duration = 1

# the sample rate (in samples/sec), change this value if needed
sample_rate = 16000

# use the sounddevice library to record audio
print("녹음 시작...")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()  # wait until the recording is done
print("녹음 완료.")

copied = recording[:]

for i in range(1, 11):
    write(str(i) + ".flac", sample_rate, recording)
    recording = np.append(recording, copied)
    print(len(recording))
