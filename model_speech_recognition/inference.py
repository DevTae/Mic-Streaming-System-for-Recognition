import threading
import numpy as np
from queue import Queue

# ASR 모델 Inference Thread
class InferenceThread(threading.Thread):
    def __init__(self, result_queue: Queue, max_len: int = 20):
        threading.Thread.__init__(self)
        self.queue = Queue()
        self.result_queue = result_queue
        self.recorded_list = list()
        self.max_len = max_len
        self.exit_signal = False
        self.Inference = Inference()

    def run(self):
        while True:
            recorded_item = self.queue.get()
            self.recorded_list.append(recorded_item)
            
            # 만약 recorded_list 길이가 max_len 보다 크면 inference 진행
            if len(self.recorded_list) >= self.max_len:
                for i in range(1, len(self.recorded_list)):
                    self.recorded_list[0] = np.append(self.recorded_list[0], self.recorded_list[i])
                target = self.recorded_list[0]
                self.recorded_list = self.recorded_list[-self.max_len+1:]
                result = self.Inference(target)
                self.result_queue.put(result) # main.py 에 있는 queue 로 값 전송
                
            if self.exit_signal == True:
                break

    def kill(self):
        self.exit_signal = True


class Inference(object):
    def __init__(self):
        pass

    # 해당 함수에서 ASR 에 대한 inference 함수를 호출하면 됨.
    def __call__(self, audio) -> str:
        return "Done"
