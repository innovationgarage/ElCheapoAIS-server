FROM ubuntu:18.04

RUN apt update
RUN apt install -y python python-pip

RUN pip install twisted

ADD server.sh /server.sh
ADD server.py /server.py

CMD ["/bin/bash", "/server.sh"]
