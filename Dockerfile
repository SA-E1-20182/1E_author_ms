FROM python:3
EXPOSE 7999
ADD webserver.py /
ADD entrypoint.sh /
RUN python3 -m pip install pymongo
RUN python3 -m pip install flask
RUN python3 -m pip install Flask-PyMongo
RUN chmod +x entrypoint.sh
CMD "./entrypoint.sh"
