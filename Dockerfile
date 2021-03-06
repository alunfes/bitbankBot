FROM python:3.9


RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

WORKDIR /usr/src/app
#COPY requirements.txt ./
COPY ignore ./ignore
#COPY Data ./Data
#COPY btc-bot2 ./btc-bot2
COPY *.py ./

RUN pip install --upgrade pip
#RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./Master.py" ]
#CMD [ "python", "-m", "venv", "btc-bot2"]
#CMD [ "./btc-bot2/bin/pip", "install", "--upgrade", "pip"]
#CMD [ "./btc-bot2/bin/pip", "install", "--no-cache-dir", "-r", "requirements.txt"]
#CMD [ "./btc-bot2/bin/pip", "install", "--upgrade", "pip"]
#CMD [ "./btc-bot2/bin/python", "./Bot.py" ]