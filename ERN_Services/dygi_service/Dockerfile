FROM dygi:1.2

RUN apt-get update && apt-get -y install netcat && apt-get clean

RUN apt-get -y install cron
RUN apt-get -y install supervisor
RUN apt-get -y install procps
RUN apt-get -y install cpulimit

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir  -r requirements.txt

CMD ["supervisord","-c","/app/supervisor/services.conf"]
