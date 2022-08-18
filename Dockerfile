FROM python:3.8

RUN apt update && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove \
    && apt-get clean

ADD ./web/requirements.txt /web/
RUN python3 -m pip install --no-cache-dir -U -r /web/requirements.txt

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /web

CMD python server.py
