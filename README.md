# TorCollector

### 주어진 seed onion마다 순회하며 모든 페이지를 수집하여 파일로 저장하는 tor crawler 프로그램

#### 프로그램 디자인
<img src="images/design.png" alt="collectorDesign" width="550">

#### 실행 방법
~~~
python3 run_multiprocess.py onion.txt
~~~

#### 추후 수정 사항
- 멀티 프로세싱 상에서 logging 추가  
- html content를 분석하여 onion category 자동 분류  
- Mongodb 연결  

