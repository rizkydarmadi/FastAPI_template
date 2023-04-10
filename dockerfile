FROM python:3.11.0
LABEL version="1.0.0"
LABEL maintainer="rizkydarmadi@gmail.com"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8888

COPY . .

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]