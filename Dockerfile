FROM python:alpine

RUN pip3 install google-api-python-client
RUN pip3 install google-auth-httplib2
RUN pip3 install google-auth-oauthlib
RUN pip3 install yamlreader

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

COPY src/ $APP_HOME/

ENTRYPOINT ["python3", "timer.py"]
