FROM python:3.7-alpine3.7

WORKDIR /home/petr/Documents/Projects/selltreck

RUN apk update && apk upgrade
# Add community repositories to install dependencies
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

# These dependencies are required for matplotlib and numpy
RUN apk --no-cache --update-cache add gcc freetype-dev libpng-dev musl-dev linux-headers g++ gfortran python3-dev

# This symlink fixes an error in numpy compilation
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

# Postgres libs and dependencies, plus python-ldap depdency
RUN apk --no-cache --update-cache add postgresql-libs postgresql-dev libffi-dev openldap-dev unixodbc-dev git



RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies python-dev py-pip build-base


COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN source venv/bin/activate
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY app app

ENV SERVER VDS1

EXPOSE 9876
ENTRYPOINT ["venv/bin/uvicorn", "--host", "0.0.0.0","--port", "9876", "app.main:app"]
