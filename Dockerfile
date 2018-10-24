FROM python:3
EXPOSE 7999
ADD webserver.py /
ADD entrypoint.sh /
RUN python3 -m pip install pymongo
RUN chmod +x entrypoint.sh
CMD "./entrypoint.sh"
