FROM python:3.5
MAINTAINER HJK <HJKdev@gmail.com>
RUN mkdir /lambda
WORKDIR /lambda
ADD . /lambda/
RUN apt-get install libxml2-dev libxslt-dev
RUN pip install -r requirements.txt
