FROM ubuntu:18.04

WORKDIR /usr/src/app

COPY . .

RUN apt-get update -y && apt-get install -y libsm6 libxext6 && apt-get install python3 -y && apt-get install python3-pip -y 

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]



