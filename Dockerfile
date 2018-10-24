FROM python:latest

ADD webserver.py /
ADD entrypoint.sh /

RUN pip install pymongo

EXPOSE 8000
RUN chmod +x entrypoint.sh
CMD "./entrypoint.sh"