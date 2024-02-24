FROM python:3.8.5

RUN apt-get update && apt-get -y install netcat && apt-get clean

RUN apt-get -y install nano
RUN apt-get -y install supervisor

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y install zsh
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
RUN export SHELL=/usr/bin/zsh

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir  -r requirements.txt
RUN pip install ipython

CMD ["supervisord","-c","/app/supervisor/services.conf"]