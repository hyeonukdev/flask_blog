# Baseline 이미지
FROM python:3

# 라이브러리 업데이트 및 설치
RUN apt-get update
RUN apt-get install python3-pip -y

# flask-app이 있는 github repository clone
WORKDIR /home/ubuntu/
RUN git clone https://github.com/hyeonukdev/flask_blog.git
WORKDIR flask_blog

# requirements.txt 파일 내부에 있는 라이브러리 전부 설치
RUN pip3 install -r requirements.txt

# container 실행 시, 실행할 명령어
CMD ["python", "run.py", "--host", "0.0.0.0"]