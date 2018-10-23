FROM python:3

ADD webserver.py /

RUN pip install pymongo

EXPOSE 8000
CMD [ "python", "./webserver.py" ]