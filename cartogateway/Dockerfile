FROM ubuntu:18.04

RUN echo Version 2

RUN apt-get update
RUN apt-get install -y python2.7 python-pip
RUN apt-get install -y netcat-openbsd
RUN pip install libais
RUN pip install psycopg2

ADD server.sh /server.sh
ADD update.py /update.py

CMD ["/server.sh"]
