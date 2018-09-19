# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_DEBUG 1
ENV COMMAND service

# Set the working directory to /app
WORKDIR /app

# Upgrade debian
RUN DEBIAN_FRONTEND="noninteractive" apt-get update -y
RUN DEBIAN_FRONTEND="noninteractive" apt-get install build-essential python-dev default-libmysqlclient-dev -y

COPY requirements.txt /tmp/
RUN cd /tmp && pip install -r requirements.txt
COPY requirements_test.txt /tmp/
RUN cd /tmp && pip install -r requirements_test.txt
#COPY requirements_internal.txt /tmp/
#RUN cd /tmp && pip install --extra-index-url https://op:FY1Pdtk5j5@pypi.openpublishing.com/ -r requirements_internal.txt

# Copy the current directory contents into the container at /app
COPY open_publishing /app/open_publishing
COPY tests /app/tests
COPY setup.cfg /app
COPY .pylintrc /app

# Some linting
RUN pylint -s n -j 8 --rcfile=.pylintrc tests
RUN flake8 tests
RUN pydocstyle tests

# Entrypoint:
ENTRYPOINT ["nosetests"]
