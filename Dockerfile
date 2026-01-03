FROM python:3.14.2-alpine3.23




WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
#ENV CONFIG_NAME=DevConfig
#ENV SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite
#ENV IS_DOCKER=1

COPY wsgi.py wsgi.py
COPY blog ./blog
#COPY instance ./instance
#при работе этого образа в compose убираем эту настройку(движок sqlite),
                            #так как БД будет постгрес



EXPOSE 5002

CMD ["python", "wsgi.py"]
