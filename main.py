import threading
import sounddevice as sd
import sys, os
from queue import Queue

# ASR 에 대한 모델 path 및 클래스, 함수 추가
sys.path.append(os.path.join(os.getcwd(), "model_speech_recognition"))
from inference import *

# interval 간격 녹음하는 쓰레드
class AudioRecordThread(threading.Thread):
    def __init__(self, queue: Queue, interval: float = 0.1, sample_rate: int = 16000, exit_signal: bool = False):
        threading.Thread.__init__(self)
        self.queue = queue
        self.interval = interval
        self.sample_rate = sample_rate
        self.exit_signal = exit_signal
        self.datas = list()

    def callback(self, indata, frames, time, status):
        self.datas += [ item for sublist in indata for item in sublist ]

        if len(self.datas) >= self.interval * self.sample_rate:
            self.queue.put(self.datas)
            self.datas = list()

    def run(self):
        with sd.Stream(samplerate=self.sample_rate, dtype='float32', channels=1, callback=self.callback):
            while self.exit_signal == False:
                pass
                
    def kill(self):
        self.exit_signal = True


if __name__ == "__main__":
    # interval * max_len = 2 초에 대한 음성을 interval 간격으로 분석.
    interval = 0.1
    sample_rate = 16000
    max_len = 20

    audio_result_queue = Queue()
    
    audio_inference_thread = AudioInferenceThread(audio_result_queue, max_len)
    audio_record_thread = AudioRecordThread(audio_inference_thread.queue, interval, sample_rate)
    
    audio_record_thread.start()
    audio_inference_thread.start()
    
    print("자동 음성인식 프로그램이 시작되었습니다.")
    
    try:
        while True:
            if audio_result_queue.qsize() > 0:
                result = audio_result_queue.get()
                print(result)
            else:
                continue
    except:
        # Thread 종료 진행
        audio_record_thread.kill()
        audio_inference_thread.kill()
        
    audio_record_thread.join()
    audio_inference_thread.join()

    print("자동 음성인식 프로그램이 종료되었습니다.")
