# Study Case Recruitment Associate Python Backend Engineer

## Requirements

- python 3.11.0
- docker-compose or postgresql 14 (docker compose recomended)
- os ubuntu 20.04 or 22.04

## How to install

- create virtual env
  ```bash
  python -m venv env
  ```
- install dependencies module
  ```bash
  python -r requirements.txt
  ```
- create database server with docker compose
  ```bash
  sudo docker-compose up -d
  ```
- migrate database
  ```bash
  python migration_up.py
  ```
- run server
  ```bash
  uvicorn main:app --reload --port 8888
  ```
- open [docs api](http://127.0.0.1:8888/docs)

## With Docker

- create database server with docker compose

  ```bash
  sudo docker-compose up -d
  ```

  - build docker

  ```bash
  docker build -t bithealth_test:1.0.0 .

  ```

- run docker
  ```bash
  sudo docker run -d -p 8888:8888 bithealth_test:1.0.0
  ```
