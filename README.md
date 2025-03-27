# TorCollector

#### 주어진 seed onion마다 순회하며 모든 페이지를 수집하여 파일로 저장하는 tor crawler 프로그램
<br>

### 프로그램 디자인
<img src="images/design.png" alt="collectorDesign" width="650">
<br>

### 수집 컨테이너 실행 방법
#### 도커 이미지 빌드 
~~~
docker build -t torc:latest .
~~~

#### 수집 컨테이너 실행
~~~
docker run -it --name <container_name> torc:latest
~~~

#### 개별 수집 코드 실행
~~~
python3 run_multiprocess.py onion.txt
~~~

#### seed onion 주소 추가
onion.txt 파일에 수집 대상 .onion 주소를 한 줄씩 추가

### seed onion 추가 수집
#### Dockerfile 수정
~~~
ENTRYPOINT ["sh", "mine_onions.sh"]
~~~

#### 도커 이미지 빌드 
~~~
docker build -t mineo:latest .
~~~

#### URL 수집을 원하는 키워드를 포함해 컨테이너 실행
~~~
docker run -it --name <container_name> mineo:latest <keyword>
~~~
