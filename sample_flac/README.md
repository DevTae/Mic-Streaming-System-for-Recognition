### Mic-Streaming-System-for-Recognition

<br/>

- `Response Time 1초 보장`에 대한 조건을 만족하기 위하여, 우선적으로 모델에 대한 `추론 시간 측정`을 진행하였음.

- 실험 환경 세팅
  - CPU : `12th Gen Intel(R) Core(TM) i5-12400F`
  
  - 음성 데이터
    - `1` ~ `10` 초에 대한 단일 음성 녹음 파일에 대한 추론 시간 측정
  
  - 딥러닝 모델 구조
    - `CNN Layer` x 2
    - `GRU Layer` x 3
    - `hidden_dim` = 512
    - `use_bidirectional` = True

<br/>

- 실험 결과
  
  ![그림2](https://github.com/DevTae/Mic-Streaming-System-for-Recognition/assets/55177359/c05f45e8-ac7f-4cde-a55d-0b3f5770a438)

  - `음성 파일 길이`와 `추론 시간` 사이의 유의미한 관계가 있음을 발견하였음.
  - 음성 파일의 길이가 늘어날수록 요구되는 추론 시간이 길어졌음.
  - Response Time 을 줄이기 위하여 음성 파일의 길이를 줄이는 방법을 택할 수 있음.
 
