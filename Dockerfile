FROM python:3.14.2-alpine3.22

WORKDIR /app_docker

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
ENV CONFIG_NAME=DevConfig
ENV IS_DOCKER=1


COPY . .

EXPOSE 5002

CMD ["python", "wsgi.py"]
