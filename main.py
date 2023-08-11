import threading
import sounddevice as sd
import sys, os
from queue import Queue

# ASR 에 대한 모델 path 및 클래스, 함수 추가
sys.path.append(os.path.join(os.getcwd(), "model_speech_recognition"))
from inference import *

# interval 간격 녹음하는 쓰레드
class RecordThread(threading.Thread):
    def __init__(self, queue: Queue, interval: float = 0.1, sample_rate: int = 16000, exit_signal: bool = False):
        threading.Thread.__init__(self)
        self.queue = queue
        self.interval = interval
        self.sample_rate = sample_rate
        self.exit_signal = exit_signal

    def callback(self, indata, outdata, frames, time, status):
        self.queue.put(outdata)

    def run(self):
        while True:
            with sd.Stream(samplerate=self.sample_rate, channels=1, callback=self.callback):
                sd.sleep(int(self.interval * 1000))
                
            if self.exit_signal == True:
                break
                
    def kill(self):
        self.exit_signal = True


if __name__ == "__main__":
    # interval * max_len = 2 초에 대한 음성을 interval 간격으로 분석.
    interval = 0.1
    sample_rate = 16000
    max_len = 20

    result_queue = Queue()
    
    inference_thread = InferenceThread(result_queue, max_len)
    record_thread = RecordThread(inference_thread.queue, interval, sample_rate)
    
    record_thread.start()
    inference_thread.start()
    
    print("자동 음성인식 프로그램이 시작되었습니다.")
    
    try:
        while True:
            if result_queue.qsize() > 0:
                result = result_queue.get()
                print(result)
            else:
                continue
    except:
        # Thread 종료 진행
        record_thread.kill()
        inference_thread.kill()
        
    record_thread.join()
    inference_thread.join()

    print("자동 음성인식 프로그램이 종료되었습니다.")
